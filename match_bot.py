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
    print(pref_data)
    matcher.populate_categorical(pref_data)
    matrix = matcher.convert_categorical(pref_data)
    pairs = matcher.pair(matrix)
    # print(pairs)
    pair_generator = matcher.solve_stm(pairs)
    print(list(pair_generator))
    lookup_table = make_reverse_lookup(ctx.guild.members)
    print(lookup_table)
    for pair in clean_list(pair_generator):
        channel_name = generate_channel_name(pair)
        chat_channel = await ctx.guild.create_text_channel(channel_name)
        for member_player in pair:
            member_name = member_player.name
            print(member_name)
            member = lookup_table.get(member_name)
            invite = await chat_channel.create_invite()
            await member.send("invite link: " + invite.url)


def make_reverse_lookup(member_list):
    return {member.name + "#" + member.discriminator: member for member in member_list}


def clean_list(pair_generator):
    sent_list = []
    cleaned_list = []
    for pair in pair_generator:
        if is_valid_pair(pair, sent_list):
            cleaned_list.append(pair)
            for member in pair:
                sent_list.append(member.name)
    return cleaned_list


def generate_channel_name(pair_of_players):
    out = ""
    out += pair_of_players[0].name.split("#")[0]
    out += "--"
    out += pair_of_players[1].name.split("#")[0]
    return out


def is_valid_pair(pair_of_players, sent_list):
    for player in pair_of_players:
        if player is None:
            return False
        elif player.name in sent_list:
            return False
    return True


bot.run(BOT_TOKEN)
