#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
from rgbmatrix import RGBMatrix
import time
from time import localtime, strftime
from threading import Thread
import subprocess
import json
import os
#
speed = 0.025
fontBig = graphics.Font()
fontBig.LoadFont("../../fonts/8x13B.bdf")
fontSmall = graphics.Font()
fontSmall.LoadFont("../../fonts/6x10.bdf")
green = graphics.Color(0, 255, 0)
red = graphics.Color( 255, 0, 0)
blue = graphics.Color(0, 0, 255)
white = graphics.Color(255, 255, 255)
#
symbols = ["NASDAQ:COST","NASDAQ:GILD","TSE:OTC"]
# textData = [["COST","161.34", "+0.53","+0.22%",green],["GILD","89.34", "+0.00","+0.00%",blue],["OTX","74.75", "+0.53","+0.22%",red]]
textData = []
def get_value():
    textDataArray = []
    identifier = ','.join(symbols)
    get_value_url = 'http://finance.google.com/finance/info?client=ig&q=' + identifier 
    value = subprocess.Popen(['curl', '-s', get_value_url], stdout=subprocess.PIPE).communicate()[0]
    j = json.loads(value[4:len(value)-1])
    for i in xrange(0,len(j)):
        dataItem = [str(j[i]['t']),str(j[i]['l']),str(j[i]['c']),str(j[i]['cp'])]
        if float(j[i]['c']) == 0.00:
            dataItem.append(blue)
        if float(j[i]['c']) > 0.00:
            dataItem.append(green)
        if float(j[i]['c']) < 0.00:
            dataItem.append(red)   
        textDataArray.append(dataItem)    
    return textDataArray

def getPrices():
    while True:
        print "Getting Update Data"
        textData = get_value()
        print "Got Data\r\n"
        time.sleep(60)
        
def getInitialPrices():
    print "Getting Initial Data"
    textData = get_value()
    print "Got Data\r\n"
    return

class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)

    def Run(self):
        self.matrix.brightness = 60
        offscreenCanvas = self.matrix.CreateFrameCanvas()

        getInitialPrices()
        print textData
        quit()
        textQueueTop = [] #pos #index
        textQueueBottom = [] #pos #index

        IndexTop=0
        IndexBottom=len(textData)-1

        posTop = offscreenCanvas.width
        posBottom = 0-8*(len(textData[IndexBottom][0])+len(textData[IndexBottom][1])+len(textData[IndexBottom][2])+len(textData[IndexBottom][3])+5)

        t = Thread(target=getPrices)
        t.daemon = True
        t.start()

        while True:
            offscreenCanvas.Clear()
            graphics.DrawText(offscreenCanvas, fontSmall, 1, 31, white, strftime("%B %d, %Y", localtime()))
            graphics.DrawText(offscreenCanvas, fontSmall, 190, 31, white, strftime("%I:%M:%S %p", localtime()))

            if len(textQueueTop) == 0:
                textQueueTop.append([posTop,IndexTop])

            if len(textQueueBottom) == 0:
                textQueueBottom.append([posBottom,IndexBottom])

            for i in xrange(0,len(textQueueTop)):
                lenTop = graphics.DrawText(offscreenCanvas, fontBig, textQueueTop[i][0], 11, textData[textQueueTop[i][1]][4], textData[textQueueTop[i][1]][0] +" "+ textData[textQueueTop[i][1]][1] +" "+ textData[textQueueTop[i][1]][2] +" ("+ textData[textQueueTop[i][1]][3]+")")
                textQueueTop[i][0] -=1

            for i in xrange(0,len(textQueueBottom)):
                lenBottom = graphics.DrawText(offscreenCanvas, fontBig, textQueueBottom[i][0], 23, textData[textQueueBottom[i][1]][4], textData[textQueueBottom[i][1]][0] +" "+ textData[textQueueBottom[i][1]][1] +" "+ textData[textQueueBottom[i][1]][2] +" ("+ textData[textQueueBottom[i][1]][3]+")")
                textQueueBottom[i][0] +=1

            if (textQueueTop[len(textQueueTop)-1][0] == (offscreenCanvas.width - lenTop-8)):
                if IndexTop != len(textData)-1:
                    IndexTop+=1
                else:
                    IndexTop = 0
                textQueueTop.append([offscreenCanvas.width,IndexTop])

            if (textQueueBottom[len(textQueueBottom)-1][0] == 8):
                if IndexBottom != 0:
                    IndexBottom-=1
                else:
                    IndexBottom = len(textData)-1
                lenTest = 8*(len(textData[IndexBottom][0])+len(textData[IndexBottom][1])+len(textData[IndexBottom][2])+len(textData[IndexBottom][3])+5)
                textQueueBottom.append([0-lenTest,IndexBottom])
           
            time.sleep(speed)
            offscreenCanvas = self.matrix.SwapOnVSync(offscreenCanvas)
# Main function
if __name__ == "__main__":
    parser = RunText()
    if (not parser.process()):
        parser.print_help()