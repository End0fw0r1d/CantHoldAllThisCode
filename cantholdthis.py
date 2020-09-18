import asyncio
import json
import os
import random
from multiprocessing.connection import Client

import discord
import discord.ext
from discord.ext import commands
from dotenv import load_dotenv
from mcstatus import MinecraftServer

minecraftIP = 'minecraft.hackervoiceim.in:25565'

commandList = ["speed", "mocking", "space", "shoot", "italics", "jpeg", "man", "jpeg2", "jpeg3", "weee", "shake", "nuke", "moreshake", "hold", "hold2",
               "overlay", "overlay2"]
# the above is kinda hacky, but I want to process all valid commands the same way, so just put any valid/currently used commands here...
# if we want to dynamically update this for added features without restarting the bot, maybe move this to a text file or something, and re-read it on a command input

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


def getID(Input):
    try:
        idString = Input[Input.rfind(':') + 1:-1]
    except:
        idString = Input
    return idString


bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    while True:
        try:
            server = MinecraftServer.lookup(minecraftIP)
            status = server.status()
            string = "Boyville, population: {0}".format(status.players.online)
            ##string = "I'm a bot and I do bot things"
            activity = discord.Game(name=string)
            await bot.change_presence(status=discord.Status.online, activity=activity)
            await asyncio.sleep(60)
        except:
            activity = discord.Game(name="server is broke")
            await bot.change_presence(status=discord.Status.online, activity=activity)
            await asyncio.sleep(60)


@bot.command(name="intense", aliases=commandList)
async def thing(ctx, *, message):
    # print(message, ctx.command)
    c = Client(('localhost', 5001))
    payload = json.dumps({"channel": ctx.message.channel.id, "command": str(ctx.invoked_with), "userinput": message})  # pass on the command plus the contents
    c.send(payload)


@bot.command(name='boys')
async def boysOnline(context):
    try:
        server = MinecraftServer.lookup(minecraftIP)
        status = server.status()
        stpart1 = "There are " + str(status.players.online) + " boys online, query took " + str(status.latency) + " ms"
        stpart2 = ""
        try:
            if status.players.online > 0:
                query = server.query()
                stpart2 = "\nThe following boys are online: " + str(query.players.names)
        except:
            stpart2 = "\nUnable to get playerlist"
        response = stpart1 + stpart2
    except:
        response = "Unable to reach server"
    client = Client(('localhost', 5000))
    payload = [context.message.channel.id, response]  # payload is [0] == channel id, [1] == message/filename
    client.send(payload)


@bot.command(name='conch')
async def magicConch(context):
    conchAnswers = ['As I see it, yes.', 'Ask again later.', 'Better not tell you now.', 'Cannot predict now.', 'Concentrate and ask again.',
                    'Don\'t count on it.', 'It is certain.', 'It is decidedly so.', 'Most likely.', 'My reply is no.', 'My sources say no.',
                    'Outlook not so good.', 'Outlook good.', 'Reply hazy, try again.', 'Signs point to yes.', 'Very doubtful.', 'Without a doubt.', 'Yes.',
                    'Yes - definitely.', 'You may rely on it.']
    answer = random.randint(0, 19)
    client = Client(('localhost', 5000))
    response = ":shell:" + conchAnswers[answer]
    payload = [context.message.channel.id, response]  # payload is [0] == channel id, [1] == message/filename
    client.send(payload)


@bot.command(name='why')
async def fortheglory(context):
    ##glory = Image.open('forthegloryofsatan.jpg')
    await context.channel.send(file=discord.File('forthegloryofsatan.jpg'))


@bot.command(name='navyseal')
async def fortheglory(context):
    ##glory = Image.open('forthegloryofsatan.jpg')
    await context.channel.send(file=discord.File('navyseal.gif'))


@bot.command(name='I')
async def iguess(context, *, message):
    if message == 'guess':
        ##await context.channel.send(file=discord.File('iguess.gif'))
        await context.channel.send('https://i.imgur.com/MMaciGr.gif')


@bot.command(name='God')
async def doyouthink(context):
    await context.channel.send('http://pockisho.net/albums/DoYouThink/DoYouThink.webm')


miscCommands = ["boys", "why", "navyseal", "I guess", "God"]

bot.remove_command('help')


@bot.command(name='help')
async def helping(ctx):
    response = "intense, " + ", ".join(commandList) + ", " + ", ".join(miscCommands)
    client = Client(('localhost', 5000))
    payload = [ctx.message.channel.id, response]  # payload is [0] == channel id, [1] == message/filename
    client.send(payload)


bot.run(TOKEN)
