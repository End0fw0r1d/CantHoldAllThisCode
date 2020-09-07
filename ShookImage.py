from PIL import Image, ImageFilter, GifImagePlugin, ImageSequence, ImageChops, ImageDraw, ImageEnhance, ImageOps
import os, glob, time, asyncio
import math, random

def processShookImage(emoPng,emojiId):
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
    images[0].save(str(emojiId)+'shook.gif', save_all=True, append_images=images[1:], duration=20, loop=0, optimize=False, transparency=255, disposal=2)
    return (str(emojiId)+'shook.gif')
    ##optimize(emojiId+'shook.gif')
    #await context.channel.send(file=discord.File(emojiId+'shook.gif'))
    #os.remove(emojiId+'shook.gif')
