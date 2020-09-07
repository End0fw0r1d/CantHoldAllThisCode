import os, glob, time, asyncio, discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord import Emoji
from discord import File
from dotenv import load_dotenv
import Levenshtein as lev
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='.')

@bot.event
async def on_message(message):
    if str(message.author.id) in ['164200668255485953','95630487023779840']:
        if 's' in message.content and 't' in message.content and message.content[0] == 's':
            ind = 0
            while True:
                ind = message.content.find('s',ind)
                ind2 = message.content.find('t',ind)+1
                if ind == -1 or ind2 == -1:
                    break
                substr = message.content[ind:ind2]
                Distance = lev.ratio('shut',substr)
                if Distance > 0.8:
                    print('yes')
                    emoji = bot.get_emoji(562674675981746191)
                    await message.add_reaction(emoji)
                    break
                ind += 1
    if str(message.author.id) != '688455378492850226' and str(message.channel.id) == '149032569038438402':
        if 's' in message.content and 't' in message.content:
            ind = 0
            while True:
                ind = message.content.find('s',ind)
                ind2 = message.content.find('t',ind)+1
                print(ind,ind2)
                if ind == -1 or ind2 == -1:
                    break
                substr = message.content[ind:ind2]
                print(substr)
                Distance = lev.ratio('shut',substr)
                print(Distance)
                if Distance > 0.8:
                    break
                ind += 1

bot.run(TOKEN)
