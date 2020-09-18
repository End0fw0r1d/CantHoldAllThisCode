import discord, os, asyncio, time, threading
from discord.ext import commands
from discord.ext.commands import Bot
from discord import Emoji
from discord import File
from multiprocessing.connection import Listener
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

acceptedEnds = ['.png','.gif','.jpg']
messageQueue = []

# client
def child(conn):
    try:
        msg = conn.recv()
        messageQueue.append([msg[0],msg[1]])
    except:
        print("reception error")
    print(len(messageQueue))

# server
def mother():
    print('starting...')
    listener = Listener(('',5000))
    while True:
        conn = listener.accept()
        child(conn)
        
bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    print('test')
    thr = threading.Thread(target=mother)
    thr.start()
    while True:
        if len(messageQueue) > 0:
            chId, msgTxt = messageQueue.pop(0)
            channel = bot.get_channel(int(chId))
            if msgTxt[-4:] in acceptedEnds:
                try:
                    await channel.send(file=discord.File(msgTxt))
                except:
                    await channel.send("resultant file too large...")
                os.remove(msgTxt)
            else:
                await channel.send(str(msgTxt))
        await asyncio.sleep(0.05)
    #await mother(('', 5000))
 
bot.run(TOKEN)
##after you send an image, make sure to delete image file

