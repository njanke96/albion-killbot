"""
Module containing main function
"""
import os
import argparse
import logging
import coloredlogs
from collections import defaultdict

from .discord_bot import DiscordClient


def killbot_main():
    ## Argument parsing
    parser = argparse.ArgumentParser(
        description="Basic Albion Online discord kill and death notification bot."
    )

    # verbosity
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        help="Default log level is INFO. -v sets the logging level to DEBUG.",
    )

    args = parser.parse_args()

    # logging level
    loglvl = logging.INFO
    v_count = int(args.verbose or 0)
    if v_count > 0:
        loglvl = logging.DEBUG

    # Logging config
    coloredlogs.install(fmt="[%(asctime)-15s] %(levelname)s: %(message)s", level=loglvl)

    # bot event loop
    logging.info("Starting Discord client...")

    # sanitizing
    try:
        channel_id = int(os.environ["AOKB_CHANNEL_ID"])
    except ValueError:
        logging.critical(f'Unable to cast "{os.environ["AOKB_CHANNEL_ID"]}" to int as channel id.')
        exit(-1)

    try:
        guild_list = os.environ["AOKB_GUILD_IDS"].split(",")[:-1]
        alliance_list = os.environ["AOKB_ALLIANCE_IDS"].split(",")[:-1]
        player_list = os.environ["AOKB_PLAYER_IDS"].split(",")[:-1]

        discord_client = DiscordClient(channel_id, guild_list, alliance_list, player_list)
        discord_client.run(os.environ["AOKB_BOT_TOKEN"])
        
    except KeyError:
        logging.critical(
            "Required environment variable missing."
        )
        exit(-1)
