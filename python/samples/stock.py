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
        font = graphics.Font()
        font.LoadFont("../../fonts/8x13.bdf")
        green = graphics.Color(0, 255, 0)
        red = graphics.Color( 255, 0, 0)
        blue = graphics.Color(0, 0, 255)
        white = graphics.Color(255, 255, 255)

        posA = 0
        posB = offscreenCanvas.width

        textA = "StockA -0.14"
        textB = "StockB 4.14"
        textC = "StockA -0.14 StockB +4.14 StockC +5.34"

        while True:
            offscreenCanvas.Clear()

            lenA = graphics.DrawText(offscreenCanvas, font, posA, 9, blue, textA)
            lenB = graphics.DrawText(offscreenCanvas, font, posB, 19, green, textB)
            lenC = graphics.DrawText(offscreenCanvas, font, 0, 32, red, textC)
           
            posA += 1
            posB -= 1
            if (posA > offscreenCanvas.width):
                posA = 0 - lenA
            if (posB + lenB < 0):
                posB = offscreenCanvas.width

            time.sleep(0.1)
            offscreenCanvas = self.matrix.SwapOnVSync(offscreenCanvas)


# Main function
if __name__ == "__main__":
    parser = RunText()
    if (not parser.process()):
        parser.print_help()
