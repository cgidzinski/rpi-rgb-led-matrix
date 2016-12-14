#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
import time

class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)

    def Run(self):
        self.matrix = RGBMatrix(1, 8, 1)
        self.matrix.brightness = 60
        offscreenCanvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("../../fonts/7x13.bdf")
        textColor = graphics.Color(255, 255, 255)
        pos = offscreenCanvas.width
        myText = "Costco +5.00%"

        while True:
            offscreenCanvas.Clear()
            len = graphics.DrawText(offscreenCanvas, font, pos, 8, textColor, myText)
            pos -= 1
            if (pos + len < 0):
                pos = offscreenCanvas.width

            time.sleep(0.025)
            offscreenCanvas = self.matrix.SwapOnVSync(offscreenCanvas)


# Main function
if __name__ == "__main__":
    parser = RunText()
    if (not parser.process()):
        parser.print_help()
