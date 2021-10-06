"""
Discord bot module.
Contains the discord bot functions and underlying discord client.
"""
import logging
import asyncio
import discord
from collections import deque

from .albion import get_pvp_kills

SLEEP_TIME = 10

class DiscordClient(discord.Client):
    """
    The discord client (bot)

    msg_channel_id: Channel ID to send messages in.
    """

    def __init__(self, msg_channel_id, guild_list, alliance_list, player_list):
        super().__init__()
        self.channel_id = msg_channel_id
        self.guild_list = guild_list
        self.alliance_list = alliance_list
        self.player_list = player_list

        # past 20 event ids
        self.event_history = deque()

    async def on_ready(self):
        logging.info(f"Logged on to discord as {self.user}.")

        # validate the provided channel id
        channel = self.get_channel(self.channel_id)
        if not channel:
            logging.critical(
                f"Channel id {self.channel_id} does not represent a valid channel. Check permissions."
            )
            self.loop.stop()

        # start killboard check loop
        self.loop.create_task(self.killboard_check_loop())

    async def killboard_check_loop(self):
        channel = self.get_channel(self.channel_id)
        logging.info("Watching the killboard...")
        logging.info("GuildID List: " + str(self.guild_list))

        while True:
            i = 0
            while i <= 200:
                events = await get_pvp_kills(self.guild_list, self.player_list, self.alliance_list, 51, i) or []
                i += 50

            if events:
                for event in events:
                    if event.event_id in self.event_history:
                        continue

                    logging.info(f"Sending kill event notification for event id {event.event_id}")

                    embed = discord.Embed(
                        title="Kill Event",
                        url=event.event_link,
                        description=f"{event.killer_name} ({event.killer_ip} IP) has killed {event.victim_name} "
                        f"({event.victim_ip} IP) for {event.kill_fame} fame! They were assisted by "
                        f"{event.num_assists} other players.",
                        color=0xFF5733
                    )

                    await channel.send(embed=embed)

                    if len(self.event_history) >= 256:
                        self.event_history.pop()

                    self.event_history.appendleft(event.event_id)

            await asyncio.sleep(SLEEP_TIME)
