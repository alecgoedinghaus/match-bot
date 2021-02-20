import discord
from discord.ext import commands
import os

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)

@bot.command()
async def survey(ctx):
    users = ctx.message.mentions
    for user in users:
        await user.send('https://forms.gle/n7xtMYnZEqwPQ1p67')

bot.run(BOT_TOKEN)