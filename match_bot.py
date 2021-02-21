import discord
from discord.ext import commands
import os

import from_sheets
import matcher

BOT_TOKEN = os.getenv('BOT_TOKEN')

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)


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
    # print(pref_data)
    matrix = matcher.convert_categorical(pref_data)
    pairs = matcher.pair(matrix)
    # print(pairs)
    pair_generator = matcher.solve_stm(pairs)
    print(list(pair_generator))
    lookup_table = make_reverse_lookup(ctx.guild.members)
    print(lookup_table)
    # for adam, eve in pair_generator:
    #     print(lookup_table[adam])
    #     print(lookup_table[eve])


def make_reverse_lookup(member_list):
    return {member.name : member.id for member in member_list}


bot.run(BOT_TOKEN)
