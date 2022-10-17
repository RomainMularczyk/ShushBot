import os
import asyncio
from dotenv import load_dotenv
from discord.ext import commands
from client.client import DiscordClient
from client.intents import load_intents


# ---- Load dotenv ----
load_dotenv()
token: str = os.environ.get("DISCORD_BOT_TOKEN")

# ---- Start client ----
intents = load_intents()
client = DiscordClient(command_prefix="/", intents=intents)


async def load_extensions() -> None:
    """Load all the cogs extensions defined in the './cogs' directory."""
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            await client.load_extension(f"cogs.{file[:-3]}")


async def main() -> None:
    await load_extensions()
    await client.start(token)


if __name__ == "__main__":
    asyncio.run(main())
