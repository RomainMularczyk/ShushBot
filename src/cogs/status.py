from typing import AsyncIterator, List
from discord.ext import commands
from discord import Message, TextChannel


class Status(commands.Cog, name="Status"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print("Status cog loaded.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def status(self, ctx: commands.Context) -> None:
        messages: List[Message] = Status.get_channel_messages(ctx)
        await ctx.send("Let me think for a second...")

    @commands.command()
    async def top_words(self, ctx: commands.Context, top_num: int) -> None:
        """Retrieves the top n words from the channel history.

        Parameters
        ----------
        ctx : Context
            The context attached to the command.
        top_num : int
            The number of top words to retrieve.

        Returns
        -------
        Dict[str, int]
            A dictionary associating a word and the number of
            its occurrences.
        """
        messages: List[Message] = await Status.get_channel_messages(ctx)
        print(messages[0])
        await ctx.send("This word")

    @commands.command()
    async def top_words_member(
        self, ctx: commands.Context, top_num: int, member: str
    ) -> None:
        """Retrieves the top n words from the channel history for
        a member of that channel.

        Parameters
        ----------
        ctx : Context
            The context attached to the command.
        top_num : int
            The number of top words to retrieve.
        member : str
            The nickname of the channel member.

        Returns
        -------
        Dict[str, int]
            A dictionary associating a word and the number of
            its occurrences.
        """
        await ctx.send("Top member numbers")

    @staticmethod
    async def get_channel_messages(ctx: commands.Context):
        history_iterator: AsyncIterator[Message] = ctx.message.channel.history(
            limit=1000
        )
        messages: List[Message] = [msg async for msg in history_iterator]
        return messages


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Status(bot))
