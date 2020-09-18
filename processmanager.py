import json
import random
import threading
import time
import io
from multiprocessing.connection import Client
from multiprocessing.connection import Listener
from PIL import Image

import requests

from intense import intensifytext
from speed import speedtext
from mockingSpongebob import mockingSpongebob
from space import processSpaceGif, processSpaceImage
from monkaShoot import processShootImage
from italicize import italicizePng, italicizeGif
from jpegify import JpegImage, JpegGif
from DickMan import processManImage, processManGif
from jpegify2 import JpegGif2, JpegImage2
from jpegify3 import JpegGif3, JpegImage3
from shook import processMoreShookImage, processNukeImage, processCrazyShookImage, processShookImage, processGifImage, processStaticImage
from notbttv import notBttv

jobQueue = []
outputQueue = []


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


def awaiting():
    while True:
        if len(outputQueue) > 0:
            print(outputQueue)
            client = Client(('localhost', 5000))
            payload = outputQueue.pop()  # payload is [0] == channel id, [1] == message/filename
            client.send(payload)
        time.sleep(0.1)


def grabImage(urll):  # if you direct link to a png/gif/etc, it will directly return it as a bytestream of the image
    r = requests.get(urll, allow_redirects=True)
    r.close()
    return io.BytesIO(r.content)


def getID(emoji_string):
    idString = emoji_string[emoji_string.rfind(':') + 1:-1]
    return (idString)


def exists(path):  # checks if url exists
    r = requests.head(path)
    return r.status_code == requests.codes.ok


def deconstruct(input, varlist):
    outlist = []
    inlist = input.split(" ")
    print(inlist)
    if len(varlist) > len(inlist):
        return False
    for i in reversed(varlist):
        while inlist[-1] == "" or inlist[-1] == " ":
            inlist.pop()
        if i == "int":
            outlist.append(int(inlist.pop()))
        if i == "text":
            outlist.append(" ".join(inlist))
        if i == "string":
            outlist.append(str(inlist.pop()))
        if i == "image":
            try:
                idstring = int(getID(inlist.pop()))
                url = "https://cdn.discordapp.com/emojis/" + str(idstring)
                gif = exists(url + ".gif")
                image = Image.open(grabImage(url))
                outlist.append([image, gif])
            except:
                return False
    outlist.reverse()
    print(outlist)
    return outlist


def imageProcessing(command, userinput, channel_id):
    randid = str(random.randint(0, 99999) + 1)
    output = "Error"
    try:
        if command == "intense":
            print("intense")
            args = deconstruct(userinput, ["text", "int", "int", "int", "int"])
            if not args:
                print("not args")
                output = "Error"
            else:
                a, r, g, b, e = args
                output = intensifytext(a, e, r, g, b, randid)
        if command == "speed":
            args = deconstruct(userinput, ["text", "int", "int", "int", "int"])
            if not args:
                output = "Error"
            else:
                a, r, g, b, e = args
                output = speedtext(a, e, r, g, b, randid)
        if command == "mocking":
            args = deconstruct(userinput, ["text"])
            if not args:
                output = "Error"
            else:
                a = args[0]
                output = mockingSpongebob(a, randid)
        if command == "space":
            args = deconstruct(userinput, ["image"])
            if not args:
                output = "Error"
            else:
                a = args[0]
                if not a[1]:
                    output = processSpaceImage(a[0], randid)
                else:
                    output = processSpaceGif(a[0], randid)
        if command == "shoot":
            args = deconstruct(userinput, ["image"])
            if not args:
                output = "Error"
            else:
                a = args[0]
                if not a[1]:
                    output = processShootImage(a[0], randid)
                else:
                    output = "Gifs not currently supported"
        if command == "italics":
            args = deconstruct(userinput, ["image"])
            if not args:
                output = "Error"
            else:
                a = args[0]
                if not a[1]:
                    output = italicizePng(a[0], randid)
                else:
                    output = italicizeGif(a[0], randid)
        if command == "jpeg":
            args = deconstruct(userinput, ["image"])
            if not args:
                output = "Error"
            else:
                a = args[0]
                if not a[1]:
                    output = JpegImage(a[0], randid)
                else:
                    output = JpegGif(a[0], randid)
        if command == "man":
            args = deconstruct(userinput, ["image"])
            if not args:
                output = "Error"
            else:
                a = args[0]
                if not a[1]:
                    output = processManImage(a[0], randid)
                else:
                    output = processManGif(a[0], randid)
        if command == "jpeg2":
            args = deconstruct(userinput, ["image", "int"])
            if not args:
                output = "Error"
            else:
                a, b = args
                b = 20 if b > 20 else b
                if not a[1]:
                    output = JpegImage2(a[0], b, randid)
                else:
                    output = JpegGif2(a[0], b, randid)
        if command == "jpeg3":
            args = deconstruct(userinput, ["image", "int"])
            if not args:
                output = "Error"
            else:
                a, b = args
                b = 20 if b > 20 else b
                if not a[1]:
                    output = JpegImage3(a[0], b, randid)
                else:
                    output = JpegGif3(a[0], b, randid)
        if command == "weee":
            args = deconstruct(userinput, ["image"])
            if not args:
                output = "Error"
            else:
                a = args[0]
                if not a[1]:
                    output = processCrazyShookImage(a[0], randid)
                else:
                    output = "Gifs not supported yet"
        if command == "shake":
            args = deconstruct(userinput, ["image"])
            if not args:
                output = "Error"
            else:
                a = args[0]
                if not a[1]:
                    output = processShookImage(a[0], randid)
                else:
                    output = "Gifs not supported yet"
        if command == "moreshake":
            args = deconstruct(userinput, ["image"])
            if not args:
                output = "Error"
            else:
                a = args[0]
                if not a[1]:
                    output = processMoreShookImage(a[0], randid)
                else:
                    output = "Gifs not supported yet"
        if command == "nuke":
            args = deconstruct(userinput, ["image"])
            if not args:
                output = "Error"
            else:
                a = args[0]
                if not a[1]:
                    output = processNukeImage(a[0], randid)
                else:
                    output = "Gifs not supported yet"
        if command == "hold":
            args = deconstruct(userinput, ["image"])
            if not args:
                output = "Error"
            else:
                a = args[0]
                if not a[1]:
                    output = processStaticImage(a[0], randid)
                else:
                    output = processGifImage(a[0], randid, False)
        if command == "hold2":
            args = deconstruct(userinput, ["image"])
            if not args:
                output = "Error"
            else:
                a = args[0]
                if not a[1]:
                    output = processStaticImage(a[0], randid)
                else:
                    output = processGifImage(a[0], randid, True)
        if command == "overlay":
            args = deconstruct(userinput, ["image", "string"])
            if not args:
                output = "Error"
            else:
                a, b = args
                if not a[1]:
                    output = notBttv(a[0], b, 0, 0, 0, 1, randid)
                else:
                    output = "Gifs not supported"
        if command == "overlay2":
            args = deconstruct(userinput, ["image", "string", "int", "int", "int", "int"])
            if not args:
                output = "Error"
            else:
                a, b, x, y, r, s = args
                s = 0.1 if s < 0.1 else s
                if not a[1]:
                    output = notBttv(a[0], b, x, y, r, s, randid)
                else:
                    output = "Gifs not supported"
    except:
        output = "Error"
    outputQueue.append([channel_id, output])  # payload is [0] == channel id, [1] == message/filename


if __name__ == '__main__':
    thr = threading.Thread(target=listening)
    thr.start()
    thr2 = threading.Thread(target=awaiting)
    thr2.start()
    while True:
        while len(jobQueue) > 0:
            job = jobQueue.pop(0)  # job is dict channel/command/message
            print(job)
            # p = multiprocessing.Process(target=imageProcessing, args=(job["command"], job["userinput"], job["channel"]))
            imageProcessing(job["command"], job["userinput"], job["channel"])
        time.sleep(0.1)
