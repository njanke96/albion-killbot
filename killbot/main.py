"""
Module containing main function
"""
import argparse
import logging
import coloredlogs
from collections import defaultdict

from .discord_bot import discord_client


def killbot_main():
    ## Argument parsing
    parser = argparse.ArgumentParser(
        description="Basic Albion Online discord kill and death notification bot."
    )

    # Token
    parser.add_argument(
        "token",
        metavar="BOT_TOKEN",
        type=str,
        nargs=1,
        help="The Discord bot token to use.",
    )

    # verbosity
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        help="Default log level is INFO. -v sets the logging level to DEBUG.",
    )

    args = parser.parse_args()
    bot_token = args.token[0]

    # logging level
    loglvl = logging.INFO
    v_count = int(args.verbose or 0)
    if v_count > 0:
        loglvl = logging.DEBUG

    # Logging config
    coloredlogs.install(fmt="[%(asctime)-15s] %(levelname)s: %(message)s", level=loglvl)

    # bot event loop
    logging.info("Starting Discord client...")
    discord_client.run(bot_token)
