#!/usr/bin/env python
# Display a runtext with double-buffering.
#sudo ./stockD.py -c 8 -b 50
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
interval = 30
#
fontBig = graphics.Font()
fontBig.LoadFont("../../fonts/8x13B.bdf")
fontSmall = graphics.Font()
fontSmall.LoadFont("../../fonts/6x10.bdf")
green = graphics.Color(0, 255, 0)
red = graphics.Color( 255, 0, 0)
blue = graphics.Color(0, 0, 255)
white = graphics.Color(255, 255, 255)
#
#symbols = ["NASDAQ:COST","NASDAQ:GILD","TSE:OTC","NASDAQ:GOOG","NASDAQ:MSFT","NASDAQ:AAPL","NASDAQ:TSLA","NYSE:DG","TSE:CXR","NASDAQ:CSIQ","INDEXNASDAQ:.IXIC","INDEXDJX:.DJI"]
symbols = ["TSX:OTC","TSX:BNS","TSX:ACQ","TSX:SNC","TSX:BB","TSX:BAD","TSX:CPG","TSX:KEY","TSX:FRU","NASDAQ:COST","NASDAQ:GILD","NASDAQ:CISQ","NASDAQ:AAPL","NASDAQ:GOOG","NASDAQ:DLTR","NASDAQ:INTC","NYSE:BIG","NYSE:TNH","NYSE:DG"]

initData = False
textData = []
textQueueTop = [] #pos #index
textQueueBottom = [] #pos #index
#
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
	print "--- 4: " + str(len(textDataArray))  
	return textDataArray
#
def getPrices():
	global textData
	global initData
	while True:
		os.system("clear")
		print "------------------------------------------"
		print "--- Stock Catcher ------------------------"
		print "------------------------------------------"
		print "--- Stock List: " + ','.join(symbols)
		print "--- Update Interval: " + str(interval)
		print "--- Scroll Speed: " + str(speed)
		print "------------------------------------------"
		print "Getting Update Data"
		textData = get_value()
		print "Got Data at " + strftime("%I:%M:%S %p", localtime())
		print "------------------------------------------"
		initData = True
		time.sleep(interval)
#
def showAlert(offscreenCanvas,text):
	offscreenCanvas.Clear()
	graphics.DrawText(offscreenCanvas, fontSmall, 1, 31, white, text)
	time.sleep(interval)
	offscreenCanvas.Clear()
	return

class RunText(SampleBase):
	def __init__(self, *args, **kwargs):
		super(RunText, self).__init__(*args, **kwargs)
#
	def Run(self):
		offscreenCanvas = self.matrix.CreateFrameCanvas()
#
		t = Thread(target=getPrices, name="DataGet")
		t.daemon = True
		t.start()
#
		while initData == False:
			time.sleep(.1)
#
		IndexTop=0
		IndexBottom=len(textData)-1
		posTop = offscreenCanvas.width
		posBottom = 0-8*(len(textData[IndexBottom][0])+len(textData[IndexBottom][1])+len(textData[IndexBottom][2])+len(textData[IndexBottom][3])+5)
#
		while True:
			offscreenCanvas.Clear()
#
			showAlert(offscreenCanvas,"Hello!")
#
			graphics.DrawText(offscreenCanvas, fontSmall, 1, 31, white, strftime("%B %d, %Y", localtime()))
			graphics.DrawText(offscreenCanvas, fontSmall, 190, 31, white, strftime("%I:%M:%S %p", localtime()))
#
			if len(textQueueTop) == 0:
				textQueueTop.append([posTop,IndexTop])
#
			if len(textQueueBottom) == 0:
				textQueueBottom.append([posBottom,IndexBottom])
#
			for i in xrange(0,len(textQueueTop)):
				lenTop = graphics.DrawText(offscreenCanvas, fontBig, textQueueTop[i][0], 11, textData[textQueueTop[i][1]][4], textData[textQueueTop[i][1]][0] +" "+ textData[textQueueTop[i][1]][1] +" "+ textData[textQueueTop[i][1]][2] +" ("+ textData[textQueueTop[i][1]][3]+")")
				textQueueTop[i][0] -=1
#
			for i in xrange(0,len(textQueueBottom)):
				lenBottom = graphics.DrawText(offscreenCanvas, fontBig, textQueueBottom[i][0], 23, textData[textQueueBottom[i][1]][4], textData[textQueueBottom[i][1]][0] +" "+ textData[textQueueBottom[i][1]][1] +" "+ textData[textQueueBottom[i][1]][2] +" ("+ textData[textQueueBottom[i][1]][3]+")")
				textQueueBottom[i][0] +=1
#
			if (textQueueTop[len(textQueueTop)-1][0] == (offscreenCanvas.width - lenTop-8)):
				if IndexTop != len(textData)-1:
					IndexTop+=1
				else:
					IndexTop = 0
				textQueueTop.append([offscreenCanvas.width,IndexTop])
#
			if (textQueueBottom[len(textQueueBottom)-1][0] == 8):
				if IndexBottom != 0:
					IndexBottom-=1
				else:
					IndexBottom = len(textData)-1
				lenTest = 8*(len(textData[IndexBottom][0])+len(textData[IndexBottom][1])+len(textData[IndexBottom][2])+len(textData[IndexBottom][3])+5)
				textQueueBottom.append([0-lenTest,IndexBottom])
#
			if textQueueTop[0][0] < -400:
				textQueueTop.pop(0)
#
			if textQueueBottom[0][0] > 400:
				textQueueBottom.pop(0)
#
			time.sleep(speed)
			offscreenCanvas = self.matrix.SwapOnVSync(offscreenCanvas)
#


# Main function
if __name__ == "__main__":
	parser = RunText()
	if (not parser.process()):
		parser.print_help()