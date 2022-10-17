from discord.ext import commands


class TooMuch(commands.Cog, name="TooMuch"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print("TooMuch cog loaded.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def toomuch(self, ctx: commands.Context) -> None:
        print("ouais")
        await ctx.send("coucou")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(TooMuch(bot))
