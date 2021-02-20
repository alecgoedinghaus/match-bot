import discord
import os

BOT_TOKEN = os.getenv('BOT_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    elif message.content.startswith('!survey'):
        users = message.mentions
        for user in users:
            await user.send('https://forms.gle/n7xtMYnZEqwPQ1p67')


client.run(BOT_TOKEN)