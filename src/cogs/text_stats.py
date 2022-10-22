from typing import AsyncIterator, List, Dict
from discord import Message
from discord.ext import commands
from src.stats.stats import BotStats


class TextStats(commands.Cog, name="TextStats"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print("Status cog loaded.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def my_stats(self, ctx: commands.Context) -> None:
        messages: List[Message] = await TextStats.get_channel_messages(ctx)
        messages_without_bot: List[Message] = [
            msg.author for msg in messages if msg.author.name != "ShushBot"
        ]
        my_messages: List[Message] = [
            msg.author for msg in messages if msg.author.name == ctx.author.name
        ]
        my_messages_ratio: int = len(my_messages) / len(messages_without_bot) * 100
        await ctx.reply(
            f"You sent {round(my_messages_ratio, 2)}% of this channel over the last 1000 messages."
        )

    @commands.command()
    async def top_words_member(
        self, ctx: commands.Context, top_num: str, member: str
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
        dict
            A dictionary associating a word and the number of
            its occurrences.
        """
        if await TextStats.check_top_words_arg(top_num, ctx):
            messages: List[Message] = await TextStats.get_channel_messages(ctx)
            stats = BotStats.top_words_per_member(messages, member)
            most_common: Dict[str, int] = stats.most_common(int(top_num))
            # Create template string
            formatted_str: str = ""
            for word, count in most_common:
                formatted_str += f"- **{word}** : {count}\n"
            await ctx.reply(
                f"Top {top_num} most common words used by {member} on this channel are :\n"
                + formatted_str
            )

    @commands.command()
    async def top_words(self, ctx: commands.Context, top_num: str) -> None:
        """Retrieves the top n words from the channel history.

        Parameters
        ----------
        ctx : Context
            The context attached to the command.
        top_num : int
            The number of top words to retrieve. Must be between 1 and 15.

        Returns
        -------
        dict
            A dictionary associating a word and the number of
            its occurrences.
        """
        if await TextStats.check_top_words_arg(top_num, ctx):
            messages: List[Message] = await TextStats.get_channel_messages(ctx)
            stats = BotStats.top_words(messages)
            most_common: Dict[str, int] = stats.most_common(int(top_num))
            # Create template string
            formatted_str: str = ""
            for word, count in most_common:
                formatted_str += f"- **{word}** : {count}\n"
            await ctx.reply(
                f"Top {top_num} most common words on this channel are :\n"
                + formatted_str
            )

    @staticmethod
    async def check_top_words_arg(arg, ctx: commands.Context) -> bool:
        try:
            if int(arg) <= 0:
                await ctx.reply(
                    "`/top_words` command cannot take negative values.\n"
                    + "Please insert a value between 1 and 15."
                )
                return False
            elif int(arg) > 15:
                await ctx.reply(
                    "`/top_words` command cannot take values higher than 15.\n"
                    + "Please insert a value between 1 and 15."
                )
                return False
            else:
                # Value is between 1 and 15 and is an integer
                return True
        except ValueError:
            await ctx.reply(
                "`/top_words` command follows this pattern : `/top_words <number>`.\n"
                + "Please pass a number as argument."
            )
            return False

    @staticmethod
    async def get_channel_messages(ctx: commands.Context):
        """Get the last 1000 messages of the channel.

        Parameters
        ----------
        ctx : Context
            The context attached to the command.

        Returns
        -------
        list
            A list of the last 1000 messages of the channel.
        """
        history_iterator: AsyncIterator[Message] = ctx.message.channel.history(
            limit=1000
        )
        messages: List[Message] = [msg async for msg in history_iterator]
        return messages


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(TextStats(bot))
