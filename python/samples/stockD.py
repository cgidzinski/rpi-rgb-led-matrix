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


        textData = [["COST","161.34", "+0.53","+0.22%",green],["GILD","89.34", "+0.00","+0.00%",blue],["OTX","74.75", "+0.53","+0.22%",red]]
        textQueue = [] #pos #index
        posA = offscreenCanvas.width
        x=0
        totalLength = 0

        textQueue.append([offscreenCanvas.width,x])


        while True:
            offscreenCanvas.Clear()
            textDate = strftime("%B %d, %Y", localtime())
            textTime = strftime("%H:%M:%S", localtime())
            graphics.DrawText(offscreenCanvas, fontSmall, 1, 31, white, textDate)
            graphics.DrawText(offscreenCanvas, fontSmall, 208, 31, white, textTime)

            

            


            for i in xrange(0,len(textQueue)):
                lenTop = graphics.DrawText(offscreenCanvas, fontBig, textQueue[i][0], 11, textData[textQueue[i][1]][4], textData[textQueue[i][1]][0])
                totalLength = (lenTop+8)
                textQueue[i][0] -=1



            if (textQueue[x][0] == (offscreenCanvas.width - lenTop-8)):
                if x != len(textData)-1:
                    x+=1
                    textQueue.append([offscreenCanvas.width,x])
                else:
                    x = 0


            lenBottom1 = graphics.DrawText(offscreenCanvas, fontBig, 0, 22,blue, str(x))
            lenBottom2 = graphics.DrawText(offscreenCanvas, fontBig, 50, 22,blue, str(len(textData)))

            time.sleep(0.04)
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






            # totalLength = 0
            # for x in xrange(0,len(textData)):
            #     lenTop = graphics.DrawText(offscreenCanvas, fontBig, posA+totalLength, 11, textData[x][4], textData[x][0]+" "+textData[x][1]+" "+textData[x][2] +" ("+ textData[x][3]+")")
            #     totalLength += (lenTop+8)

            # posA -=1

            # if (posA  < 0+8):
            #     posA = offscreenCanvas.width
            #     # lenTop = graphics.DrawText(offscreenCanvas, fontBig, posA+totalLength, 11, textData[x][4], textData[x][0]+" "+textData[x][1]+" "+textData[x][2] +" ("+ textData[x][3]+")")
            #     # totalLength += (lenTop+8)
