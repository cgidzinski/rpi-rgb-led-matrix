# /etc/rc.local
#sudo python displaymain.py -c 8 -b 50
from samplebase import SampleBase
from rgbmatrix import graphics
from rgbmatrix import RGBMatrix
from PIL import Image
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
purple = graphics.Color(155, 48, 255)
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
            graphics.DrawLine(offscreenCanvas, 0, 0, width, 0, color)
            graphics.DrawLine(offscreenCanvas, 0, height, width, height, color)
            graphics.DrawLine(offscreenCanvas, 0, 0, 0, height, color)
            graphics.DrawLine(offscreenCanvas, width, 0, width, height, color)
        def severityColors(val):
            if len(val) < bugLow:
                return green
            elif len(val) > bugHigh:
                return red
            else:
                return orange

        def bugsnagOverview(offscreenCanvas):
            newErrors = bugsnagCall.findErrors("new")
            ipErrors = bugsnagCall.findErrors("in_progress")
            offscreenCanvas.Clear()

            drawSquare(offscreenCanvas, white)
            graphics.DrawLine(offscreenCanvas, 0, height-3, width, height-3, white)

            
            graphics.DrawLine(offscreenCanvas, 0, 0, 28, 28, purple)
            graphics.DrawLine(offscreenCanvas, 0, 28, 28, 0, purple)
            
            graphics.DrawLine(offscreenCanvas, 0, 0, 28, 0, purple)
            graphics.DrawLine(offscreenCanvas, 0, 28, 28, 28, purple)
            graphics.DrawLine(offscreenCanvas, 0, 0, 0, 28, purple)
            graphics.DrawLine(offscreenCanvas, 28, 0, 28, 28, purple)
            

            image = Image.open('./bugsnag.jpg')
            image.thumbnail((28, 28), Image.ANTIALIAS)
            self.matrix.SetImage(image.convert('RGB'))



            label = "New"
            graphics.DrawText(offscreenCanvas, fontBig, 30, 12, severityColors(newErrors), str(len(newErrors)))
            graphics.DrawText(offscreenCanvas, fontBig, 30+(8*len(str(len(newErrors)))+3), 12, white, label)
            
            label = "In Progress"
            graphics.DrawText(offscreenCanvas, fontBig, 30, 26, severityColors(ipErrors), str(len(ipErrors)))
            graphics.DrawText(offscreenCanvas, fontBig, 30+(8*len(str(len(ipErrors)))+3), 26, white, label)

            offscreenCanvas = self.matrix.SwapOnVSync(offscreenCanvas)
            time.sleep(30)

        def bugsnagList(offscreenCanvas):
            newErrors = bugsnagCall.findErrors("new")
            ipErrors = bugsnagCall.findErrors("in_progress")
            offscreenCanvas.Clear()

            for bug in ipErrors:
                offscreenCanvas.Clear()
                drawSquare(offscreenCanvas,green)
                graphics.DrawText(offscreenCanvas, fontSmall, width-(6*len(bug['severity'])), 7, red ,bug['severity'] )
                graphics.DrawText(offscreenCanvas, fontSmall, 2, 9, blue, "INP" )
                graphics.DrawText(offscreenCanvas, fontSmall, 24, 9, white,  bug['error_class'] )
                graphics.DrawText(offscreenCanvas, fontSmall, 2, 20, white, bug['message'] )
                graphics.DrawLine(offscreenCanvas, 0, 21, width, 21, white)
                graphics.DrawText(offscreenCanvas, fontSmall, 2, 30, white,bug['context'] )
                offscreenCanvas = self.matrix.SwapOnVSync(offscreenCanvas)
                time.sleep(5);
            
            for bug in newErrors:
                offscreenCanvas.Clear()
                drawSquare(offscreenCanvas,green)
                graphics.DrawText(offscreenCanvas, fontSmall, width-(6*len(bug['severity'])), 7, red ,bug['severity'] )
                graphics.DrawText(offscreenCanvas, fontSmall, 2, 9, blue, "NEW" )
                graphics.DrawText(offscreenCanvas, fontSmall, 24, 9, white,  bug['error_class'] )
                graphics.DrawText(offscreenCanvas, fontSmall, 2, 20, white,bug['message'] )
                graphics.DrawLine(offscreenCanvas, 0, 21, width, 21, white)
                graphics.DrawText(offscreenCanvas, fontSmall, 2, 30, white,bug['context'] )
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
        #
        while True:
            bugsnagOverview(offscreenCanvas)
        


# Main function
if __name__ == "__main__":
    parser = main()
    if (not parser.process()):
            parser.print_help()
