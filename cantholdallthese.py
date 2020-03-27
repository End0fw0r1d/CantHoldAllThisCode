from PIL import Image, ImageFilter, GifImagePlugin, ImageSequence, ImageChops, ImageDraw
import os, glob, time, asyncio
import math, random
import io
import discord
import requests
import json
import ftplib
##import moviepy.editor as mp##dont think I need anymore
from discord.ext import commands
from discord.ext.commands import Bot
from discord import Emoji
from discord import File
from dotenv import load_dotenv
from pygifsicle import optimize
from requests_toolbelt import MultipartEncoder
from io import BytesIO
##from imgurpython import ImgurClient

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

mydict = {}
with open('mydict.json') as json_file:
    mydict = json.load(json_file)

def exists(path):
    r = requests.head(path)
    return r.status_code == requests.codes.ok

def grabImage(urll): ##if you direct link to a png/gif/etc, it will directly return it as a bytestream of the image
    r = requests.get(urll, allow_redirects=True)
    return io.BytesIO(r.content)
    r.close()
##Imgur upload stuff below
##def authenticateImgur():
##	client_id = os.getenv('IMGUR_API_ID')
##	client_secret = os.getenv('IMGUR_API_SECRET')
##	client = ImgurClient(client_id, client_secret)

##	# Authorization flow, pin example (see docs for other auth types)
####	authorization_url = client.get_auth_url('pin')
##
####	print("Go to the following URL: {0}".format(authorization_url))
##
##	# Read in the pin, handle Python 2 or 3 here.
####	pin = input("Enter pin code: ")
##
##	# ... redirect user to `authorization_url`, obtain pin (or code or token) ...
####	credentials = client.authorize(pin, 'pin')
####	client.set_user_auth(credentials['access_token'], credentials['refresh_token'])
##	access_token = os.getenv('ACCESS_TOKEN')
##	refresh_token = os.getenv('REFRESH_TOKEN')
##	client.set_user_auth(access_token, refresh_token)
##
####	print("Authentication successful! Here are the details:")
####	print("   Access token:  {0}".format(credentials['access_token']))
####	print("   Refresh token: {0}".format(credentials['refresh_token']))
##
##	return client

##def upload_png(gif):
##    client_id = os.getenv('IMGUR_API_ID')
##    client_secret = os.getenv('IMGUR_API_SECRET')
##    if client_id is None or client_secret is None:
##        print('Cannot upload - could not find IMGUR_API_ID or IMGUR_API_SECRET environment variables')
##        return
##    ##client = ImgurClient(client_id, client_secret)
##    client = authenticateImgur()
##    print("wee")
##    response = client.upload_from_path(gif, anon=False)
##    text = ('File uploaded: {}'.format(response['link']))
##    return text

def get_token():
    payload = {
    'grant_type':"password",
    'client_id':os.getenv('GFYCAT_CLIENT_ID'),
    'client_secret':os.getenv('GFYCAT_CLIENT_SECRET'),
    'username':os.getenv('GFYCAT_USERNAME'),
    'password':os.getenv('GFYCAT_PASSWORD')
    }

    url = "https://api.gfycat.com/v1/oauth/token"
    r = requests.post(url, data=str(payload), headers={'User-Agent': "Slow down bot"})

    response = r.json()

    access_token = response["access_token"]
    print(access_token)
    return access_token

def upload_gfy(emoteId,which):
    print("uploading")
    title = "github.com/End0fw0r1d/CantHoldAllThisCode"
    # get gfyname
    url = "https://api.gfycat.com/v1/gfycats"
    headers = {"Authorization": "Bearer " + get_token(), 'User-Agent': "Slow down bot",
                'Content-Type': 'application/json'}
    params = {}
    if title:
        params["title"] = title
    r = requests.post(url, headers=headers, data=str(params))
    print(r.text)
    metadata = r.json()
    url = "https://filedrop.gfycat.com"
    with open(emoteId+".gif", 'rb') as f:
        files = {"key": metadata["gfyname"], "file": (metadata["gfyname"], f, "video/mp4")}
        m = MultipartEncoder(fields=files)
        r = requests.post(url, data=m, headers={'Content-Type': m.content_type, 'User-Agent': "Slowing down gifs"})
    url = "https://api.gfycat.com/v1/gfycats/fetch/status/" + metadata["gfyname"]
    headers = {'User-Agent': "Slowing down gifs"}
    print("waiting for encode...", end=" ")
    time.sleep(2)
    os.remove(emoteId+'.gif')
    r = requests.get(url, headers=headers)
    ticket = r.json()
    print(ticket)
    print(url)
    print(metadata["gfyname"])
    mydict[emoteId+which] = metadata["gfyname"]
    with open('mydict.json', 'w') as outfile:
        json.dump(mydict, outfile)
    # Sometimes we have to wait
    percentage = 0
    for i in range(457):
        if ticket["task"] == "encoding":
            time.sleep(4)
            r = requests.get(url, headers=headers)
            ticket = r.json()
            print(ticket)
            if float(ticket.get('progress', 0)) > percentage:
                percentage = float(ticket['progress'])
                print(percentage, end=" ")
            else:
                break
    # os.system('rm temp/slow-{}.mp4'.format(sub_id))
    return metadata["gfyname"]


async def processStaticImage(context,emoPng,emojiId):
    one1 = Image.open("Base.png").copy() if emojiId != '681244980593164336' else Image.open("BaseAwooga.png").copy()
    two1 = Image.open("Arm.png").copy()
    wRatio = emoPng.width/emoPng.height
    ## w*h = a, a = 4900, w = wR*h, (wR*h)*h = a, wR*h^2 = a
    height = round(math.sqrt(4900/wRatio))
    width = round(wRatio*height)
    for i in range(leng):
        one1.alpha_composite(emoPng.resize((width,height), Image.LANCZOS).rotate(rot[i], Image.BICUBIC, expand=1),(X[i],Y[i]))
    comp2 = Image.alpha_composite(one1,two1)
    for i in range(leng2):
        comp2.alpha_composite(emoPng.resize((width,height), Image.LANCZOS).rotate(rot2[i], Image.BICUBIC, expand=1),(X2[i],Y2[i]))
    comp2.save(emojiId+'.png', format='PNG')
    await context.channel.send(file=discord.File(emojiId+'.png',filename="CantHoldAllThese.png"))
    os.remove(emojiId+'.png')


async def processGifImage(context,emoGif,emojiId,rando):
    one1 = Image.open("Base.png").copy()
    two2 = Image.open("Arm.png").copy()
    images = []
    Offset1 = []
    Offset2 = []
    totalFrames = emoGif.n_frames
    gifDuration = emoGif.info['duration']
    wRatio = emoGif.width/emoGif.height
    ## w*h = a, a = 4900, w = wR*h, (wR*h)*h = a, wR*h^2 = a
    height = round(math.sqrt(4900/wRatio))
    width = round(wRatio*height)
    for i in range(0, 7, 1):
        Offset1.append(random.randint(0,totalFrames*rando))
    for i in range(0, 2, 1):
        Offset2.append(random.randint(0,totalFrames*rando))
    if totalFrames < 200:
        for frame in range(0, totalFrames, 1):
            onec = one1.copy()
            twoc = two2.copy()
            for i in range(leng):
                newframe = frame + Offset1[i]
                if newframe >= totalFrames:
                    newframe = newframe - totalFrames
                emoGif.seek(newframe)
                emoFrame = emoGif.copy().convert('RGBA')
                onec.alpha_composite(emoFrame.resize((width,height), Image.LANCZOS).rotate(rot[i], Image.BICUBIC, expand=1),(X[i],Y[i]))
            comp2 = Image.alpha_composite(onec,twoc)
            for i in range(leng2):
                newframe = frame + Offset2[i]
                if newframe >= totalFrames:
                    newframe = newframe - totalFrames
                emoGif.seek(newframe)
                emoFrame = emoGif.copy().convert('RGBA')
                comp2.alpha_composite(emoFrame.resize((width,height), Image.LANCZOS).rotate(rot2[i], Image.BICUBIC, expand=1),(X2[i],Y2[i]))
            images.append(comp2)
        images[0].save(emojiId+'.gif', save_all=True, append_images=images[1:], duration=gifDuration, loop=0, optimize=True)
        optimize(emojiId+'.gif')
        which = 'rand' if rando else ''
        await context.channel.send("https://giant.gfycat.com/"+upload_gfy(emojiId,which)+".webm")
        ##await ctx.channel.send(file=discord.File('CantHoldAllThese.gif'))
    else:
        await context.channel.send("Emoji too long")

async def processShookImage(context,emoPng,emojiId):
    images = []
    frames = 24-1
    ##img = Image.new('RGBA', (80,80), (0, 0 ,0 ,0))
    canvas = Image.open('canvas.png')
    frequency = 3
    frequency2 = 6
    emoPng = emoPng.convert('RGBA')
    for i in range(0, frames, 1):
        ##canvas = img2.copy()
        ratio = emoPng.height/emoPng.width
        if emoPng.width > 80:
            image = emoPng.copy().resize((80,round(80*ratio)), Image.BICUBIC)
        else:
            image = emoPng.copy().resize((80,round(80*ratio)), Image.NEAREST)
        image = image.rotate(round(4*math.sin(((2*math.pi)/frequency)*(i-frequency))), Image.BICUBIC, expand=0)
        canvas.paste(image)
        image = canvas
        offsetX = round(1*0.8*math.sin(((2*math.pi)/frequency2)*(i-frequency2)))
        offsetY = round(1*0.2*math.sin(((2*math.pi)/frequency2)*(i-frequency2)))
        image2 = ImageChops.offset(image,offsetX,offsetY)
        croppedImage = image2.crop((0,0,80,80))
        alpha = croppedImage.split()[3]
        croppedImage = croppedImage.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <=128 else 0)
        croppedImage.paste(255, mask)
        images.append(croppedImage)
    images[0].save(emojiId+'shook.gif', save_all=True, append_images=images[1:], duration=20, loop=0, optimize=False, transparency=255, disposal=2)
    ##optimize(emojiId+'shook.gif')
    await context.channel.send(file=discord.File(emojiId+'shook.gif'))
    os.remove(emojiId+'shook.gif')

async def processMoreShookImage(context,emoPng,emojiId):
    images = []
    frames = 24-1
    ##img = Image.new('RGBA', (80,80), (0, 0 ,0 ,0))
    canvas = Image.open('canvas.png')
    frequency = 3
    frequency2 = 6
    emoPng = emoPng.convert('RGBA')
    for i in range(0, frames, 1):
        ##canvas = img2.copy()
        ratio = emoPng.height/emoPng.width
        if emoPng.width > 80:
            image = emoPng.copy().resize((80,round(80*ratio)), Image.BICUBIC)
        else:
            image = emoPng.copy().resize((80,round(80*ratio)), Image.NEAREST)
        image = image.rotate(round(8*math.sin(((2*math.pi)/frequency)*(i-frequency))), Image.BICUBIC, expand=0)
        canvas.paste(image)
        image = canvas
        offsetX = round(2*0.8*math.sin(((2*math.pi)/frequency2)*(i-frequency2)))
        offsetY = round(2*0.2*math.sin(((2*math.pi)/frequency2)*(i-frequency2)))
        image2 = ImageChops.offset(image,offsetX,offsetY)
        croppedImage = image2.crop((0,0,80,80))
        alpha = croppedImage.split()[3]
        croppedImage = croppedImage.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <=128 else 0)
        croppedImage.paste(255, mask)
        images.append(croppedImage)
    images[0].save(emojiId+'moreshook.gif', save_all=True, append_images=images[1:], duration=20, loop=0, optimize=False, transparency=255, disposal=2)
    ##optimize(emojiId+'moreshook.gif')
    await context.channel.send(file=discord.File(emojiId+'moreshook.gif'))
    os.remove(emojiId+'moreshook.gif')

async def processCrazyShookImage(context,emoPng,emojiId):
    images = []
    frames = 60-1
    ##img = Image.new('RGBA', (80,80), (0, 0 ,0 ,0))
    canvas = Image.open('canvas.png')
    frequency = 3
    frequency2 = 6
    emoPng = emoPng.convert('RGBA')
    for i in range(0, frames, 1):
        ##canvas = img2.copy()
        ratio = emoPng.height/emoPng.width
        if emoPng.width > 80:
            image = emoPng.copy().resize((80,round(80*ratio)), Image.BICUBIC)
        else:
            image = emoPng.copy().resize((80,round(80*ratio)), Image.NEAREST)
        image = image.rotate(round(8*math.sin(((2*math.pi)/frequency)*(i-frequency))+(i*6)), Image.BICUBIC, expand=0)
        offsetX = round(2*0.8*math.sin(((2*math.pi)/frequency2)*(i-frequency2))+((i*80)/30))
        offsetY = round(2*0.2*math.sin(((2*math.pi)/frequency2)*(i-frequency2))+((i*80*ratio)/60))
        image2 = ImageChops.offset(image,offsetX,offsetY)
        croppedImage = image2
        alpha = croppedImage.split()[3]
        croppedImage = croppedImage.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <=128 else 0)
        croppedImage.paste(255, mask)
        images.append(croppedImage)
    images[0].save(emojiId+'crazyshook.gif', save_all=True, append_images=images[1:], duration=20, loop=0, optimize=False, transparency=255, disposal=2)
    ##optimize(emojiId+'crazyshook.gif')
    await context.channel.send(file=discord.File(emojiId+'crazyshook.gif'))
    os.remove(emojiId+'crazyshook.gif')

async def processSpaceImage(context,emoPng,emojiId):
    images = []
    frames = 480-1
    img2 = Image.open('canvas.png')
    frequency = 3
    frequency2 = 6
    xStart = []
    yStart = []
    dist = 100
    emoPng = emoPng.convert('RGBA')
    for i in range(0, 4, 1):
        rotations = random.randint(0,360)*(math.pi/180)
        xStart.append(round(math.sin(rotations)*dist))
        yStart.append(round(math.cos(rotations)*dist))
    print(xStart)
    print(yStart)
    X = 0
    Y = 0
    stage = 0
    rotMul = 1
    interval = 120
    for i in range(0, frames, 1):
        if i == (interval):
            stage = 1
            X = 0
            Y = 0
        if i == (interval*2):
            stage = 2
            X = 0
            Y = 0
        if i == (interval*3):
            stage = 3
            X = 0
            Y = 0
            rotMul = 3
        canvas = img2.copy()
        ratio = emoPng.height/emoPng.width
        if emoPng.width > 60:
            image = emoPng.copy().resize((60,round(60*ratio)), Image.BICUBIC)
        else:
            image = emoPng.copy().resize((60,round(60*ratio)), Image.NEAREST)
        image = image.rotate(i*2*rotMul, Image.BICUBIC, expand=1)
        xOff = round((60-image.width)/2)
        yOff = round(((60*ratio)-image.height)/2)
        if i == 50:
            print(image.width)
        ##the below static number is 400 minus width then divided by 2
        canvas.alpha_composite(image,(170+xStart[stage]+xOff,170+yStart[stage]+yOff))
        X -= xStart[stage]*0.02
        Y -= yStart[stage]*0.02
        ##canvas.alpha_composite(image,(160,160))
        offsetX = round(X)
        offsetY = round(Y)
        image2 = ImageChops.offset(canvas,offsetX,offsetY)
        croppedImage = image2.crop((160,160,240,240))
        ##croppedImage = image2.crop((0,0,400,400))
        alpha = croppedImage.split()[3]
        croppedImage = croppedImage.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <=128 else 0)
        croppedImage.paste(255, mask)
        images.append(croppedImage)
    images[0].save(emojiId+'space.gif', save_all=True, append_images=images[1:], duration=40, loop=0, optimize=False, transparency=255, disposal=2)
    ##optimize(emojiId+'space.gif')
    await context.channel.send(file=discord.File(emojiId+'space.gif'))
    os.remove(emojiId+'space.gif')

##client = discord.Client()
##@client.event
##async def on_message(message):
##    if message.author == client.user:
##        return
##    print(message.content)
##client.run(TOKEN)

bot = commands.Bot(command_prefix='!')

@bot.command(name='hold')
async def holding(ctx, emojiStr):
    ##print(emojiStr)
    idString = emojiStr[emojiStr.find('<'):]
    lookStart = emojiStr.find(":",3)+1
    idString = idString[lookStart:][:-1]
    shorts = True if idString == '681244980593164336' else False
    url = "https://cdn.discordapp.com/emojis/"+idString
    gifProcess = exists(url+".gif")
    if gifProcess and idString in mydict:
        await ctx.channel.send("https://giant.gfycat.com/"+mydict[idString]+".webm")
    elif gifProcess:
        emojiImage = Image.open(grabImage(url))
        await processGifImage(ctx,emojiImage,idString,False)
    else:
        emojiImage = Image.open(grabImage(url)).convert('RGBA')
        await processStaticImage(ctx,emojiImage,idString)
        

@bot.command(name='shake')
async def shaking(ctx, emojiStr):
    idString = emojiStr[emojiStr.find('<'):]
    lookStart = emojiStr.find(":",3)+1
    idString = idString[lookStart:][:-1]
    url = "https://cdn.discordapp.com/emojis/"+idString
    gifProcess = exists(url+".gif")
    if gifProcess and idString+'rand' in mydict:
        await ctx.channel.send("https://giant.gfycat.com/"+mydict[idString+'rand']+".webm")
    elif gifProcess:
        emojiImage = Image.open(grabImage(url))
        await processGifImage(ctx,emojiImage,idString,True)
    else:
        emojiImage = Image.open(grabImage(url)).convert('RGBA')
        await processStaticImage(ctx,emojiImage,idString)

@bot.command(name='wide')
async def widening(context, *, content):
    print(content)
    contents = content.split(">")
    print(contents)
    length = len(contents)
    for i in range(length):
        contents[i] = contents[i][contents[i].find('<'):]
        lookStart = contents[i].find(":",4)+1
        contents[i] = contents[i][lookStart:]
        if len(contents[i]) < 2:
            del contents[i]
    print(contents)
    length = len(contents)-1
    one1 = Image.open("Base.png").copy()
    two1 = Image.open("Arm.png").copy()
    ## w*h = a, a = 4900, w = wR*h, (wR*h)*h = a, wR*h^2 = a
    for i in range(leng):
        url = "https://cdn.discordapp.com/emojis/"+contents[random.randint(0,length)]+'.png'
        print(url)
        emoPng = Image.open(grabImage(url))
        wRatio = emoPng.width/emoPng.height
        height = round(math.sqrt(4900/wRatio))
        width = round(wRatio*height)
        one1.alpha_composite(emoPng.resize((width,height), Image.LANCZOS).rotate(rot[i], Image.BICUBIC, expand=1),(X[i],Y[i]))
    comp2 = Image.alpha_composite(one1,two1)
    for i in range(leng2):
        url = "https://cdn.discordapp.com/emojis/"+contents[random.randint(0,length)]+'.png'
        emoPng = Image.open(grabImage(url))
        wRatio = emoPng.width/emoPng.height
        height = round(math.sqrt(4900/wRatio))
        width = round(wRatio*height)
        comp2.alpha_composite(emoPng.resize((width,height), Image.LANCZOS).rotate(rot2[i], Image.BICUBIC, expand=1),(X2[i],Y2[i]))
    file = ''.join(contents)
    print(contents)
    comp2.save(file+'.png', format='PNG')
    await context.channel.send(file=discord.File(file+'.png',filename="CantHoldAllThese.png"))
    os.remove(file+'.png')

@bot.command(name='shook')
async def shooking(context, emojiStr):
    idString = emojiStr[emojiStr.find('<'):]
    lookStart = emojiStr.find(":",3)+1
    idString = idString[lookStart:][:-1]
    url = "https://cdn.discordapp.com/emojis/"+idString
    gifProcess = exists(url+".gif")
    if not gifProcess and idString+'shook' in mydict:
        await ctx.channel.send("https://giant.gfycat.com/"+mydict[idString]+".webm")
    elif not gifProcess:
        emojiImage = Image.open(grabImage(url))
        await processShookImage(context,emojiImage,idString)
    else:
        await context.channel.send('Gif emoji not supported at this time. :-(')

@bot.command(name='moreshook')
async def moreshooking(context, emojiStr):
    idString = emojiStr[emojiStr.find('<'):]
    lookStart = emojiStr.find(":",3)+1
    idString = idString[lookStart:][:-1]
    url = "https://cdn.discordapp.com/emojis/"+idString
    gifProcess = exists(url+".gif")
    if not gifProcess and idString+'moreshook' in mydict:
        await ctx.channel.send("https://giant.gfycat.com/"+mydict[idString]+".webm")
    elif not gifProcess:
        emojiImage = Image.open(grabImage(url))
        await processMoreShookImage(context,emojiImage,idString)
    else:
        await context.channel.send('Gif emoji not supported at this time. :-(')

@bot.command(name='weee')
async def crazyshooking(context, emojiStr):
    idString = emojiStr[emojiStr.find('<'):]
    lookStart = emojiStr.find(":",3)+1
    idString = idString[lookStart:][:-1]
    url = "https://cdn.discordapp.com/emojis/"+idString
    gifProcess = exists(url+".gif")
    if not gifProcess and idString+'crazyshook' in mydict:
        await ctx.channel.send("https://giant.gfycat.com/"+mydict[idString]+".webm")
    elif not gifProcess:
        emojiImage = Image.open(grabImage(url))
        await processCrazyShookImage(context,emojiImage,idString)
    else:
        await context.channel.send('Gif emoji not supported at this time. :-(')

@bot.command(name='space')
async def spacey(context, emojiStr):
    idString = emojiStr[emojiStr.find('<'):]
    lookStart = emojiStr.find(":",3)+1
    idString = idString[lookStart:][:-1]
    url = "https://cdn.discordapp.com/emojis/"+idString
    gifProcess = exists(url+".gif")
    if not gifProcess and idString+'space' in mydict:
        await ctx.channel.send("https://giant.gfycat.com/"+mydict[idString]+".webm")
    elif not gifProcess:
        emojiImage = Image.open(grabImage(url))
        await processSpaceImage(context,emojiImage,idString)
    else:
        await context.channel.send('Gif emoji not supported at this time. :-(')
        
##@bot.command(name='wide3')
##async def widening2(context, *, content):
##    print(content)
##    contents = content.split(">")
##    contentsImages = []
##    endFrame = []
##    durations = []
##    gifDuration = 0
##    maxFrame = 0;
##    images = []
##    length = len(contents)
##    for i in range(length):
##        contents[i] = contents[i][contents[i].find('<'):]
##        lookStart = contents[i].find(":",4)+1
##        contents[i] = contents[i][lookStart:]
##        if len(contents[i]) < 2:
##            del contents[i]
##    length = len(contents)-1
##    for i in range(len(contents)):
##        url = "https://cdn.discordapp.com/emojis/"+contents[i]
##        print(url)
##        contentsImages.append(Image.open(grabImage(url)))
##        if exists(url+".gif"):
####            print(contentsImages[i].info)
####            print(contentsImages[i].n_frames)
####            print('prior url is gif')
##            endFrame.append(contentsImages[i].n_frames)
##            if contentsImages[i].info['duration'] == 0:
##                durations.append(15*contentsImages[i].n_frames)
##            else:
##                durations.append(contentsImages[i].info['duration'])
##        else:
##            print('prior url is not gif')
##            endFrame.append(1)
##            durations.append(1)
##        if gifDuration < durations[i]:
##            gifDuration = durations[i]
##        if maxFrame < (endFrame[i]):
##            maxFrame = endFrame[i]
##    one1 = Image.open("Base.png").copy()
##    two1 = Image.open("Arm.png").copy()
##    maxFrame = (maxFrame*2)
##    set1 = []
##    set2 = []
##    for i in range(0, 7, 1):
##        set1.append(contentsImages[i])
##        print(i)
##    for i in range(0, 2, 1):
##        set2.append(contentsImages[i+6])
##        print(i+6)
##    ## w*h = a, a = 4900, w = wR*h, (wR*h)*h = a, wR*h^2 = a
##    for frame in range(0, maxFrame, 1):
##        ##print(frame)
##        one1 = Image.open("Base.png").copy()
##        for i in range(leng):
##            ##numb of playbacks is a rounded of max duration divided by duration, rounded to be a whole number
##            ##max frame of single is total frames divided by number of playbacks to be done, rounded because ints only
##            ##frame progress is ratio times progress through total; ratio being total frames of gif times playbacks to be done, divided by max or somthn
##            testRatio = maxFrame/(endFrame[i]*2) if endFrame[i] > 0 else 1
##            print(endFrame[i])
##            print(durations[i])
##            currentFrame = math.floor(testRatio*(frame/(gifDuration/durations[i])))
##            print('part 1:'+str(i))
##            emoGif = set1[i]
##            emoGif.seek(currentFrame%endFrame[i])
##            emoPng = emoGif.copy().convert('RGBA')
##            wRatio = emoPng.width/emoPng.height
##            height = round(math.sqrt(4900/wRatio))
##            width = round(wRatio*height)
##            one1.alpha_composite(emoPng.resize((width,height), Image.LANCZOS).rotate(rot[i], Image.BICUBIC, expand=1),(X[i],Y[i]))
##        comp2 = Image.alpha_composite(one1,two1)
##        for i in range(leng2):
##            currentFrame = math.floor((maxFrame/(endFrame[i]*2))*(frame/(gifDuration/durations[i])))
##            print('part2:'+str(i))
##            emoGif = set2[i]
##            if i == 2:
##                print(currentFrame)
##                print(endFrame[i])
##            emoGif.seek(currentFrame%endFrame[i])
##            emoPng = emoGif.copy().convert('RGBA')
##            wRatio = emoPng.width/emoPng.height
##            height = round(math.sqrt(4900/wRatio))
##            width = round(wRatio*height)
##            comp2.alpha_composite(emoPng.resize((width,height), Image.LANCZOS).rotate(rot2[i], Image.BICUBIC, expand=1),(X2[i],Y2[i]))
##        images.append(comp2)
##    file = ''.join(contents)
##    images[0].save(file+'.gif', save_all=True, append_images=images[1:], duration=gifDuration, loop=0, optimize=True)
##    optimize(file+'.gif')
##    await context.channel.send(file=discord.File(file+'.gif'))


@bot.command(name='read')
async def reading(context, *, message):
    await context.channel.send(message)
        


bot.run(TOKEN)
