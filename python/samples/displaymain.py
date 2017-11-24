# /etc/rc.local
#sudo python displaymain.py -c 8 -b 50
from samplebase import SampleBase
from rgbmatrix import graphics
from rgbmatrix import RGBMatrix
from PIL import Image
import json, os, time, commands, random
#
import bugsnagCall
#
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
purple = graphics.Color(155, 48, 255)
#
width = 255
height =31 
bugLow = 5
bugHigh = 10
#
slogans = ["Loading Bear Cave","Loading Skynet","Loading Broken Code","Flaunching Data Into Space"]
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

        def severityColors(val):
            if len(val) < bugLow:
                return green
            elif len(val) > bugHigh:
                return red
            else:
                return orange

        def bugsnagOverview(offscreenCanvas):
            newErrors = bugsnagCall.findErrors("new")
            openErrors = bugsnagCall.findErrors("open")
            ipErrors = bugsnagCall.findErrors("in_progress")
            ignoredErrors = bugsnagCall.findErrors("ignored")
            offscreenCanvas.Clear()
            for cycle in xrange(1,255):

                image = Image.open('./bugsnag.jpg')
                image.thumbnail((28, 28), Image.ANTIALIAS)
                image.convert('RGB')
                pixels =  list(image.getdata())
                
                index = 0
                for y in xrange(0,28):
                    for x in xrange(0,28):
                        offscreenCanvas.SetPixel(x+1,y+1,pixels[index][0],pixels[index][1],pixels[index][2])
                        index += 1

                drawSquare(offscreenCanvas,purple)
                graphics.DrawLine(offscreenCanvas, 0, height-3, width, height-3, purple)

                label = "New"
                graphics.DrawText(offscreenCanvas, fontBig, 30+(8*len(label)+3), 12, severityColors(newErrors), str(len(newErrors)))
                graphics.DrawText(offscreenCanvas, fontBig, 30, 12, white, label)
                
                label = "In Progress"
                graphics.DrawText(offscreenCanvas, fontBig, 30+(8*len(label)+3), 26, severityColors(ipErrors), str(len(ipErrors)))
                graphics.DrawText(offscreenCanvas, fontBig, 30, 26, white, label)
                
                label = "Open"
                graphics.DrawText(offscreenCanvas, fontBig, width-(8*(len(label)+len(str(len(openErrors))))), 12, severityColors(openErrors), str(len(openErrors)))
                graphics.DrawText(offscreenCanvas, fontBig, width-(8*len(label)), 12, white, label)

                label = "Ignored"
                graphics.DrawText(offscreenCanvas, fontBig, width-(8*(len(label)+len(str(len(ignoredErrors))))), 26, severityColors(ignoredErrors), str(len(ignoredErrors)))
                graphics.DrawText(offscreenCanvas, fontBig, width-(8*len(label)), 26, white, label)

                minX =1 
                maxX = 254
                 
                graphics.DrawLine(offscreenCanvas, minX, height-2, cycle, height-2, orange)
                graphics.DrawLine(offscreenCanvas, minX, height-1, cycle, height-1, orange)
                offscreenCanvas = self.matrix.SwapOnVSync(offscreenCanvas)
                offscreenCanvas.Clear()
                time.sleep(0.05) 
                

        def chunk(seq, size):
            return [seq[i:i+size] for i in range(0, len(seq), size)]

        def showGif(offscreenCanvas, image,speed):
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
                        offscreenCanvas.SetPixel(x,y,colors[pixels[index]][0],colors[pixels[index]][1],colors[pixels[index]][2])
                        index += 1
                image.seek(z);
                offscreenCanvas = self.matrix.SwapOnVSync(offscreenCanvas)
                time.sleep(speed)
            
        def bugsnagList(offscreenCanvas):
            newErrors = bugsnagCall.findErrors("new")
            ipErrors = bugsnagCall.findErrors("in_progress")
            offscreenCanvas.Clear()

            for bug in ipErrors:
                offscreenCanvas.Clear()
                drawSquare(offscreenCanvas,green)
                graphics.DrawText(offscreenCanvas, fontSmall, width-(6*len(bug['severity'])), 7, red ,bug['severity'] )
                graphics.DrawText(offscreenCanvas, fontSmall, 2, 9, blue, "INP" )
                graphics.DrawText(offscreenCanvas, fontSmall, 24, 9, white,  bug['error_class'] )
                graphics.DrawText(offscreenCanvas, fontSmall, 2, 20, white, bug['message'] )
                graphics.DrawLine(offscreenCanvas, 0, 21, width, 21, white)
                graphics.DrawText(offscreenCanvas, fontSmall, 2, 30, white,bug['context'] )
                offscreenCanvas = self.matrix.SwapOnVSync(offscreenCanvas)
                time.sleep(5);
            
            for bug in newErrors:
                offscreenCanvas.Clear()
                drawSquare(offscreenCanvas,green)
                graphics.DrawText(offscreenCanvas, fontSmall, width-(6*len(bug['severity'])), 7, red ,bug['severity'] )
                graphics.DrawText(offscreenCanvas, fontSmall, 2, 9, blue, "NEW" )
                graphics.DrawText(offscreenCanvas, fontSmall, 24, 9, white,  bug['error_class'] )
                graphics.DrawText(offscreenCanvas, fontSmall, 2, 20, white,bug['message'] )
                graphics.DrawLine(offscreenCanvas, 0, 21, width, 21, white)
                graphics.DrawText(offscreenCanvas, fontSmall, 2, 30, white,bug['context'] )
                offscreenCanvas = self.matrix.SwapOnVSync(offscreenCanvas)
                time.sleep(5);






        offscreenCanvas = self.matrix.CreateFrameCanvas()
        offscreenCanvas.Clear()
        slogansText = slogans[random.randint(0,len(slogans)-1)]
        for cnum in xrange(0,2):
            offscreenCanvas = self.matrix.SwapOnVSync(offscreenCanvas)
            graphics.DrawText(offscreenCanvas, fontBig, 36, 12, green, slogansText)
            graphics.DrawText(offscreenCanvas, fontBig, 34, 30, blue, commands.getoutput('hostname -I'))
            drawSquare(offscreenCanvas,white)
        lastTime = int(time.time())
        
        while (int(time.time())-lastTime < 4 ):
            showGif(offscreenCanvas, "./bear.gif",0.1)
        #
        bugsnagCall.setup()
        #
        while True:
            bugsnagOverview(offscreenCanvas)
        


# Main function
if __name__ == "__main__":
    parser = main()
    if (not parser.process()):
            parser.print_help()
