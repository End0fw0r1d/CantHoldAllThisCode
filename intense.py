from PIL import Image, ImageFilter, GifImagePlugin, ImageFont, ImageSequence, ImageChops, ImageDraw, ImageEnhance, ImageOps
import os, glob, time, asyncio
import math, random

def intensifytext(inputText, intensity, red, blue, green, emojiId):
    canv = Image.open('canvas.png').resize((800,100))
    d1 = ImageDraw.Draw(canv)
    myFont = ImageFont.truetype('font/whitney-semibold.otf',30)
    d1.text((0,0),inputText, font=myFont, fill=(red,blue,green), align='center')
    xd, yd = myFont.getsize(inputText)
    canv = canv.crop((0,0,xd,yd))
    images = []
    frames = 24-1
    frequency = 4
    frequency2 = 3
    canvas = Image.open('canvas.png').resize((xd+50,yd+50))
    for i in range(0, frames, 1):
        image = canv
        canvas.paste(image)
        image = canvas
        offsetX = round(math.sin(((2*math.pi)/frequency2)*(i-frequency2)))*intensity
        offsetY = round(math.sin(((2*math.pi)/frequency)*(i-frequency)))*intensity
        image2 = ImageChops.offset(image,offsetX,offsetY)
        croppedImage = image2.crop((0,0,xd,(yd+15)))
        alpha = croppedImage.split()[3]
        croppedImage = croppedImage.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <=128 else 0)
        croppedImage.paste(255, mask)
        images.append(croppedImage)
    images[0].save(emojiId+'intense.gif', save_all=True, append_images=images[1:], duration=20, loop=0, optimize=False, transparency=255, disposal=2)
    return (emojiId+'intense.gif')
