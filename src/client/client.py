import os
from typing import Tuple, Counter

from dotenv import load_dotenv
from discord.ext.commands import Bot
from discord import Intents
from discord import Message

from bot.shusher import ShusherBot


# ---- Load dotenv ----
load_dotenv()
token: str = os.environ.get("DISCORD_BOT_TOKEN")


# ---- Client ----
class DiscordClient(Bot, ShusherBot):
    """Describes a Discord client."""

    def __init__(self, intents: Intents, command_prefix: str, name: str) -> None:
        super(DiscordClient, self).__init__(
            intents=intents, command_prefix=command_prefix, name=name
        )

    async def on_ready(self) -> None:
        print(f"Logged in as {self.user.name} with the ID {self.user.id}.")

    async def on_message(self, message: Message) -> None:
        # Process command before going further
        await self.process_commands(message)
        # Do the usually things
        current_channel_id: int = message.channel.id
        authors_stats: Counter[str] = await self.retrieve_channel_data(
            current_channel_id
        )
        ratio: Tuple[bool, float] = await self.check_ratio(
            message.author.name, authors_stats
        )
        if ratio[0]:
            await message.reply(self.display_message(message.author.name, ratio[1]))
