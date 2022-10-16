import os
from collections import Counter
from dotenv import load_dotenv
from discord import Client
from discord import Intents
from discord.message import Message
from typing import AsyncIterator, List, Dict, Tuple


# ---- Load dotenv ----
load_dotenv()
token: str = os.environ.get("DISCORD_BOT_TOKEN")


# ---- Client ----
class DiscordClient(Client):
    """Describes a Discord client."""

    def __init__(self, intents: Intents) -> None:
        super().__init__(intents=intents)

    async def on_ready(self) -> None:
        print(f"Logged in as {self.user.name} with the ID {self.user.id}.")

    async def on_message(self, message) -> None:
        current_channel_id: int = message.channel.id
        authors_stats: Counter[str, int] = await self.retrieve_channel_data(
            current_channel_id
        )
        ratio: Tuple[bool, float] = await self.check_ratio(
            message.author.name, authors_stats
        )
        if ratio[0]:
            await message.reply(
                f"""You need to shut the fuck up, now {message.author.name}. That's cause you wrote {ratio[1]}% of the messages of this channel."""
            )

    async def retrieve_channel_data(self, channel_id: int) -> Counter[str, int]:
        """Returns a counter of the number of messages each member of the channel
        sent.

        Parameters
        ----------
        channel_id : int
            The ID of a Discord channel.

        Returns
        -------
        Counter
            A counter of the number of messages each member of the channel sent.
        """
        history_iterator: AsyncIterator[Message] = self.get_channel(channel_id).history(
            limit=1000
        )
        messages: List[Message] = [msg async for msg in history_iterator]
        author_data: Counter = Counter()
        for msg in messages:
            author_data[msg.author.name] += 1

        return author_data

    async def check_ratio(
        self, author: str, authors_stats: Counter[str, int]
    ) -> Tuple[bool, float]:
        """Checks if the discussion message ratio of the author is under
        15%.

        Parameters
        ----------
        author : str
            The name of the author of the message.
        authors_stats : Counter(str, int)
            A counter representing the number of messages each author has sent over the
            last 1000 messages.

        Returns
        -------
        Tuple(bool, float)
            A tuple made of :
            - A boolean value checking if the author wrote more than 15% of the messages
            of the channel
            - A float number representing the percentage of the messages he/she sent on
            the channel
        """
        total_perc: float = round(
            authors_stats[author] / authors_stats.total() * 100, 2
        )
        if authors_stats[author] > authors_stats.total() * 15 / 100:
            return (True, total_perc)
        else:
            return (False, total_perc)
