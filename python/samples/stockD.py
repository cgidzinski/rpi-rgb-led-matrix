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


        # textData = [["COST","161.34", "+0.53","+0.22%",green],["GILD","89.34", "+0.00","+0.00%",blue],["OTX","74.75", "+0.53","+0.22%",red]]
        textData = [["C","O", "S","T",green],["G","I","L","D",blue],["O","T","E","X",red],["C","O", "S","T",green],["G","I","L","D",blue],["O","T","E","X",red]]
        posA = 0
        while True:
            offscreenCanvas.Clear()
            textDate = strftime("%B %d, %Y", localtime())
            textTime = strftime("%H:%M:%S", localtime())
            graphics.DrawText(offscreenCanvas, fontSmall, 1, 31, white, textDate)
            graphics.DrawText(offscreenCanvas, fontSmall, 208, 31, white, textTime)



            totalLength = 0
            for x in xrange(0,len(textData)):
                lenTop = graphics.DrawText(offscreenCanvas, fontBig, posA+totalLength, 11, textData[x][4], textData[x][0]+" "+textData[x][1]+" "+textData[x][2] +" ("+ textData[x][3]+")")
                totalLength += (lenTop+8)






            lenBottom = graphics.DrawText(offscreenCanvas, fontBig, 0, 22,blue, "COST 163.24 GILD 72.54 OTX 88.46")
           

            posA -=1

            time.sleep(0.035)
            offscreenCanvas = self.matrix.SwapOnVSync(offscreenCanvas)


# Main function
if __name__ == "__main__":
    parser = RunText()
    if (not parser.process()):
        parser.print_help()


            # totalOffsetTop = 0
            # for x in xrange(0,len(textData)):
            #     lenTop = graphics.DrawText(offscreenCanvas, fontBig, posA+(totalOffsetTop), 11, textData[x][3], textData[x][1]+" "+textData[x][1] +" ("+ textData[x][2]+")")
            #     totalOffsetTop += (lenTop+8)
            # posA -= 1


            # if (posA + totalOffsetTop < 0):
            #     posA = offscreenCanvas.width