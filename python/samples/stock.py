#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
from rgbmatrix import RGBMatrix
import time

class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)

    def Run(self):
        self.matrix.brightness = 60
        offscreenCanvas = self.matrix.CreateFrameCanvas()
        fontBig = graphics.Font()
        fontBig.LoadFont("../../fonts/8x13.bdf")
        fontSmall = graphics.Font()
        fontSmall.LoadFont("../../fonts/6x10.bdf")
        green = graphics.Color(0, 255, 0)
        red = graphics.Color( 255, 0, 0)
        blue = graphics.Color(0, 0, 255)
        white = graphics.Color(255, 255, 255)

        posA = 0 #offscreenCanvas.width
        posB = 0

        textA = "COST +3.14 (+2.68%) GILD +6.54 (+3.23%) WILD +3.14 (+2.68%) KILD +3.14 (+2.68%)"
        scrollTextA = ""
        textB = "GILD +6.54 (+3.23%) GILD +6.54 (+3.23%) GILD +6.54 (+3.23%) GILD +6.54 (+3.23%)"
        textC = "Why you play the babby gam?"

        while True:
            offscreenCanvas.Clear()

            lenA = graphics.DrawText(offscreenCanvas, fontBig, 0, 10, red, scrollTextA)
            lenB = graphics.DrawText(offscreenCanvas, fontBig, posB, 21, green, textB)
            lenC = graphics.DrawText(offscreenCanvas, fontSmall, 0, 30, white, textC)
           
            
            
            scrollTextA = textA[0+posA:32+posA]
            time.sleep(0.3)
            posA += 1
            offscreenCanvas = self.matrix.SwapOnVSync(offscreenCanvas)


# Main function
if __name__ == "__main__":
    parser = RunText()
    if (not parser.process()):
        parser.print_help()
