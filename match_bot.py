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
    print(bot.user.name + " is here to spice up your discord server today!")
    print(bot.user.id)


@bot.command(brief='Sends out compatibility survey to targeted user.')
async def survey(ctx):
    users = ctx.message.mentions
    for user in users:
        await user.send('Welcome to our server!\nPlease fill out this survey at your earliest convenience!\nhttps://forms.gle/vV2DbQJduPhps4AR7')


@bot.command(brief='Compares survey results to determine most compatible pairs of users.')
async def match(ctx):
    if(not ctx.message.author.guild_permissions.administrator):
        await ctx.send("***HEY YOU DON'T HAVE PERMISSIONS FOR THIS COMMAND***")
        return
    await ctx.send("***Coffee Chats incoming in 3..2..1..***")
    pref_data = from_sheets.survey_to_df()
    matcher.populate_categorical(pref_data)
    matrix = matcher.convert_categorical(pref_data)
    pairs = matcher.pair(matrix)
    pair_generator = matcher.solve_stm(pairs)
    lookup_table = make_reverse_lookup(ctx.guild.members)
    for pair in clean_list(pair_generator):
        channel_name = generate_channel_name(pair)
        chat_channel = await ctx.guild.create_text_channel(channel_name)
        for member_player in pair:
            member_name = member_player.name
            member = lookup_table.get(member_name)
            invite = await chat_channel.create_invite()
            await member.send("Have a great conversation :smile:/n" + invite.url)


@bot.command(brief='Simple call command to verify the bot isn\'t dead.')
async def ping(ctx):
    await ctx.message.channel.send("Po(n)g!")


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
