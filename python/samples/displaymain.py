# /etc/rc.local
#sudo python displaymain.py -c 8 -b 50
from samplebase import SampleBase
from rgbmatrix import graphics
from rgbmatrix import RGBMatrix
import json, os, time, commands, random
#
import bugsnagCall
#
fontSmall = graphics.Font()
fontSmall.LoadFont("../../fonts/6x10.bdf")
fontBig = graphics.Font()
fontBig.LoadFont("../../fonts/8x13B.bdf")
fontSuper = graphics.Font()
fontSuper.LoadFont("../../fonts/10x20.bdf")
#
green = graphics.Color(0, 255, 0)
red = graphics.Color( 255, 0, 0)
blue = graphics.Color(0, 0, 255)
white = graphics.Color(255, 255, 255)
orange = graphics.Color(255, 165, 0)
#
width = 256
height = 64
bugLow = 5
bugHigh = 10
#
slogans = ["Loading Bear Cave","Loading Skynet","Loading Broken Code","Flaunching Data To Space"]
#
class main(SampleBase):
    def __init__(self, *args, **kwargs):
        super(main, self).__init__(*args, **kwargs)

    def Run(self):
        def drawSquare(color, offscreenCanvas):
            for y in xrange(0,height,1):
                offset_canvas.SetPixel(0, y, 255, 255, 255)
                offset_canvas.SetPixel(width, y, 255, 255, 255)
            for x in xrange(0,width,1):
                offset_canvas.SetPixel(x, 0, 255, 255, 255)
                offset_canvas.SetPixel(x, height, 255, 255, 255)

        def bugsnag(proj, offscreenCanvas):
            newErrors = bugsnagCall.findErrors(proj,"new")
            ipErrors = bugsnagCall.findErrors(proj,"in_progress")
            offscreenCanvas.Clear()

            graphics.DrawText(offscreenCanvas, fontBig, 1, 11, white, "NEW Bugs: ")
            if len(newErrors) < bugLow:
                graphics.DrawText(offscreenCanvas, fontBig, 72, 11, green, str(len(newErrors)))
            elif len(newErrors) > bugHigh:
                graphics.DrawText(offscreenCanvas, fontBig, 72, 11, orange, str(len(newErrors)))
            else:
                graphics.DrawText(offscreenCanvas, fontBig, 72, 11, red, str(len(newErrors)))

            graphics.DrawText(offscreenCanvas, fontBig, 1, 29, white, "IP Bugs: ")
            if len(ipErrors) < bugLow:
                graphics.DrawText(offscreenCanvas, fontBig, 64, 29, green, str(len(ipErrors)))
            elif len(ipErrors) > bugHigh:
                graphics.DrawText(offscreenCanvas, fontBig, 64, 29, orange, str(len(ipErrors)))
            else:
                graphics.DrawText(offscreenCanvas, fontBig, 64, 29, red, str(len(ipErrors)))

            offscreenCanvas = self.matrix.SwapOnVSync(offscreenCanvas)
            time.sleep(10)
            for bug in xrange(0,len(newErrors),1):
                offscreenCanvas.Clear()
                graphics.DrawText(offscreenCanvas, fontSmall, 1, 8, white,newErrors[bug]['error_class'] )
                graphics.DrawText(offscreenCanvas, fontSmall, 1, 16, white,newErrors[bug]['message'] )
                graphics.DrawText(offscreenCanvas, fontSmall, 1, 24, white,newErrors[bug]['context'] )
                graphics.DrawText(offscreenCanvas, fontSmall, 1, 32, white,newErrors[bug]['severity'] )
                offscreenCanvas = self.matrix.SwapOnVSync(offscreenCanvas)
                time.sleep(500);

        offscreenCanvas = self.matrix.CreateFrameCanvas()
        offscreenCanvas.Clear()
        slogansText = slogans[random.randint(0,len(slogans)-1)]
        for pos in xrange(width,0,-2):
            offscreenCanvas.Clear()
            graphics.DrawText(offscreenCanvas, fontBig, pos, 11, green, slogansText)
            graphics.DrawText(offscreenCanvas, fontBig, pos, 31, blue, commands.getoutput('hostname -I'))
            offscreenCanvas = self.matrix.SwapOnVSync(offscreenCanvas)
        #
        bugsnagCall.setup()
        org = bugsnagCall.findOrg()
        proj = bugsnagCall.findProject(org)
        #
        while True:
            bugsnag(proj, offscreenCanvas)
        


# Main function
if __name__ == "__main__":
    parser = main()
    if (not parser.process()):
            parser.print_help()
