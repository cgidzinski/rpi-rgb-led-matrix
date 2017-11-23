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
width = 255
height =31 
bugLow = 5
bugHigh = 10
#
slogans = ["Loading Bear Cave","Loading Skynet","Loading Broken Code","Flaunching Data Into Space"]
#
class main(SampleBase):
    def __init__(self, *args, **kwargs):
        super(main, self).__init__(*args, **kwargs)

    def Run(self):
        def drawSquare(offscreenCanvas, color):
            graphics.DrawLine(offscreenCanvas, 0, 0, width, 0, orange)
            graphics.DrawLine(offscreenCanvas, 0, height, width, height, orange)
            graphics.DrawLine(offscreenCanvas, 0, 0, 0, height, orange)
            graphics.DrawLine(offscreenCanvas, width, 0, width, height, orange)
            

        def bugsnag(proj, offscreenCanvas):
            newErrors = bugsnagCall.findErrors(proj,"new")
            ipErrors = bugsnagCall.findErrors(proj,"in_progress")
            offscreenCanvas.Clear()

            drawSquare(offscreenCanvas,white)

            graphics.DrawLine(offscreenCanvas, 26, 0, 26, height, orange)
            graphics.DrawLine(offscreenCanvas, 0, 11, width, 11, white)
            graphics.DrawLine(offscreenCanvas, 0, 22, width, 22, white)

            graphics.DrawText(offscreenCanvas, fontBig, 2, 12, white, "NEW")
            if len(newErrors) < bugLow:
                graphics.DrawText(offscreenCanvas, fontBig, 72, 21, green, str(len(newErrors)))
            elif len(newErrors) > bugHigh:
                graphics.DrawText(offscreenCanvas, fontBig, 72, 21, orange, str(len(newErrors)))
            else:
                graphics.DrawText(offscreenCanvas, fontBig, 72, 21, red, str(len(newErrors)))

            graphics.DrawText(offscreenCanvas, fontBig, 2, 28, white, "IP ")
            if len(ipErrors) < bugLow:
                graphics.DrawText(offscreenCanvas, fontBig, 64, 28, green, str(len(ipErrors)))
            elif len(ipErrors) > bugHigh:
                graphics.DrawText(offscreenCanvas, fontBig, 64, 28, orange, str(len(ipErrors)))
            else:
                graphics.DrawText(offscreenCanvas, fontBig, 64, 28, red, str(len(ipErrors)))

            offscreenCanvas = self.matrix.SwapOnVSync(offscreenCanvas)
            time.sleep(100)
            for bug in xrange(0,len(newErrors),1):
                offscreenCanvas.Clear()
                drawSquare(offscreenCanvas,green)
                graphics.DrawText(offscreenCanvas, fontSmall, 2, 9, white,newErrors[bug]['severity'] )
                graphics.DrawText(offscreenCanvas, fontSmall, 8*len(newErrors[bug]['severity']), 9, white,newErrors[bug]['error_class'] )
                graphics.DrawLine(offscreenCanvas, 0, 11, width, 11, white)
                graphics.DrawText(offscreenCanvas, fontSmall, 2, 19, white,newErrors[bug]['message'] )
                graphics.DrawLine(offscreenCanvas, 0, 21, width, 21, white)
                graphics.DrawText(offscreenCanvas, fontSmall, 2, 29, white,newErrors[bug]['context'] )
                offscreenCanvas = self.matrix.SwapOnVSync(offscreenCanvas)
                time.sleep(5);

        offscreenCanvas = self.matrix.CreateFrameCanvas()
        offscreenCanvas.Clear()
        slogansText = slogans[random.randint(0,len(slogans)-1)]
        for pos in xrange(width,1,-2):
            offscreenCanvas.Clear()
            graphics.DrawText(offscreenCanvas, fontBig, pos, 12, green, slogansText)
            graphics.DrawText(offscreenCanvas, fontBig, pos, 30, blue, commands.getoutput('hostname -I'))
            drawSquare(offscreenCanvas,orange)
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
