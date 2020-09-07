from PIL import Image, ImageFilter, GifImagePlugin, ImageSequence, ImageChops, ImageDraw, ImageEnhance, ImageOps
import os, glob, time, asyncio
import math, random, json, io, datetime
import adventuring

userdict = {}
with open('gamblingMen.json') as json_file:
    userdict = json.load(json_file)

cashMinutes = 10
cashTim = cashMinutes*60

def addCash(UID,additional):
    print('adding cash...',additional)
    currentTime = datetime.datetime.now()
    lastTime = datetime.datetime.strptime(userdict[UID][0], '%Y-%m-%d %H:%M:%S.%f')
    difTime = currentTime - lastTime
    accumulation, acc2 = divmod(difTime.total_seconds(), cashTim)
    remaindTime = userdict[UID][1] + acc2
    if remaindTime > cashTim:
        extraMoney = math.floor(remaindTime/cashTim)
        accumulation = accumulation + extraMoney
        remaindTime = remaindTime%cashTim
    newMoney = accumulation + userdict[UID][2] + additional
    print(userdict[UID])
    userdict[UID] = [str(currentTime),remaindTime,newMoney]
    print(userdict[UID])
    with open('gamblingMen.json', 'w') as outfile:
        print('dumping to json...')
        json.dump(userdict, outfile)

def accumulateCash(UID):
    print('accumulating...')
    currentTime = datetime.datetime.now()
    if UID in userdict:
        #await context.channel.send(userdict[UID])
        lastTime = datetime.datetime.strptime(userdict[UID][0], '%Y-%m-%d %H:%M:%S.%f')
        difTime = currentTime - lastTime
        accumulation, acc2 = divmod(difTime.total_seconds(), cashTim)
        remaindTime = userdict[UID][1] + acc2
        if remaindTime > cashTim:
            extraMoney = math.floor(remaindTime/cashTim)
            accumulation = accumulation + extraMoney
            remaindTime = remaindTime%cashTim
        newMoney = accumulation + userdict[UID][2]
        userdict[UID] = [str(currentTime),remaindTime,newMoney]
        with open('gamblingMen.json', 'w') as outfile:
            json.dump(userdict, outfile)
        return accumulation
    else:
        userdict[UID] = [str(currentTime),0,150]
        with open('gamblingMen.json', 'w') as outfile:
            json.dump(userdict, outfile)
        return 0

def bank(UID):
    return ("User has gained $"+str(accumulateCash(UID))+" passively and $"+str(adventuring.simTime(UID))+" actively from owned adventurers since last updated"+"\nUser has $"+str(userdict[UID][2]))

def slotMachine(message,UID):
    slotsArr = [':gem:',':moneybag:',':four_leaf_clover:',':grapes:',':watermelon:',':cherries:',':banana:',':lemon:']
    bet = 10
    returns = 0
    totalReturns = 0
    broke = False
    jackpot = False
    currentTime = datetime.datetime.now()
    accumulateCash(UID)
    rollHistory = []
    try:
        NumTries = int(message)
        if NumTries > 10:
            NumTries = 10
    except:
        NumTries = 1
    for i in range(NumTries):
        if bet > userdict[UID][2]:
            broke = True
            break
        else:
            rollA = random.randint(0,7)
            rollB = random.randint(0,7)
            rollC = random.randint(0,7)
            returns = 0
            if rollA == rollB:
                if random.randint(0,99) < 10:
                    rollC = rollB
            if rollA == rollC:
                if random.randint(0,99) < 10:
                    rollB = rollA
            if rollB == rollC:
                if random.randint(0,99) < 10:
                    rollA = rollB
            if rollA == rollB and rollB == rollC:
                jackpot = True
                if rollA == 0:
                    returns = 350
                elif rollA == 1:
                    returns = 250
                elif rollA == 2:
                    returns = 200
                elif rollA == 3 or rollA == 4 or rollA == 5 or rollA == 6:
                    returns = 160
                elif rollA == 7:
                    returns = 100
            elif rollA != rollB and rollA != rollC and rollB != rollC:
                shadyRoll = random.randint(0,99)
                if shadyRoll < 5:
                    rollA = rollB
                elif shadyRoll < 10:
                    rollA = rollC
                elif shadyRoll < 15:
                    rollB = rollC
            elif not jackpot and (rollA == rollB or rollB == rollC or rollA == rollC):
                if rollA == rollB:
                    if rollA == 0:
                        returns = 20
                    elif rollA == 1:
                        returns = 14
                    else:
                        returns = 6
                elif rollB == rollC:
                    if rollB == 0:
                        returns = 20
                    elif rollB == 1:
                        returns = 14
                    else:
                        returns = 6
                elif rollA == rollC:
                    if rollA == 0:
                        returns = 20
                    elif rollA == 1:
                        returns = 14
                    else:
                        returns = 6
            addCash(UID,(returns - bet))
            rollHistory.append([slotsArr[rollA],slotsArr[rollB],slotsArr[rollC]])
            totalReturns += returns
        #await context.channel.send('Rolled: '+slotsArr[rollA]+' '+slotsArr[rollB]+' '+slotsArr[rollC]+"\nReward: $"+str(returns))
    result = str(rollHistory).replace('\'','').replace(',','')[1:][:-1]
    if broke:
        addt = 'Ran out of cash...\n'
    else:
        addt = ''
    if jackpot:
        return(addt+'Jackpot!\nRolled: '+result+"\nReward: $"+str(totalReturns))
    else:
        return(addt+'Rolled: '+result+"\nReward: $"+str(totalReturns))
        #await context.channel.send('Jackpot!')
    #await context.channel.send('Rolled: '+result+"\nReward: $"+str(totalReturns))
