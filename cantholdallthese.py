from PIL import Image, ImageFilter, GifImagePlugin, ImageSequence
import os, glob
import math, random
import io
import discord
import requests
from discord.ext import commands
from discord.ext.commands import Bot
from discord import Emoji
from discord import File
from dotenv import load_dotenv
from pygifsicle import optimize

X = [226,160,280,198,255,280,160]
Y = [515,530,540,550,550,585,645]
X2 = [310,220]
Y2 = [595,790]
leng = len(X)
leng2 = len(X2)
rot = []
rot2 = []
for i in range(leng):
    rot.append(random.randint(0,360))
    ##print(rot[i])
for i in range(leng2):
    rot2.append(random.randint(0,360))
    ##print(rot2[i])
    
one = Image.open("Base.png")
two = Image.open("Arm.png")
short = Image.open("BaseAwooga.png")
shorts = False

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

def exists(path):
    r = requests.head(path)
    return r.status_code == requests.codes.ok

def download(urll,gifProcess):
        r = requests.get(urll, allow_redirects=True)
        if gifProcess:
            open('whutt.gif', 'wb').write(r.content)
        else:
            open('whutt.png', 'wb').write(r.content)
        r.close()

bot = commands.Bot(command_prefix='!')

@bot.command(name='emoji')
async def nine_nine(ctx, test):
        start = test.find(":",3)+1
        stri2 = test[start:]
        stri3 = stri2[:-1]
        if stri3 == '681244980593164336':
            shorts = True
        else:
            shorts = False
        if shorts:
            one1 = short.copy()
        else:
            one1 = one.copy()
        two2 = two.copy()
        ##await ctx.send("https://cdn.discordapp.com/emojis/"+stri3+".png")
        url = "https://cdn.discordapp.com/emojis/"+stri3
        if exists(url+".gif"):
            gifProcess = True
            pog = download(url+".gif",gifProcess)  
        else:
            gifProcess = False
            pog = download(url+".png",gifProcess)
            pog = Image.open("whutt.png")
            ##pog.save("whatif.png")
        if gifProcess:
            images = []
            pog = Image.open("whutt.gif")
            ##pog.show()
            totalFrames = pog.n_frames
            gifDuration = pog.info['duration']
            if totalFrames < 91:
                for frame in range(0, totalFrames, 1):
                    onec = one.copy()
                    twoc = two.copy()
                    pogc = pog
                    pogc.seek(frame)    
                    pogc2 = pogc.copy().convert('RGBA')
                    ##pogc.show()
                    ##pogc2.show()
                    for i in range(leng):
                        ##print(i)
                        onec.alpha_composite(pogc2.resize((70,70), Image.LANCZOS).rotate(rot[i], Image.BICUBIC, expand=1),(X[i],Y[i]))
                    comp2 = Image.alpha_composite(onec,twoc)
                    for i in range(leng2):
                        ##print(i)
                        comp2.alpha_composite(pogc2.resize((70,70), Image.LANCZOS).rotate(rot2[i], Image.BICUBIC, expand=1),(X2[i],Y2[i]))
                    ##comp2.show()
                    print(frame)
                    images.append(comp2)
                images[0].save('CantHoldAllThese.gif', save_all=True, append_images=images[1:], duration=gifDuration, loop=0, optimize=True)
                optimize("CantHoldAllThese.gif")
                print(os.path.getsize('CantHoldAllThese.gif'))
                await ctx.channel.send(file=discord.File('CantHoldAllThese.gif'))
            else:
                await ctx.channel.send("Emoji too long")
        else:
            for i in range(leng):
                ##print(i)
                one1.alpha_composite(pog.resize((70,70), Image.LANCZOS).rotate(rot[i], Image.BICUBIC, expand=1),(X[i],Y[i]))
            comp2 = Image.alpha_composite(one1,two2)
            for i in range(leng2):
                comp2.alpha_composite(pog.resize((70,70), Image.LANCZOS).rotate(rot2[i], Image.BICUBIC, expand=1),(X2[i],Y2[i]))
            ##comp2.show()
            comp2.save('CantHoldAllThese.png')
            await ctx.channel.send(file=discord.File('CantHoldAllThese.png'))


bot.run(TOKEN)
