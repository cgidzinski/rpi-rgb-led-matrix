# /etc/rc.local
#sudo python displaymain.py -c 8 -b 50
from samplebase import SampleBase
from rgbmatrix import graphics
from rgbmatrix import RGBMatrix
from threading import Thread
from PIL import Image
import subprocess, json, os, time, commands, random
#
fontNano = graphics.Font()
fontNano.LoadFont("../../fonts/4x6.bdf")
fontTiny = graphics.Font()
fontTiny.LoadFont("../../fonts/5x8.bdf")
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
yellow = graphics.Color(255, 255, 0)
purple = graphics.Color(155, 48, 255)
#
width = 255
height =31 
bugLow = 5
bugHigh = 10
#
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

        def drawImage(offscreenCanvas,image,xCoord):
            image = Image.open(image)
            image.thumbnail((256, 32), Image.ANTIALIAS)
            image.convert('RGB')
            pixels =  list(image.getdata())
            index = 0
            for y in xrange(0,32):
                for x in xrange(0,256):
                    offscreenCanvas.SetPixel((xCoord+x),y,pixels[index][0],pixels[index][1],pixels[index][2])
                    index += 1

        def chunk(seq, size):
            return [seq[i:i+size] for i in range(0, len(seq), size)]

        def showGif(offscreenCanvas, image, speed, xCoord):
            image = Image.open(image)
            image.convert('RGB')
            frames = 0 
            try:
                while True:
                    image.seek(image.tell()+1)
                    frames+=1
            except:
                pass
            palette= image.im.getpalette()
            colors= [map(ord, bytes) for bytes in chunk(palette, 3)]
            image.seek(0);
            for z in xrange(0,frames):
                index = 0
                pixels =  list(image.getdata())
                for y in xrange(0,32):
                    for x in xrange(0,32):
                        offscreenCanvas.SetPixel(xCoord+x,y,colors[pixels[index]][0],colors[pixels[index]][1],colors[pixels[index]][2])
                        index += 1
                image.seek(z);
                offscreenCanvas = self.matrix.SwapOnVSync(offscreenCanvas)
                time.sleep(speed)

#############################################################################################################################
        offscreenCanvas = self.matrix.CreateFrameCanvas()
        drawImage(offscreenCanvas, "./img.png",0)
        offscreenCanvas = self.matrix.SwapOnVSync(offscreenCanvas)
        #
        while True:
            time.sleep(1)        


# Main function
if __name__ == "__main__":
    parser = main()
    if (not parser.process()):
            parser.print_help()
