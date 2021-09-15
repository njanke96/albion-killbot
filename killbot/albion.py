"""
Albion unofficial API interface
https://www.tools4albion.com/api_info.php
"""
import logging
import aiohttp
from datetime import datetime

BASE_URL = "https://gameinfo.albiononline.com/api/gameinfo"
API_CALL_TIMEOUT = 30


class KillEvent:
    """
    Structured data from the /events endpoint.
    Constructed with a dict representing json data for the event
    """
    def __init__(self, ev):
        killer = ev["Killer"]
        victim = ev["Victim"]

        # killer and victim info
        self.killer_name = killer["Name"]
        self.killer_ip = int(killer["AverageItemPower"])
        self.victim_name = victim["Name"]
        self.victim_ip = int(victim["AverageItemPower"])

        # kill info
        self.kill_fame = int(killer["KillFame"])
        self.event_id = ev["EventId"]
        self.event_link = f"https://albiononline.com/en/killboard/kill/{self.event_id}"
        self.timestamp = _parse_timestamp(ev["TimeStamp"])
        self.num_assists = len(ev["Participants"]) - 1


async def get_pvp_kills(guild_id_list, limit=51, offset=0):
    """
    Returns a list of KillEvent objects filtered by guild IDs in guild_id_list. Returns None
    if the request failed.

    guild_id_list: [str]
    limit and offset are directly passed to the API call.
    """
    async with aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=API_CALL_TIMEOUT)
    ) as sess:

        try:
            async with sess.get(
                BASE_URL + "/events", params={"limit": limit, "offset": offset}
            ) as resp:
                # check status
                if resp.status != 200:
                    logging.warning(
                        f"Status code {resp.status} when checking kill events!"
                    )
                    return None

                resp_json = await resp.json()

                return [
                    KillEvent(x)
                    for x in resp_json
                    if x["Killer"]["GuildId"] in guild_id_list
                    or x["Victim"]["GuildId"] in guild_id_list
                ]

        except Exception as e:
            logging.debug("Encountered an error on kill event request: {0}".format(e))
            return None


def _parse_timestamp(timestamp_str):
    """
    Parse a timestamp in the Albion server's format.
    Returns a datetime object.
    """
    # ignore millis and 'Z' char
    return datetime.fromisoformat(timestamp_str.split(".")[0])
