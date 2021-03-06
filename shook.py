from PIL import Image, ImageFilter, GifImagePlugin, ImageSequence, ImageChops, ImageDraw, ImageEnhance, ImageOps
import os, glob, time, asyncio
import math, random

X = [226, 160, 280, 198, 255, 280, 160]
Y = [515, 530, 540, 550, 550, 585, 645]
X2 = [310, 220]
Y2 = [595, 790]
leng = len(X)
leng2 = len(X2)
rot = []
rot2 = []
for i in range(leng):
    rot.append(random.randint(0, 360))
    ##print(rot[i])
for i in range(leng2):
    rot2.append(random.randint(0, 360))
    ##print(rot2[i])

one = Image.open("Base.png")
two = Image.open("Arm.png")
short = Image.open("BaseAwooga.png")
shorts = False


def processStaticImage(emoPng, emojiId):
    emoPng = emoPng.convert("RGBA")
    one1 = Image.open("Base.png").copy()  # if emojiId != '681244980593164336' else Image.open("BaseAwooga.png").copy()
    two1 = Image.open("Arm.png").copy()
    wRatio = emoPng.width / emoPng.height
    ## w*h = a, a = 4900, w = wR*h, (wR*h)*h = a, wR*h^2 = a
    height = round(math.sqrt(4900 / wRatio))
    width = round(wRatio * height)
    for i in range(leng):
        one1.alpha_composite(emoPng.resize((width, height), Image.LANCZOS).rotate(rot[i], Image.BICUBIC, expand=1), (X[i], Y[i]))
    comp2 = Image.alpha_composite(one1, two1)
    for i in range(leng2):
        comp2.alpha_composite(emoPng.resize((width, height), Image.LANCZOS).rotate(rot2[i], Image.BICUBIC, expand=1), (X2[i], Y2[i]))
    comp2.save(emojiId + 'hold.png', format='PNG')
    return emojiId + 'hold.png'

def processGifImageT(emoGif, emojiId):
    return processGifImage(emoGif, emojiId, True)

def processGifImageF(emoGif, emojiId):
    return processGifImage(emoGif, emojiId, False)

def processGifImage(emoGif, emojiId, rando):
    one1 = Image.open("Base.png").copy()
    two2 = Image.open("Arm.png").copy()
    images = []
    Offset1 = []
    Offset2 = []
    totalFrames = emoGif.n_frames
    gifDuration = emoGif.info['duration']
    wRatio = emoGif.width / emoGif.height
    ## w*h = a, a = 4900, w = wR*h, (wR*h)*h = a, wR*h^2 = a
    height = round(math.sqrt(4900 / wRatio))
    width = round(wRatio * height)
    for i in range(0, 7, 1):
        Offset1.append(random.randint(0, totalFrames * rando))
    for i in range(0, 2, 1):
        Offset2.append(random.randint(0, totalFrames * rando))
    if totalFrames < 1200:
        for frame in range(0, totalFrames, 1):
            onec = one1.copy()
            twoc = two2.copy()
            for i in range(leng):
                newframe = frame + Offset1[i]
                if newframe >= totalFrames:
                    newframe = newframe - totalFrames
                emoGif.seek(newframe)
                emoFrame = emoGif.copy().convert('RGBA')
                onec.alpha_composite(emoFrame.resize((width, height), Image.LANCZOS).rotate(rot[i], Image.BICUBIC, expand=1), (X[i], Y[i]))
            comp2 = Image.alpha_composite(onec, twoc)
            for i in range(leng2):
                newframe = frame + Offset2[i]
                if newframe >= totalFrames:
                    newframe = newframe - totalFrames
                emoGif.seek(newframe)
                emoFrame = emoGif.copy().convert('RGBA')
                comp2.alpha_composite(emoFrame.resize((width, height), Image.LANCZOS).rotate(rot2[i], Image.BICUBIC, expand=1), (X2[i], Y2[i]))
            comp2 = comp2.resize((170, 227), Image.LANCZOS)
            images.append(comp2)
        images[0].save(emojiId + 'hold.gif', save_all=True, append_images=images[1:], duration=gifDuration, loop=0, optimize=True)
        return emojiId + 'hold.gif'
    else:
        return "Too many frames"


def processShookImage(emoPng, emojiId):
    images = []
    frames = 24 - 1
    ##img = Image.new('RGBA', (80,80), (0, 0 ,0 ,0))
    canvas = Image.open('canvas.png')
    frequency = 3
    frequency2 = 6
    emoPng = emoPng.convert('RGBA')
    for i in range(0, frames, 1):
        ##canvas = img2.copy()
        ratio = emoPng.height / emoPng.width
        if emoPng.width > 80:
            image = emoPng.copy().resize((80, round(80 * ratio)), Image.BICUBIC)
        else:
            image = emoPng.copy().resize((80, round(80 * ratio)), Image.NEAREST)
        image = image.rotate(round(4 * math.sin(((2 * math.pi) / frequency) * (i - frequency))), Image.BICUBIC, expand=0)
        canvas.paste(image)
        image = canvas
        offsetX = round(1 * 0.8 * math.sin(((2 * math.pi) / frequency2) * (i - frequency2)))
        offsetY = round(1 * 0.2 * math.sin(((2 * math.pi) / frequency2) * (i - frequency2)))
        image2 = ImageChops.offset(image, offsetX, offsetY)
        croppedImage = image2.crop((0, 0, 80, 80))
        alpha = croppedImage.split()[3]
        croppedImage = croppedImage.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        croppedImage.paste(255, mask)
        images.append(croppedImage)
    images[0].save(str(emojiId) + 'shook.gif', save_all=True, append_images=images[1:], duration=20, loop=0, optimize=False, transparency=255, disposal=2)
    return (str(emojiId) + 'shook.gif')


def processMoreShookImage(emoPng, emojiId):
    images = []
    frames = 24 - 1
    ##img = Image.new('RGBA', (80,80), (0, 0 ,0 ,0))
    canvas = Image.open('canvas.png')
    frequency = 3
    frequency2 = 6
    emoPng = emoPng.convert('RGBA')
    for i in range(0, frames, 1):
        ##canvas = img2.copy()
        ratio = emoPng.height / emoPng.width
        if emoPng.width > 80:
            image = emoPng.copy().resize((80, round(80 * ratio)), Image.BICUBIC)
        else:
            image = emoPng.copy().resize((80, round(80 * ratio)), Image.NEAREST)
        image = image.rotate(round(8 * math.sin(((2 * math.pi) / frequency) * (i - frequency))), Image.BICUBIC, expand=0)
        canvas.paste(image)
        image = canvas
        offsetX = round(2 * 0.8 * math.sin(((2 * math.pi) / frequency2) * (i - frequency2)))
        offsetY = round(2 * 0.2 * math.sin(((2 * math.pi) / frequency2) * (i - frequency2)))
        image2 = ImageChops.offset(image, offsetX, offsetY)
        croppedImage = image2.crop((0, 0, 80, 80))
        alpha = croppedImage.split()[3]
        croppedImage = croppedImage.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        croppedImage.paste(255, mask)
        images.append(croppedImage)
    images[0].save(emojiId + 'moreshook.gif', save_all=True, append_images=images[1:], duration=20, loop=0, optimize=False, transparency=255, disposal=2)
    ##optimize(emojiId+'moreshook.gif')
    return emojiId + 'moreshook.gif'


def processCrazyShookImage(emoPng, emojiId):  # is this even used?
    images = []
    frames = 60 - 1
    ##img = Image.new('RGBA', (80,80), (0, 0 ,0 ,0))
    canvas = Image.open('canvas.png').resize((50, 50))
    frequency = 3
    frequency2 = 6
    emoPng = emoPng.convert('RGBA')
    for i in range(0, frames, 1):
        ##canvas = img2.copy()
        ratio = emoPng.height / emoPng.width
        if emoPng.width > 50:
            image = emoPng.copy().resize((50, round(50 * ratio)), Image.BICUBIC)
        else:
            image = emoPng.copy().resize((50, round(50 * ratio)), Image.NEAREST)
        image = image.rotate(round(8 * math.sin(((2 * math.pi) / frequency) * (i - frequency)) + (i * 6)), Image.BICUBIC, expand=0)
        offsetX = round(2 * 0.8 * math.sin(((2 * math.pi) / frequency2) * (i - frequency2)) + ((i * 50) / 30))
        offsetY = round(2 * 0.2 * math.sin(((2 * math.pi) / frequency2) * (i - frequency2)) + ((i * 50 * ratio) / 60))
        image2 = ImageChops.offset(image, offsetX, offsetY)
        croppedImage = image2
        alpha = croppedImage.split()[3]
        croppedImage = croppedImage.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        croppedImage.paste(255, mask)
        images.append(croppedImage)
    images[0].save(emojiId + 'crazyshook.gif', save_all=True, append_images=images[1:], duration=20, loop=0, optimize=False, transparency=255, disposal=2)
    ##optimize(emojiId+'crazyshook.gif')
    return emojiId + 'crazyshook.gif'


def processNukeImage(emoPng, emojiId):
    images = []
    frames = 240 - 1
    ##img = Image.new('RGBA', (160,160), (0, 0 ,0 ,0))
    canvas = Image.open('canvas.png')
    frequency = 3
    frequency2 = 6
    emoPng = emoPng.convert('RGBA')
    for i in range(0, frames, 1):
        mult = (i / 287) * 1.9 + 0.2
        if i > 159:
            endt = (i - 160)
            exp = 3 ** (endt / 12) - 1
            if i == 160:
                print(i, exp)
        else:
            exp = 0
            endt = 0
        ##canvas = img.copy()
        ratio = emoPng.height / emoPng.width
        if emoPng.width > 80:
            image = emoPng.copy().resize((80, round(80 * ratio)), Image.BICUBIC)
        else:
            image = emoPng.copy().resize((80, round(80 * ratio)), Image.NEAREST)
        image = image.rotate(round(mult * 8 * math.sin(((2 * math.pi) / frequency) * (i - frequency))), Image.BICUBIC, expand=0)
        canvas.paste(image)
        image = canvas
        offsetX = round(mult * 3 * 0.8 * math.sin(((2 * math.pi) / frequency2) * (i - frequency2)))
        offsetY = round(mult * 3 * 0.2 * math.sin(((2 * math.pi) / frequency2) * (i - frequency2)))
        image2 = ImageChops.offset(image, offsetX, offsetY)
        croppedImage = image2.crop((0, 0, 80, round(80 * ratio)))
        alpha = croppedImage.split()[3]
        cropL = croppedImage.load()
        if i > 159:
            expt = 1.3 ** (endt / 20) - 1
            for y in range(0, round(80 * ratio), 1):
                for x in range(0, 80, 1):
                    r, g, b, a = cropL[x, y]
                    rrat = (255 - r) / 80
                    grat = (255 - g) / 80
                    brat = (255 - b) / 80
                    rend = round(rrat * expt) + r if round(rrat * expt) + r < 255 else 255
                    gend = round(grat * expt) + g if round(grat * expt) + g < 255 else 255
                    bend = round(brat * expt) + b if round(brat * expt) + b < 255 else 255
                    if a > 0:
                        cropL[x, y] = (rend, gend, bend, 255)
        croppedImage = ImageEnhance.Brightness(croppedImage).enhance(exp + 1)
        ##croppedImage = croppedImage.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        croppedImage = croppedImage.convert('P', palette=Image.ADAPTIVE, colors=255)
        croppedImage.quantize(30)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        croppedImage.paste(255, mask)
        images.append(croppedImage)
    images[0].save(emojiId + 'nuke.gif', save_all=True, append_images=images[1:], duration=20, loop=0, optimize=False, transparency=255, disposal=2)
    return emojiId + 'nuke.gif'


def processNukeGif(emoGif, emojiId):
    images = []
    frames = 240 - 1
    totalFrames = emoGif.n_frames
    gifDuration = emoGif.info['duration']
    if gifDuration < 20:
        gifDuration = 100
    frame_ratio = 20 / gifDuration
    # img = Image.new('RGBA', (160,160), (0, 0 ,0 ,0))
    canvas = Image.open('canvas.png')
    frequency = 3
    frequency2 = 6
    # emoPng = emoPng.convert('RGBA')
    for i in range(0, frames, 1):
        framePick = int(math.floor((i * frame_ratio) % totalFrames))
        emoGif.seek(framePick)
        emoPng = emoGif.copy().convert('RGBA')
        mult = (i / 287) * 1.9 + 0.2
        if i > 159:
            endt = (i - 160)
            exp = 3 ** (endt / 12) - 1
            if i == 160:
                print(i, exp)
        else:
            exp = 0
            endt = 0
        # canvas = img.copy()
        ratio = emoPng.height / emoPng.width
        if emoPng.width > 80:
            image = emoPng.copy().resize((80, round(80 * ratio)), Image.BICUBIC)
        else:
            image = emoPng.copy().resize((80, round(80 * ratio)), Image.NEAREST)
        image = image.rotate(round(mult * 8 * math.sin(((2 * math.pi) / frequency) * (i - frequency))), Image.BICUBIC, expand=0)
        canvas.paste(image)
        image = canvas
        offsetX = round(mult * 3 * 0.8 * math.sin(((2 * math.pi) / frequency2) * (i - frequency2)))
        offsetY = round(mult * 3 * 0.2 * math.sin(((2 * math.pi) / frequency2) * (i - frequency2)))
        image2 = ImageChops.offset(image, offsetX, offsetY)
        croppedImage = image2.crop((0, 0, 80, round(80 * ratio)))
        alpha = croppedImage.split()[3]
        cropL = croppedImage.load()
        if i > 159:
            expt = 1.3 ** (endt / 20) - 1
            for y in range(0, round(80 * ratio), 1):
                for x in range(0, 80, 1):
                    r, g, b, a = cropL[x, y]
                    rrat = (255 - r) / 80
                    grat = (255 - g) / 80
                    brat = (255 - b) / 80
                    rend = round(rrat * expt) + r if round(rrat * expt) + r < 255 else 255
                    gend = round(grat * expt) + g if round(grat * expt) + g < 255 else 255
                    bend = round(brat * expt) + b if round(brat * expt) + b < 255 else 255
                    if a > 0:
                        cropL[x, y] = (rend, gend, bend, 255)
        croppedImage = ImageEnhance.Brightness(croppedImage).enhance(exp + 1)
        # croppedImage = croppedImage.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        croppedImage = croppedImage.convert('P', palette=Image.ADAPTIVE, colors=255)
        croppedImage.quantize(30)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        croppedImage.paste(255, mask)
        images.append(croppedImage)
    images[0].save(emojiId + 'nuke.gif', save_all=True, append_images=images[1:], duration=20, loop=0, optimize=False, transparency=255, disposal=2)
    return emojiId + 'nuke.gif'
