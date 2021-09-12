"""
Discord bot module.
Contains the discord bot functions and underlying discord client.
"""
import logging
import asyncio
import discord


class _DiscordClient(discord.Client):
    async def on_ready(self):
        logging.info(f"Logged on to discord as {self.user}.")

        # start loop
        self.loop.create_task(self.killboard_check_loop())

    async def killboard_check_loop(self):
        while True:
            print("ayooo!")
            await asyncio.sleep(2)


discord_client = _DiscordClient()
