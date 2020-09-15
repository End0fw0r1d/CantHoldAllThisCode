import sys, requests, io, math, random
from PIL import Image
from io import BytesIO
from multiprocessing.connection import Client
from ShookImage import processShookImage
from italicize import italicizePng, italicizeGif
from jpegify import JpegImage, JpegGif
from jpegify2 import JpegImage2, JpegGif2
from jpegify3 import JpegImage3, JpegGif3
from notbttv import notBttv
from space import processSpaceGif, processSpaceImage
from monkaShoot import processShootImage
from intense import intensifytext
from DickMan import processManImage, processManGif
import slots
import adventuring


randId = str(random.randint(0,99999))
message = False
def exists(path):
    r = requests.head(path)
    return r.status_code == requests.codes.ok

def grabImage(urll): ##if you direct link to a png/gif/etc, it will directly return it as a bytestream of the image
    r = requests.get(urll, allow_redirects=True)
    return io.BytesIO(r.content)
    r.close()

args = sys.argv
print(args[2])
#args[0] is program name
#args[1] is discord channel
#args[2] is image id string, or other main arg
#args[3] is command used
#args[4] will be any extra pass-args?
#if the id string isn't just numbers, it isn't a valid image id string and is prolly a message
try:
    idString = int(args[2])
    url = "https://cdn.discordapp.com/emojis/"+str(idString)
    gif = exists(url+".gif")
    emojiImage = Image.open(grabImage(url))
except:
    idString = args[2]
    if idString == 'gachiPRIDE':
        emojiImage = Image.open('gachiPRIDE.gif')
        gif = True
    message = True
imageFilename = 'error'
if args[3] == 'slots':
    imageFilename = slots.slotMachine(int(args[2]),str(args[4]))
if args[3] == 'bank':
    imageFilename = slots.bank(str(args[2]))
if args[3] == 'buildstart':
    imageFilename = adventuring.buildStart(str(args[2]))
if args[3] == 'simtest':
    imageFilename = adventuring.simTime(str(args[2]))
if args[3] == 'intense':
    print(args)
    imageFilename = intensifytext(str(args[2]),int(args[-1]),int(args[-4]),int(args[-3]),int(args[-2]),randId)
if args[3] == 'shook':
    if gif == False:
        imageFilename = processShookImage(emojiImage,randId)
if args[3] == 'italics':
    if gif:
        imageFilename = italicizeGif(emojiImage,randId)
    else:
        imageFilename = italicizePng(emojiImage,randId)
if args[3] == 'jpeg':
    if gif:
        imageFilename = JpegGif(emojiImage,randId)
    else:
        imageFilename = JpegImage(emojiImage,randId)
if args[3] == 'jpeg2':
    if gif:
        imageFilename = JpegGif2(emojiImage,randId,int(args[4]))
    else:
        imageFilename = JpegImage2(emojiImage,randId,int(args[4]))
if args[3] == 'jpeg3':
    if gif:
        imageFilename = JpegGif3(emojiImage,randId,int(args[4]))
    else:
        imageFilename = JpegImage3(emojiImage,randId,int(args[4]))
if args[3] == 'overlay':
    imageFilename = notBttv(emojiImage,randId,args[4],int(args[5]),int(args[6]),float(args[7]),float(args[8]))
if args[3] == 'space':
    if gif:
        imageFilename = processSpaceGif(emojiImage,randId)
    else:
        imageFilename = processSpaceImage(emojiImage,randId)
if args[3] == 'shoot':
    if gif:
        #imageFilename = processSpaceGif(emojiImage,randId)
        imageFilename = "gifs not yet supported :C"
    else:
        imageFilename = processShootImage(emojiImage,randId)
if args[3] == 'man':
    if gif:
        imageFilename = processManGif(emojiImage,randId)
    else:
        imageFilename = processManImage(emojiImage,randId)


c = Client(('localhost', 5000))
payload = [args[1],imageFilename] #if imageFilename is none, do something mebbe
c.send(payload)
