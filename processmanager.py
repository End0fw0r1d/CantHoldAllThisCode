import io
import json
import multiprocessing
import random
import threading
import time
import os.path
from multiprocessing.connection import Client
from multiprocessing.connection import Listener

import requests
from PIL import Image

from DickMan import processManImage, processManGif
from intense import intensifytext
from italicize import italicizePng, italicizeGif
from jpegify import JpegImage, JpegGif
from jpegify2 import JpegGif2, JpegImage2
from jpegify3 import JpegGif3, JpegImage3
from mockingSpongebob import mockingSpongebob
from monkaShoot import processShootImage
from notbttv import notBttv, notBttvDef
from pptasty import process4headImage, process4headGif, processwormholeImage, processwormholeGif
from shook import processMoreShookImage, processNukeImage, processCrazyShookImage, processShookImage, processGifImageT, processGifImageF, processStaticImage, \
    processNukeGif
from space import processSpaceGif, processSpaceImage
from speed import speedtext

jobQueue = []
outputQueue = []
imageArgs = {"intense": ["text", "int", "int", "int", "int"], "speed": ["text", "int", "int", "int", "int"], "mocking": ["text"], "space": ["image"],
             "shoot": ["image"], "italics": ["image"], "jpeg": ["image"], "man": ["image"], "jpeg2": ["image", "int"], "jpeg3": ["image", "int"],
             "weee": ["image"], "shake": ["image"], "nuke": ["image"], "moreshake": ["image"], "hold": ["image"], "hold2": ["image"],
             "overlay2": ["image", "string", "int", "int", "int", "int"], "overlay": ["image", "string"], "4head": ["image", "int"], "wormhole": ["image"]}
imageFunc = {"intense": [intensifytext], "speed": [speedtext], "mocking": [mockingSpongebob], "space": [processSpaceImage, processSpaceGif],
             "shoot": [processShootImage], "italics": [italicizePng, italicizeGif], "jpeg": [JpegImage, JpegGif], "man": [processManImage, processManGif],
             "jpeg2": [JpegImage2, JpegGif2], "jpeg3": [JpegImage3, JpegGif3], "weee": [processCrazyShookImage], "shake": [processShookImage],
             "nuke": [processNukeImage, processNukeGif], "moreshake": [processMoreShookImage], "hold": [processStaticImage, processGifImageF],
             "hold2": [processStaticImage, processGifImageT], "overlay2": [notBttvDef], "overlay": [notBttv], "4head": [process4headImage, process4headGif],
             "wormhole": [processwormholeImage, processwormholeGif]}


def listening():
    listener = Listener(('', 5001))
    while True:
        try:
            conn = listener.accept()
            msg = json.loads(conn.recv())
            jobQueue.append(msg)
        except:
            print("transfer failed...")
        time.sleep(0.1)


# def awaiting():
#     while True:
#         if len(outputQueue) > 0:
#             print(outputQueue)
#             client = Client(('localhost', 5000))
#             payload = outputQueue.pop()  # payload is [0] == channel id, [1] == message/filename
#             client.send(payload)
#         time.sleep(0.1)


def grabImage(urll):  # if you direct link to a png/gif/etc, it will directly return it as a bytestream of the image
    r = requests.get(urll, allow_redirects=True)
    r.close()
    return io.BytesIO(r.content)


def getID(emoji_string):
    idString = emoji_string[emoji_string.rfind(':') + 1:-1]
    print(idString)
    return (idString)


def exists(path):  # checks if url exists
    r = requests.head(path)
    return r.status_code == requests.codes.ok


def deconstruct(inlist, varlist):
    outlist = []
    arglist = []
    gif = False
    for i in inlist:    # removes all empty list positions
        if i == "" or i == " ":
            inlist.remove(i)
    for i in range(len(varlist)-1,0,-1):
        arglist.insert(0,inlist.pop())
    if inlist != []:
        if inlist[0] in imageArgs:
            varg = inlist.pop(0)
            arglist.insert(0, imageProcessing(varg," ".join(inlist)))
        else:
            if varlist[0] != "text":
                arglist.insert(0, inlist.pop(0))
            else:
                arglist.insert(0, " ".join(inlist))
    for i in reversed(varlist):
        if i == "int":
            outlist.append(int(arglist.pop()))
        if i == "text":
            outlist.append(" ".join(arglist))
        if i == "string":
            outlist.append(str(arglist.pop()))
        if i == "image":
            if os.path.isfile(arglist[-1]):
                if str(arglist[-1])[-3:] == "gif":
                    gif = True
                filename = str(arglist[-1])
                image = Image.open(filename)
                outlist.append(image)
                os.remove(arglist.pop())
            else:
                try:
                    idstring = int(getID(arglist.pop()))
                    url = "https://cdn.discordapp.com/emojis/" + str(idstring)
                    gif = exists(url + ".gif")
                    image = Image.open(grabImage(url))
                    outlist.append(image)
                except:
                    return False
    outlist.reverse()
    print(outlist)
    return outlist, gif


def imageProcessing(command, userinput):
    randid = str(random.randint(0, 99999) + 1)
    output = "Error"
    try:
        if command in imageArgs:
            args, gswitch = deconstruct(userinput.split(" "), imageArgs[command])
            if not args:
                output = "Error"
            else:
                args.append(randid)
                if not gswitch:
                    output = imageFunc[command][0](*args)
                else:
                    output = imageFunc[command][1](*args)
    except:
        output = "Error"
    return output
    # client = Client(('localhost', 5000))
    # payload = [channel_id, output]  # payload is [0] == channel id, [1] == message/filename
    # client.send(payload)
    # outputQueue.append([channel_id, output])  # payload is [0] == channel id, [1] == message/filename

def processing(command, userinput, channel_id):
    output = "Error"
    output = imageProcessing(command, userinput)
    client = Client(('localhost', 5000))
    payload = [channel_id, output]  # payload is [0] == channel id, [1] == message/filename
    client.send(payload)

if __name__ == '__main__':
    thr = threading.Thread(target=listening)
    thr.start()
    # thr2 = threading.Thread(target=awaiting)
    # thr2.start()
    while True:
        while len(jobQueue) > 0:
            job = jobQueue.pop(0)  # job is dict channel/command/message
            print(job)
            p = multiprocessing.Process(target=processing, args=(job["command"], job["userinput"], job["channel"]))
            p.start()
            # processing(job["command"], job["userinput"], job["channel"])
        time.sleep(0.1)
