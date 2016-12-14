#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
from rgbmatrix import RGBMatrix
import time
from time import localtime, strftime

class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)

    def Run(self):
        self.matrix.brightness = 60
        offscreenCanvas = self.matrix.CreateFrameCanvas()
        fontBig = graphics.Font()
        fontBig.LoadFont("../../fonts/8x13B.bdf")
        fontSmall = graphics.Font()
        fontSmall.LoadFont("../../fonts/6x10.bdf")
        green = graphics.Color(0, 255, 0)
        red = graphics.Color( 255, 0, 0)
        blue = graphics.Color(0, 0, 255)
        white = graphics.Color(255, 255, 255)

        posA = 0 #offscreenCanvas.width
        posB = 0

        textTop = [["Costco [COST]", "+0.53","+0.22%",green],["Gilead Sciences [GILD]", "+0.53","+0.22%",blue],["OpenText [OTX]", "+0.53","+0.22%",red]]
        textBottom = [["Costco [COST]", "+0.53","+0.22%",green],["Gilead Sciences [GILD]", "+0.53","+0.22%",blue],["OpenText [OTX]", "+0.53","+0.22%",red]]
   

        while True:
            offscreenCanvas.Clear()
            textDate = strftime("%B %d, %Y", localtime())
            textTime = strftime("%H:%M:%S", localtime())
            graphics.DrawText(offscreenCanvas, fontSmall, 1, 31, white, textDate)
            graphics.DrawText(offscreenCanvas, fontSmall, 208, 31, white, textTime)




            totalOffsetTop = 0
            for x in xrange(0,len(textTop)):
                lenTop = graphics.DrawText(offscreenCanvas, fontBig, posA+(totalOffsetTop), 11, textTop[x][3], textTop[x][1]+" "+textTop[x][1] +" ("+ textTop[x][2]+")")
                totalOffsetTop += (lenTop+8)
            posA -= 1


            if (posA + totalOffsetTop < 0):
                posA = offscreenCanvas.width





            totalOffsetBottom = 0
            for x in xrange(0,len(textBottom)):
                lenBottom = graphics.DrawText(offscreenCanvas, fontBig, posB+(totalOffsetBottom), 22, textTop[x][3],  textTop[x][1]+" "+textTop[x][1] +" ("+ textTop[x][2]+")")
                totalOffsetBottom += (lenBottom+8)
            posB += 1
            if (posB > totalOffsetBottom-(8*len(textBottom))):
                posB = 0
            time.sleep(0.035)
            offscreenCanvas = self.matrix.SwapOnVSync(offscreenCanvas)


# Main function
if __name__ == "__main__":
    parser = RunText()
    if (not parser.process()):
        parser.print_help()
