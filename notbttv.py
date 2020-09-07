from PIL import Image, ImageFilter, GifImagePlugin, ImageSequence, ImageChops, ImageDraw, ImageEnhance, ImageOps
import os, glob, time, asyncio
import math, random


def notBttv(emoPng, emojiId, arg, ex, ey, roty, scale):
    maskedArgs = ['hazmat','hazmatf']
    emoPng = emoPng.convert('RGBA')
    overlay = Image.open(arg+'.png').convert('RGBA')
    canvas80 = Image.open('canvas.png').resize((80,80))
    canvas2 = canvas80.copy()
    ratio = emoPng.height/emoPng.width
    ratio2 = canvas80.height/canvas80.width
    if arg in maskedArgs:
        needMask = True
    else:
        needMask = False
    if emoPng.width > 70:
        image = emoPng.copy().resize((70,round(70*ratio)), Image.BICUBIC)
    else:
        image = emoPng.copy().resize((70,round(70*ratio)), Image.NEAREST)
    if overlay.width > 80:
        image2 = overlay.copy().resize((80,round(80*ratio2)), Image.BICUBIC)
    else:
        image2 = overlay.copy().resize((80,round(80*ratio2)), Image.NEAREST)
    if needMask:
        if scale < 1: ##rescaling if scale is not 1
            image = image.copy().resize((round(image.width*scale),round(image.height*scale)), Image.BICUBIC)
        elif scale > 1:
            image = image.copy().resize((round(image.width*scale),round(image.height*scale)), Image.NEAREST)
        image = image.rotate(float(roty), Image.BICUBIC, expand=1)
        if image.height > 70 or image.width > 70:
            image = image.crop((((image.width-70)/2),((image.height-70)/2),image.width-((image.width-70)/2),image.height-((image.height-70)/2)))
        canvas80.alpha_composite(image,(round((80-image.width)/2)+5+ex,round((80-image.height)/2)+5+ey))
        mask = Image.open(arg+'mask.png').convert('RGBA')
        mask = mask.copy().resize((80,round(80*ratio2)), Image.NEAREST)
        canvas2.alpha_composite(mask,(round((80-image2.width)/2),0))
        mask = canvas2.convert('L')
        maskL = mask.load()
        canvasL = canvas80.load()
        for y in range(0,80,1):
            for x in range(0,80,1):
                num = math.floor((maskL[x,y]*10)/256)
                if maskL[x,y] > 10:
                    canvasL[x,y] = (0,0,0,0)
    if needMask:
        canvas80.alpha_composite(image2,(round((80-image2.width)/2),0))
    else:
        canvas80.alpha_composite(image,(round((80-image.width)/2)+5,round((80-image.height)/2)+5))
        image2 = image2.rotate(float(roty), Image.BICUBIC, expand=1)
        image2 = ImageChops.offset(image2,ex,ey)
        if scale < 1: ##rescaling if scale is not 1
            image2 = image2.copy().resize((round(image2.width*scale),round(image2.height*scale)), Image.BICUBIC)
        elif scale > 1:
            image2 = image2.copy().resize((round(image2.width*scale),round(image2.height*scale)), Image.NEAREST)
        image2 = image2.crop((((image2.width-80)/2),((image2.height-80)/2),image2.width-((image2.width-80)/2),image2.height-((image2.height-80)/2)))
        canvas80.alpha_composite(image2,(round((80-image2.width)/2),round((80-image2.height)/2)))
    canvas80.convert('RGBA')
    canvas80.save(emojiId+'overlay.png')
    return (str(emojiId)+'overlay.png')
