from discord.ext import commands

bot = commands.Bot(command_prefix="/")


@bot.command()
async def status(ctx):
    await ctx.send("coucou")
