# /etc/rc.local
#sudo python displaymain.py -c 8 -b 50
from samplebase import SampleBase
from rgbmatrix import graphics
from rgbmatrix import RGBMatrix
import json
import os
import time
import commands
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
width = 256
height = 64


class main(SampleBase):
    def __init__(self, *args, **kwargs):
            super(main, self).__init__(*args, **kwargs)

    def Run(self):
            offscreenCanvas = self.matrix.CreateFrameCanvas()
            offscreenCanvas.Clear()
            graphics.DrawText(offscreenCanvas, fontBig, 0, 12, green, "Loading Bear Cave Hivemind")
            graphics.DrawText(offscreenCanvas, fontBig, 0, 25, blue, commands.getoutput('hostname -I'))
            offscreenCanvas = self.matrix.SwapOnVSync(offscreenCanvas)
            time.sleep(10)
            #
            offscreenCanvas.Clear()
            bugsnagCall.setup()
            org = bugsnagCall.findOrg()
            proj = bugsnagCall.findProject(org)
            newErrors = bugsnagCall.findErrors(proj,"New")
            ipErrors = bugsnagCall.findErrors(proj,"in_progress")
            graphics.DrawText(offscreenCanvas, fontSuper, 0, 10, green, "New Bugs: "+ str(len(newErrors)))
            graphics.DrawText(offscreenCanvas, fontSuper, 0, 31, red, "IP Bugs: "+ str(len(ipErrors)))
            offscreenCanvas = self.matrix.SwapOnVSync(offscreenCanvas)
            time.sleep(10000)

# Main function
if __name__ == "__main__":
    parser = main()
    if (not parser.process()):
            parser.print_help()
