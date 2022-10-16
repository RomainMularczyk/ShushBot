import os
from dotenv import load_dotenv
from client.client import DiscordClient
from client.intents import load_intents

# ---- Load dotenv ----
load_dotenv()
token: str = os.environ.get("DISCORD_BOT_TOKEN")

# ---- Start client ----
intents = load_intents()
client = DiscordClient(intents=intents)
# cmds = BotCommands(client)
client.run(token)
