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
        font.LoadFont("../../fonts/7x14.bdf")
        textColor = graphics.Color(000, 000, 255)
        pos = 0
        myText = "Costco +5.00%"

        while True:
            offscreenCanvas.Clear()
            len = graphics.DrawText(offscreenCanvas, font, pos, 12, textColor, myText)
            pos += 1
            if (pos > offscreenCanvas.width):
                pos = 0 - len
            time.sleep(0.035)
            offscreenCanvas = self.matrix.SwapOnVSync(offscreenCanvas)


# Main function
if __name__ == "__main__":
    parser = RunText()
    if (not parser.process()):
        parser.print_help()
