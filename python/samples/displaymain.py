# /etc/rc.local
#sudo python displaymain.py -c 8 -b 50
from samplebase import SampleBase
from rgbmatrix import graphics
from rgbmatrix import RGBMatrix
import json
import os
import time
import commands
from random import randint
#
import bugsnagCall
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
orange = graphics.Color(255, 165, 0)
width = 256
height = 64

slogans = ["Loading Bear Cave","Loading Skynet","Loading Broken Code"]

class main(SampleBase):
    def __init__(self, *args, **kwargs):
            super(main, self).__init__(*args, **kwargs)

    def Run(self):
            offscreenCanvas = self.matrix.CreateFrameCanvas()
            offscreenCanvas.Clear()
            pos = width
            while pos > 0:
                offscreenCanvas.Clear()
                graphics.DrawText(offscreenCanvas, fontBig, pos, 11, green, slogans[random.randint(0,len(slogans)-1])
                graphics.DrawText(offscreenCanvas, fontBig, pos, 31, blue, "IP: "+commands.getoutput('hostname -I'))
                offscreenCanvas = self.matrix.SwapOnVSync(offscreenCanvas)
                pos -=2
                time.sleep(0.001)
            time.sleep(5)
            #
            bugsnagCall.setup()
            org = bugsnagCall.findOrg()
            proj = bugsnagCall.findProject(org)

            while True:
                offscreenCanvas.Clear()
                newErrors = bugsnagCall.findErrors(proj,"New")
                ipErrors = bugsnagCall.findErrors(proj,"in_progress")
                graphics.DrawText(offscreenCanvas, fontBig, 1, 11, white, "NEW Bugs: ")
                graphics.DrawText(offscreenCanvas, fontBig, 72, 11, green, str(len(newErrors)))
                graphics.DrawText(offscreenCanvas, fontBig, 1, 29, white, "IP Bugs: ")
                graphics.DrawText(offscreenCanvas, fontBig, 64, 29, orange, str(len(ipErrors)))
                offscreenCanvas = self.matrix.SwapOnVSync(offscreenCanvas)
                time.sleep(60)

# Main function
if __name__ == "__main__":
    parser = main()
    if (not parser.process()):
            parser.print_help()
