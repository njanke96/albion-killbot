"""
Discord bot module.
Contains the discord bot functions and underlying discord client.
"""
import logging
import asyncio
import discord


class DiscordClient(discord.Client):
    """
    The discord client (bot)

    msg_channel_id: Channel ID to send messages in.
    """

    def __init__(self, msg_channel_id):
        super().__init__()
        try:
            self.channel_id = int(msg_channel_id)
        except ValueError:
            logging.critical(f'Unable to cast "{msg_channel_id}" to int as channel id.')
            exit(-1)

    async def on_ready(self):
        logging.info(f"Logged on to discord as {self.user}.")

        # validate the provided channel id
        channel = self.get_channel(self.channel_id)
        if not channel:
            logging.critical(
                f"Channel id {self.channel_id} does not represent a valid channel. Check permissions."
            )
            self.loop.stop()

        # start loop
        self.loop.create_task(self.killboard_check_loop())

    async def killboard_check_loop(self):
        channel = self.get_channel(self.channel_id)

        while True:
            await channel.send("Hello!")
            await asyncio.sleep(2)
