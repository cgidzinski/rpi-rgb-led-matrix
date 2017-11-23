# /etc/rc.local
#sudo python displaymain.py -c 8 -b 50
from samplebase import SampleBase
from rgbmatrix import graphics
from rgbmatrix import RGBMatrix
import time
from time import localtime, strftime
from threading import Thread
import subprocess
import json
import os
import commands
#
fontBig = graphics.Font()
fontBig.LoadFont("../../fonts/8x13B.bdf")
fontSmall = graphics.Font()
fontSmall.LoadFont("../../fonts/6x10.bdf")
fontSuper = graphics.Font()
fontSuper.LoadFont("../../fonts/10x20.bdf")
green = graphics.Color(0, 255, 0)
red = graphics.Color( 255, 0, 0)
blue = graphics.Color(0, 0, 255)
white = graphics.Color(255, 255, 255)



class main(SampleBase):
	def __init__(self, *args, **kwargs):
		super(main, self).__init__(*args, **kwargs)
#
	def Run(self):
		offscreenCanvas = self.matrix.CreateFrameCanvas()
		offscreenCanvas.Clear()
		graphics.DrawText(offscreenCanvas, fontSuper, 1, 20, white, commands.getoutput('hostname -I'))
		offscreenCanvas = self.matrix.SwapOnVSync(offscreenCanvas)
		time.sleep(30)

# Main function
if __name__ == "__main__":
	parser = main()
	if (not parser.process()):
		parser.print_help()