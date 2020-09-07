from PIL import Image, ImageFilter, GifImagePlugin, ImageSequence, ImageChops, ImageDraw, ImageEnhance, ImageOps
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
#from pygifsicle import optimize
from requests_toolbelt import MultipartEncoder
from io import BytesIO
from mcstatus import MinecraftServer
import datetime
##from imgurpython import ImgurClient


minecraftIP = 'minecraft.hackervoiceim.in:25565'
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

def getID(Input):
    try:
        idString = Input[Input.rfind(':')+1:-1]
    except:
        idString = Input
    return(idString)

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

async def processCrazyShookImage(context,emoPng,emojiId): #is this even used?
    images = []
    frames = 60-1
    ##img = Image.new('RGBA', (80,80), (0, 0 ,0 ,0))
    canvas = Image.open('canvas.png').resize((50,50))
    frequency = 3
    frequency2 = 6
    emoPng = emoPng.convert('RGBA')
    for i in range(0, frames, 1):
        ##canvas = img2.copy()
        ratio = emoPng.height/emoPng.width
        if emoPng.width > 50:
            image = emoPng.copy().resize((50,round(50*ratio)), Image.BICUBIC)
        else:
            image = emoPng.copy().resize((50,round(50*ratio)), Image.NEAREST)
        image = image.rotate(round(8*math.sin(((2*math.pi)/frequency)*(i-frequency))+(i*6)), Image.BICUBIC, expand=0)
        offsetX = round(2*0.8*math.sin(((2*math.pi)/frequency2)*(i-frequency2))+((i*50)/30))
        offsetY = round(2*0.2*math.sin(((2*math.pi)/frequency2)*(i-frequency2))+((i*50*ratio)/60))
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

async def processNukeImage(context,emoPng,emojiId):
    images = []
    frames = 240-1
    ##img = Image.new('RGBA', (160,160), (0, 0 ,0 ,0))
    canvas = Image.open('canvas.png')
    frequency = 3
    frequency2 = 6
    emoPng = emoPng.convert('RGBA')
    for i in range(0, frames, 1):
        mult = (i/287)*1.9+0.2
        if i > 159:
            endt = (i-160)
            exp = 3**(endt/12)-1
            if i==160:
                print(i, exp)
        else:
            exp = 0
            endt = 0
        ##canvas = img.copy()
        ratio = emoPng.height/emoPng.width
        if emoPng.width > 80:
            image = emoPng.copy().resize((80,round(80*ratio)), Image.BICUBIC)
        else:
            image = emoPng.copy().resize((80,round(80*ratio)), Image.NEAREST)
        image = image.rotate(round(mult*8*math.sin(((2*math.pi)/frequency)*(i-frequency))), Image.BICUBIC, expand=0)
        canvas.paste(image)
        image = canvas
        offsetX = round(mult*3*0.8*math.sin(((2*math.pi)/frequency2)*(i-frequency2)))
        offsetY = round(mult*3*0.2*math.sin(((2*math.pi)/frequency2)*(i-frequency2)))
        image2 = ImageChops.offset(image,offsetX,offsetY)
        croppedImage = image2.crop((0,0,80,round(80*ratio)))
        alpha = croppedImage.split()[3]
        cropL = croppedImage.load()
        if i > 159:
            expt = 1.3**(endt/20)-1
            for y in range(0,round(80*ratio),1):
                for x in range(0,80,1):
                    r,g,b,a = cropL[x,y]
                    rrat = (255-r)/80
                    grat = (255-g)/80
                    brat = (255-b)/80
                    rend = round(rrat*expt)+r if round(rrat*expt)+r < 255 else 255
                    gend = round(grat*expt)+g if round(grat*expt)+g < 255 else 255
                    bend = round(brat*expt)+b if round(brat*expt)+b < 255 else 255
                    if a > 0:
                        cropL[x,y] = (rend,gend,bend,255)
        croppedImage = ImageEnhance.Brightness(croppedImage).enhance(exp+1)
        ##croppedImage = croppedImage.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        croppedImage = croppedImage.convert('P', palette=Image.ADAPTIVE, colors=255)
        croppedImage.quantize(30)
        mask = Image.eval(alpha, lambda a: 255 if a <=128 else 0)
        croppedImage.paste(255, mask)
        images.append(croppedImage)
    images[0].save(emojiId+'nuke.gif', save_all=True, append_images=images[1:], duration=20, loop=0, optimize=False, transparency=255, disposal=2)
    await context.channel.send(file=discord.File(emojiId+'nuke.gif'))
    os.remove(emojiId+'nuke.gif')

async def processSpaceImage(context,emoPng,emojiId):
    images = []
    frames = 960-1
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
    interval = 240
    for i in range(0, frames, 1):
        if i == (interval):
            print('stage1')
            stage = 1
            X = 0
            Y = 0
        if i == (interval*2):
            print('stage2')
            stage = 2
            X = 0
            Y = 0
        if i == (interval*3):
            print('stage3')
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
        image = image.rotate(i*1*rotMul, Image.BICUBIC, expand=1)
        xOff = round((60-image.width)/2)
        yOff = round(((60*ratio)-image.height)/2)
        if i == 50:
            print(image.width)
        ##the below static number is 400 minus width then divided by 2
        canvas.alpha_composite(image,(170+xStart[stage]+xOff,170+yStart[stage]+yOff))
##        X -= xStart[stage]*0.02
##        Y -= yStart[stage]*0.02
        X -= xStart[stage]*0.01
        Y -= yStart[stage]*0.01
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
    images[0].save(emojiId+'space.gif', save_all=True, append_images=images[1:], duration=20, loop=0, optimize=False, transparency=255, disposal=2)
    ##optimize(emojiId+'space.gif')
    await context.channel.send(file=discord.File(emojiId+'space.gif'))
    os.remove(emojiId+'space.gif')

async def processSpaceGif(context,emoGif,emojiId):
    images = []
    frames = 960-1
    img2 = Image.open('canvas.png')
    frequency = 3
    frequency2 = 6
    xStart = []
    yStart = []
    dist = 100
    totalFrames = emoGif.n_frames
    gifDuration = emoGif.info['duration']
    if gifDuration < 20:
        gifDuration = 100
    frame_ratio = 20/gifDuration
    #emoPng = emoPng.convert('RGBA')
    for i in range(0, 4, 1):
        rotations = random.randint(0,360)*(math.pi/180)
        xStart.append(round(math.sin(rotations)*dist))
        yStart.append(round(math.cos(rotations)*dist))
    #print(xStart)
    #print(yStart)
    X = 0
    Y = 0
    stage = 0
    rotMul = 1
    interval = 240
    #print(totalFrames)
    for i in range(0, frames, 1):
        #print(i)
        #print(frame_ratio)
        framePick = int(math.floor((i*frame_ratio)%totalFrames))
        #print((i*frame_ratio)%totalFrames)
        emoGif.seek(framePick)
        emoPng = emoGif.copy().convert('RGBA')
        if i == (interval):
            #print('stage1')
            stage = 1
            X = 0
            Y = 0
        if i == (interval*2):
            #print('stage2')
            stage = 2
            X = 0
            Y = 0
        if i == (interval*3):
            #print('stage3')
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
        image = image.rotate(i*1*rotMul, Image.BICUBIC, expand=1)
        xOff = round((60-image.width)/2)
        yOff = round(((60*ratio)-image.height)/2)
        if i == 50:
            print(image.width)
        ##the below static number is 400 minus width then divided by 2
        canvas.alpha_composite(image,(170+xStart[stage]+xOff,170+yStart[stage]+yOff))
##        X -= xStart[stage]*0.02
##        Y -= yStart[stage]*0.02
        X -= xStart[stage]*0.01
        Y -= yStart[stage]*0.01
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
    images[0].save(emojiId+'space.gif', save_all=True, append_images=images[1:], duration=20, loop=0, optimize=False, transparency=255, disposal=2)
    ##optimize(emojiId+'space.gif')
    await context.channel.send(file=discord.File(emojiId+'space.gif'))
    os.remove(emojiId+'space.gif')
    
async def getId(emojiStr):
    idString = getID(emojiStr)
    url = "https://cdn.discordapp.com/emojis/"+idString
    gifProcess = exists(url+".gif")
    emojiValid = exists(url+".png")
    return idString, gifProcess, emojiValid


##client = discord.Client()
##@client.event
##async def on_message(message):
##    if message.author == client.user:
##        return
##    print(message.content)
##client.run(TOKEN)

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
        
##@bot.event
##async def on_message(message):
##    if message.content == 'F':
##        channel = message.channel
##        await channel.send("Is for friends who do stuff together")
##    if message.content == 'U':
##        channel = message.channel
##        await channel.send("Is for you and me")
##    if message.content == 'N':
##        channel = message.channel
##        await channel.send("Is for anywhere and anytime at all\nDown here in the deep blue sea!")
        
    
@bot.command(name='why')
async def fortheglory(context):
    ##glory = Image.open('forthegloryofsatan.jpg')
    await context.channel.send(file=discord.File('forthegloryofsatan.jpg'))
    

@bot.command(name='hold')
async def holding(ctx, emojiStr):
    ##print(emojiStr)
    idString = getID(emojiStr)
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
    idString = getID(emojiStr)
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

@bot.command(name='shook') #DONE
async def shooking(context, emojiStr):
    print(emojiStr)
    idString = getID(emojiStr)
    print(idString)
    channel = context.message.channel.id
    #output needs to be 3 args: channel, image id string, and command used
    os.system('python3 mstest.py '+str(channel)+' '+str(idString)+' shook')

@bot.command(name='moreshook')
async def moreshooking(context, emojiStr):
    idString = getID(emojiStr)
    url = "https://cdn.discordapp.com/emojis/"+idString
    gifProcess = exists(url+".gif")
    if not gifProcess and idString+'moreshook' in mydict:
        await ctx.channel.send("https://giant.gfycat.com/"+mydict[idString]+".webm") #these don't use webm hosts, deprecate these sometime
    elif not gifProcess:
        emojiImage = Image.open(grabImage(url))
        await processMoreShookImage(context,emojiImage,idString)
    else:
        await context.channel.send('Gif emoji not supported at this time. :-(')

@bot.command(name='nuke')
async def moreshooking(context, emojiStr):
    idString = getID(emojiStr)
    url = "https://cdn.discordapp.com/emojis/"+idString
    gifProcess = exists(url+".gif")
    if not gifProcess and idString+'nuke' in mydict:
        await ctx.channel.send("https://giant.gfycat.com/"+mydict[idString]+".webm")
    elif not gifProcess:
        emojiImage = Image.open(grabImage(url))
        await processNukeImage(context,emojiImage,idString)
    else:
        await context.channel.send('Gif emoji not supported at this time. :-(')

@bot.command(name='weee')
async def crazyshooking(context, emojiStr):
    idString = getID(emojiStr)
    url = "https://cdn.discordapp.com/emojis/"+idString
    gifProcess = exists(url+".gif")
    if not gifProcess and idString+'crazyshook' in mydict:
        await ctx.channel.send("https://giant.gfycat.com/"+mydict[idString]+".webm")
    elif not gifProcess:
        emojiImage = Image.open(grabImage(url))
        await processCrazyShookImage(context,emojiImage,idString)
    else:
        await context.channel.send('Gif emoji not supported at this time. :-(')

@bot.command(name='intense')
async def intensifytext(context, text, intensity):
    channel = context.message.channel.id
    os.system('python3 mstest.py '+str(channel)+' '+str(text)+' intense '+str(intensity))

@bot.command(name='space')
async def spacey(context, emojiStr):
    idString = getID(emojiStr)
    channel = context.message.channel.id
    #output needs to be 3 args: channel, image id string, and command used
    os.system('python3 mstest.py '+str(channel)+' '+str(idString)+' space')

@bot.command(name='shoot')
async def spacey(context, emojiStr):
    idString = getID(emojiStr)
    channel = context.message.channel.id
    #output needs to be 3 args: channel, image id string, and command used
    os.system('python3 mstest.py '+str(channel)+' '+str(idString)+' shoot')

@bot.command(name='italics') #DONE
async def italicize(context, emojiStr):
    idString = getID(emojiStr)
    channel = context.message.channel.id
    #output needs to be 3 args: channel, image id string, and command used
    os.system('python3 mstest.py '+str(channel)+' '+str(idString)+' italics')

@bot.command(name='jpeg') #DONE
async def Jpegify(context, emojiStr):
    idString = getID(emojiStr)
    channel = context.message.channel.id
    os.system('python3 mstest.py '+str(channel)+' '+str(idString)+' jpeg')

@bot.command(name='man') #DONE
async def DickMan(context, emojiStr):
    idString = getID(emojiStr)
    channel = context.message.channel.id
    os.system('python3 mstest.py '+str(channel)+' '+str(idString)+' man')

@bot.command(name='jpeg2') #DONE
async def Jpegify2(context, *, message):
    if message != None:
        args = list(message.split(" "))
    validLen = False
    if len(args) == 1 or len(args) == 2:
        validLen = True
    emojiStr = args[0]
    idString = getID(emojiStr)
    if validLen:
        try:
            args[1] = int(args[1])
            if int(args[1]) > 20:
                args[1] = 20
                await context.channel.send('Capped at 20')
            times = args[1]
            channel = context.message.channel.id
            os.system('python3 mstest.py '+str(channel)+' '+str(idString)+' jpeg2 '+str(times))
        except:
            await context.channel.send('Entry in [1] not an int')
    else:
        await context.channel.send('Invalid Number of Args')

@bot.command(name='jpeg3') #DONE
async def Jpegify3(context, *, message):
    print(message)
    if message != None:
        args = list(message.split(" "))
    validLen = False
    if len(args) == 1 or len(args) == 2:
        validLen = True
    emojiStr = args[0]
    idString = getID(emojiStr)
    url = "https://cdn.discordapp.com/emojis/"+idString
    if validLen:
        try:
            args[1] = int(args[1])
            if int(args[1]) > 20:
                args[1] = 20
                await context.channel.send('Capped at 20')
            gifProcess = exists(url+".gif")
            times = args[1]
            channel = context.message.channel.id
            os.system('python3 mstest.py '+str(channel)+' '+str(idString)+' jpeg3 '+str(times))
        except:
            await context.channel.send('Entry in [1] not an int')
    else:
        await context.channel.send('Invalid Number of Args')
    
@bot.command(name='boys')
async def boysOnline(context):
    try:
        server = MinecraftServer.lookup(minecraftIP)
        status = server.status()
        await context.channel.send("There are {0} boys online, query took {1} ms".format(status.players.online, status.latency))
        if status.players.online > 0:
            query = server.query()
            await context.channel.send("The following boys are online: {0}".format(", ".join(query.players.names)))
    except:
        await context.channel.send("Error")

@bot.command(name='listboys')
async def boysList(context):
    server = MinecraftServer.lookup(minecraftIP)
    query = server.query()
    await context.channel.send("The following boys are online: {0}".format(", ".join(query.players.names)))

@bot.command(name='conch')
async def magicConch(context):
    conchAnswers = ['As I see it, yes.','Ask again later.','Better not tell you now.','Cannot predict now.','Concentrate and ask again.','Don\'t count on it.','It is certain.','It is decidedly so.','Most likely.','My reply is no.','My sources say no.','Outlook not so good.','Outlook good.','Reply hazy, try again.','Signs point to yes.','Very doubtful.','Without a doubt.','Yes.','Yes - definitely.','You may rely on it.']
    answer = random.randint(0,19)
    await context.channel.send(":shell:"+conchAnswers[answer])
    
@bot.command(name='bank')
async def slotMachine(context):
    currentTime = datetime.datetime.now()
    UID = str(context.message.author.id)
    #accumulateCash(UID)
    ##await context.channel.send("User has gained $"+str(accumulateCash(UID))+" since last updated"+"\nUser has $"+str(userdict[UID][2]))
    channel = context.message.channel.id
    os.system('python3 mstest.py '+str(channel)+' '+str(UID)+' bank')
    ##await context.channel.send("user has $"+str(userdict[UID][2]))

@bot.command(name='slots')
async def slotMachine(context, *, message):
    slotsArr = [':gem:',':moneybag:',':four_leaf_clover:',':grapes:',':watermelon:',':cherries:',':banana:',':lemon:']
    bet = 8
    returns = 0
    totalReturns = 0
    jackpot = False
    currentTime = datetime.datetime.now()
    UID = str(context.message.author.id)
    try:
        NumTries = int(message)
        if NumTries > 10:
            NumTries = 10
    except:
        NumTries = 1
    channel = context.message.channel.id
    os.system('python3 mstest.py '+str(channel)+' '+str(NumTries)+' slots '+str(UID))

    
@bot.command(name='loan')
async def loan(context,amnt):
    UID = str(context.message.author.id)
    try:
        amnt = int(amnt)
        if str(UID) == "95630487023779840":
            addCash(UID,amnt)
            await context.channel.send(str(amnt)+" added")
        else:
            await context.channel.send("Unprivileged User")
    except:
        await context.channel.send("Error")

@bot.command(name='overlay')
async def overlaying(context, *, message):
    overlays = ['hazmat', 'mask', 'hazmatf']
    noneValid = False
    isGif = False
    if message != None:
        args = list(message.split(" "))
    validLen = False
    if len(args) == 2 or len(args) == 6:
        validLen = True
    if message != None and validLen:
        concatId, isGif, isValid = await getId(args[0])
        if not isValid:
            concatId, isGif, isValid = await getId(args[1])
            arg2 = args[0]
            if not isValid:
                noneValid = True
        else:
            arg2 = args[1]
        if not noneValid and not isGif:
            if arg2 in overlays:
                #url = "https://cdn.discordapp.com/emojis/"+concatId
                #emojiImage = Image.open(grabImage(url))
                if len(args) == 6:
                    ex = int(args[2])
                    ey = int(args[3])
                    roto = float(args[4])
                    scale = float(args[5])
                else:
                    ex = 0
                    ey = 0
                    roto = 0
                    scale = 1
                #await notBttv(context, emojiImage, concatId, arg2, ex, ey, roto, scale)
                channel = context.message.channel.id
                os.system('python3 mstest.py '+str(channel)+' '+str(concatId)+' overlay '+str(arg2)+' '+str(ex)+' '+str(ey)+' '+str(roto)+' '+str(scale))
            else:
                await context.channel.send('Valid overlays are: hazmat, mask')
    if message == None or noneValid or validLen == False:
        await context.channel.send('Valid overlays are: hazmat, mask')
        await context.channel.send('Proper format is !overlay <emote> <overlay> [x offset] [y offset] [rotation in degrees] [scale as a mult of 1]')
        await context.channel.send('Arguments in [] are optional, but must be used all at once if used')
    if isGif:
        await context.channel.send('Gif emoji not supported')
    ##await context.channel.send(message)
        
@bot.command(name='read')
async def reading(context, *, message):
    await context.channel.send(message)

@bot.command(name='I')
async def iguess(context, *, message):
    if message == 'guess':
        ##await context.channel.send(file=discord.File('iguess.gif'))
        await context.channel.send('https://i.imgur.com/MMaciGr.gif')

@bot.command(name='God')
async def doyouthink(context):
    await context.channel.send('http://pockisho.net/albums/DoYouThink/DoYouThink.webm')

@bot.command(name='mst')
async def mst(context):
    guild = context.message.guild.id
    channel = context.message.channel.id
    #channel2 = bot.get_channel(channel)
    print(guild,channel)
    os.system('python3 mstest.py '+str(channel))
    #await channel2.send('test')

@bot.command(name='buildstart')
async def bst(context):
    UID = str(context.message.author.id)
    channel = context.message.channel.id
    os.system('python3 mstest.py '+str(channel)+' '+UID+' '+'buildstart')

@bot.command(name='simtest')
async def sts(context):
    UID = str(context.message.author.id)
    channel = context.message.channel.id
    os.system('python3 mstest.py '+str(channel)+' '+UID+' '+'simtest')

bot.run(TOKEN)
