#from PIL import Image, ImageFilter, GifImagePlugin, ImageSequence, ImageChops, ImageDraw, ImageEnhance, ImageOps
import os, glob, time, asyncio
import math, random, json, io, datetime
import slots

minutesT = 30
secondsT = minutesT*60

workerdict = {}
with open('workingMen.json') as json_file:
    workerdict = json.load(json_file)

#structure is something like {userid:[userdata],userid:[userdata]}
#when you access a section of {} that doesnt exist yet, it creates it, like in dict[uid]
#when you associate dict[uid] with a value, it formats it as uid:value
#then when you access dict[uid], it returns value
#should consider nesting these logically...
#important values to keep track of are number of hospitals, number of houses, total population, total adventurers
def convertStrToTime(y):
    return datetime.datetime.strptime(y, '%Y-%m-%d %H:%M:%S.%f')
    
def simTime(UID):
    buildStart(UID)
    currentTime = datetime.datetime.now()
    lastTime = convertStrToTime(workerdict[UID]['lasttime'][0])
    difTime = currentTime - lastTime
    occurrences, remaind = divmod(difTime.total_seconds(), secondsT)
    remaindTime = workerdict[UID]['lasttime'][1] + remaind
    if remaindTime > secondsT:
        addOcc = math.floor(remaindTime/secondsT)
        occurrences = occurrences + addOcc
        remaindTime = remaindTime%secondsT
    workerdict[UID]['lasttime'] = [str(currentTime),remaindTime]
    occurrences = int(occurrences)
    print(occurrences)
    totalReturns = 0
    for i in range(occurrences):
        income = workerdict[UID]['adventurers']*10
        popcost = workerdict[UID]['population']*1
        hoscost = workerdict[UID]['hospitals']*0
        houscost = workerdict[UID]['houses']*2
        schcost = workerdict[UID]['schools']*0
        expenses = popcost + hoscost + houscost
        returns = income - expenses
        totalReturns += returns
        print(income,expenses,returns)
        slots.addCash(UID,(returns))
    with open('workingMen.json', 'w') as outfile:
            json.dump(workerdict, outfile)
    return str(totalReturns)

def buildStart(UID):
    currentTime = datetime.datetime.now()
    if UID in workerdict:
        print(workerdict[UID])
    else:
        workerdict[UID] = {}
        with open('workingMen.json', 'w') as outfile:
            json.dump(workerdict, outfile)
        workerdict[UID]['lasttime'] = [str(currentTime),0]
        workerdict[UID]['hospitals'] = 1
        workerdict[UID]['houses'] = 4
        workerdict[UID]['population'] = 10
        workerdict[UID]['adventurers'] = 4
        workerdict[UID]['schools'] = 0
        with open('workingMen.json', 'w') as outfile:
            json.dump(workerdict, outfile)
    return str(workerdict[UID])

def startAdventure():
    print('stuff')












