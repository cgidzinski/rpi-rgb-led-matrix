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
        textQueueTop = [] #pos #index
        textQueueBottom = [] #pos #index
        posTop = offscreenCanvas.width
        posBottom = offscreenCanvas.width
        IndexTop=0
        IndexBottom=0
       

        while True:
            offscreenCanvas.Clear()
            textDate = strftime("%B %d, %Y", localtime())
            textTime = strftime("%H:%M:%S", localtime())
            graphics.DrawText(offscreenCanvas, fontSmall, 1, 31, white, textDate)
            graphics.DrawText(offscreenCanvas, fontSmall, 208, 31, white, textTime)

            if len(textQueueTop) == 0:
                textQueueTop.append([offscreenCanvas.width,IndexTop])

            if len(textQueueBottom) == 0:
                textQueueBottom.append([offscreenCanvas.width,IndexBottom])



            for i in xrange(0,len(textQueueTop)):
                lenTop = graphics.DrawText(offscreenCanvas, fontBig, textQueueTop[i][0], 11, textData[textQueueTop[i][1]][4], textData[textQueueTop[i][1]][0] +" "+ textData[textQueueTop[i][1]][1] +" "+ textData[textQueueTop[i][1]][2] +" ("+ textData[textQueueTop[i][1]][3]+")")
                textQueueTop[i][0] -=1

            for i in xrange(0,len(textQueueBottom)):
                lenBottom = graphics.DrawText(offscreenCanvas, fontBig, textQueueBottom[i][0], 22, textData[textQueueBottom[i][1]][4], textData[textQueueBottom[i][1]][0] +" "+ textData[textQueueBottom[i][1]][1] +" "+ textData[textQueueBottom[i][1]][2] +" ("+ textData[textQueueBottom[i][1]][3]+")")
                textQueueBottom[i][0] -=1



            if (textQueueTop[len(textQueueTop)-1][0] == (offscreenCanvas.width - lenTop-8)):
                if IndexTop != len(textData)-1:
                    IndexTop+=1
                else:
                    IndexTop = 0
                textQueueTop.append([offscreenCanvas.width,IndexTop])

            if (textQueueBottom[len(textQueueBottom)-1][0] == (offscreenCanvas.width - lenBottom-8)):
                if IndexBottom != len(textData)-1:
                    IndexBottom+=1
                else:
                    IndexBottom = 0
                textQueueBottom.append([offscreenCanvas.width,IndexBottom])
           
            time.sleep(0.03)
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
