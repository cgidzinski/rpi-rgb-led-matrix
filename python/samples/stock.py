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
        textA = "COST +3.14 (+2.68%) COST +3.14 (+2.68%) COST +3.14 (+2.68%) COST +3.14 (+2.68%)"
        textB = "GILD +6.54 (+3.23%) GILD +6.54 (+3.23%) GILD +6.54 (+3.23%) GILD +6.54 (+3.23%)"
        textC = strftime("%a, %d %b %Y %H:%M:%S", localtime(none))

        while True:
            offscreenCanvas.Clear()

            lenA = graphics.DrawText(offscreenCanvas, fontBig, posA, 11, red, textA)
            lenB = graphics.DrawText(offscreenCanvas, fontBig, posB, 22, green, textB)
            lenC = graphics.DrawText(offscreenCanvas, fontSmall, 0, 30, white, textC)
           
            textC = strftime("%a, %d %b %Y %H:%M:%S", localtime())
            posA += 1
            posB -= 1
            if (posA > offscreenCanvas.width):
                posA = -lenA

            if (posB + lenB < 0):
                posB = offscreenCanvas.width
            # scrollTextA = textA[0+posA:32+posA]
            time.sleep(0.05)
            # posA += 1
            offscreenCanvas = self.matrix.SwapOnVSync(offscreenCanvas)


# Main function
if __name__ == "__main__":
    parser = RunText()
    if (not parser.process()):
        parser.print_help()
