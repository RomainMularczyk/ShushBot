from collections import Counter
from typing import AsyncIterator, Counter, List, Tuple
from discord import Message


class ShusherBot:
    """Discord Shusher bot modules. Provides functions to calculate the ratio
    of messages an author wrote in a particular channel."""

    async def retrieve_channel_data(self, channel_id: int) -> Counter[str]:
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
            if msg.author.name != "ShushBot":
                author_data[msg.author.name] += 1

        return author_data

    @staticmethod
    async def check_ratio(
        author: str, authors_stats: Counter[str]
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

    @staticmethod
    def display_message(author_name: str, perc: float) -> str:
        """Return message to display to loud authors.

        Parameters
        ----------
        author_name : str
            The author's name.

        perc: float
            Percentage of the messages sent on the channel by the author.

        Returns
        -------
        str
            The message to display to loud authors.
        """
        message: str = (
            f"You need to shut the fuck up, now {author_name}."
            + f" That's cause you wrote {perc}% of the messages of this channel."
        )
        return message
