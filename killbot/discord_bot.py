"""
Discord bot module.
Contains the discord bot functions and underlying discord client.
"""
import logging
import asyncio
import aiohttp
import discord


class DiscordClient(discord.Client):
    """
    The discord client (bot)

    msg_channel_id: Channel ID to send messages in.
    """

    def __init__(self, msg_channel_id):
        super().__init__()
        self.channel_id = msg_channel_id

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

        await channel.send("Curtis has died, R I P")

    async def killboard_check_loop(self):
        channel = self.get_channel(self.channel_id)

        while True:
            await asyncio.sleep(20)
