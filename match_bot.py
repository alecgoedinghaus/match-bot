import discord
from discord.ext import commands
import os

import from_sheets
import matcher

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

@bot.command()
async def match(ctx):
    print("running matching...")
    pref_data = from_sheets.survey_to_df()
    print(pref_data)
    #print(matcher.convert_categorical(pref_data))
    matrix = matcher.convert_categorical(pref_data)
    pairs = matcher.pair(matrix)

bot.run(BOT_TOKEN)
