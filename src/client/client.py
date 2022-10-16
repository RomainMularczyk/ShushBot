import os
from dotenv import load_dotenv
from discord import Client
from discord import Intents

# ---- Load dotenv ----
load_dotenv()
token: str = os.environ.get("DISCORD_BOT_TOKEN")


class DiscordClient(Client):
    def __init__(self, intents: Intents) -> None:
        super().__init__(intents=intents)

    async def on_ready(self) -> None:
        print("Logged in as")
        print(self.user.name)
        print(self.user.id)
        print("-----")

    async def on_message(self, message) -> None:
        print(message.guild)
        return
