# /etc/rc.local
#sudo python displaymain.py -c 8 -b 50
from samplebase import SampleBase
from rgbmatrix import graphics
from rgbmatrix import RGBMatrix
from PIL import Image
import json, os, time, commands, random
#
import githubCall
import bugsnagCall
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
purple = graphics.Color(155, 48, 255)
#
width = 255
height =31 
bugLow = 5
bugHigh = 10
#
slogans = ["Loading Bear Cave","Loading Bearnet","Loading Bear Code","Flaunching Data Into Space"]
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

        def drawImage(offscreenCanvas,image):
            image = Image.open(image)
            image.thumbnail((32, 32), Image.ANTIALIAS)
            image.convert('RGB')
            pixels =  list(image.getdata())
            index = 0
            for y in xrange(0,32):
                for x in xrange(0,32):
                    offscreenCanvas.SetPixel(x+1,y+1,pixels[index][0],pixels[index][1],pixels[index][2])
                    index += 1

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

        def severityColorsInt(val):
            if val < bugLow:
                return green
            elif val > bugHigh:
                return red
            else:
                return orange
        
        def severityColors(val):
            if len(val) < bugLow:
                return green
            elif len(val) > bugHigh:
                return red
            else:
                return orange

        def githubOverview(offscreenCanvas):
            prs = githubCall.getData()
            offscreenCanvas.Clear()
            needReview = 0
            needTophat = 0
            needWIP = 0 
            openPR = len(prs)
            for pr in prs: 
               if pr['approvals'] < 2:
                   needReview +=1
               else:
                   needTophat +=1
               if pr['labels'].count('WIP'):
                   needWIP += 1
            needReview -= needWIP   
            openPR -= needWIP
            
            drawImage(offscreenCanvas,"./github.jpg")
            drawSquare(offscreenCanvas,purple)



            label = "Open"
            graphics.DrawText(offscreenCanvas, fontBig, 36+(8*len(label)+3), 12, severityColorsInt(openPR), str(openPR))
            graphics.DrawText(offscreenCanvas, fontBig, 36, 12, white, label)
            
            label = "WIP"
            graphics.DrawText(offscreenCanvas, fontBig, 36+(8*len(label)+3), 28, severityColorsInt(needWIP), str(needWIP))
            graphics.DrawText(offscreenCanvas, fontBig, 36, 28, white, label)
            
            label = "Need Review"
            graphics.DrawText(offscreenCanvas, fontBig, width-(8*(len(label)+len(str(needReview))+1)), 12, severityColorsInt(needReview), str(needReview))
            graphics.DrawText(offscreenCanvas, fontBig, width-(8*len(label)+1), 12, white, label)
            
            label = "Need Tophat"
            graphics.DrawText(offscreenCanvas, fontBig, width-(8*(len(label)+len(str(needTophat))+1)), 28, severityColorsInt(needTophat), str(needTophat))
            graphics.DrawText(offscreenCanvas, fontBig, width-(8*len(label)+1), 28,  white, label)

            offscreenCanvas = self.matrix.SwapOnVSync(offscreenCanvas)
            time.sleep(5)
        ##############
            for pr in prs:
                offscreenCanvas.Clear()
                if pr['labels'].count("WIP") != 0:
                    continue
                drawImage(offscreenCanvas,"./github.jpg")
                drawSquare(offscreenCanvas,purple)
                graphics.DrawText(offscreenCanvas, fontBig, 36, 27, orange ,pr['title'] )
                txtLen = "#"+str(pr['number'])
                graphics.DrawText(offscreenCanvas, fontBig, 36, 12, green,txtLen)

                graphics.DrawText(offscreenCanvas, fontBig, 215-(8*len(pr['user'])+1),12 , blue ,pr['user'] )
                if pr['approvals'] == 0: graphics.DrawText(offscreenCanvas, fontBig, 257-(5*8), 12, red ,"["+str(pr['approvals'])+"/2]" )
                if pr['approvals'] == 1: graphics.DrawText(offscreenCanvas, fontBig, 257-(5*8), 12, orange ,"["+str(pr['approvals'])+"/2]" )
                if pr['approvals'] >= 2: graphics.DrawText(offscreenCanvas, fontBig, 257-(5*8), 12, green ,"["+str(pr['approvals'])+"/2]" )
                offscreenCanvas = self.matrix.SwapOnVSync(offscreenCanvas)
                time.sleep(1) 

        
        def bugsnagOverview(offscreenCanvas):
            Errors = bugsnagCall.getData()
            newErrors = Errors['new']
            openErrors = Errors['open']
            ipErrors = Errors['in_progress']
            ignoredErrors = Errors['ignored']

            offscreenCanvas.Clear()
            drawImage(offscreenCanvas,"./bugsnag.jpg")
            drawSquare(offscreenCanvas,purple)

            label = "New"
            graphics.DrawText(offscreenCanvas, fontBig, 36+(8*len(label)+3), 12, severityColors(newErrors), str(len(newErrors)))
            graphics.DrawText(offscreenCanvas, fontBig, 36, 12, white, label)
            
            label = "In Progress"
            graphics.DrawText(offscreenCanvas, fontBig, 36+(8*len(label)+3), 28, severityColors(ipErrors), str(len(ipErrors)))
            graphics.DrawText(offscreenCanvas, fontBig, 36, 28, white, label)
            
            label = "Open"
            graphics.DrawText(offscreenCanvas, fontBig, width-(8*(len(label)+len(str(len(openErrors)))+1)), 12, severityColors(openErrors), str(len(openErrors)))
            graphics.DrawText(offscreenCanvas, fontBig, width-(8*(len(label))), 12, white, label)

            label = "Ignored"
            graphics.DrawText(offscreenCanvas, fontBig, width-(8*(len(label)+len(str(len(ignoredErrors)))+1)), 28, severityColors(ignoredErrors), str(len(ignoredErrors)))
            graphics.DrawText(offscreenCanvas, fontBig, width-(8*(len(label))), 28, white, label)

            offscreenCanvas = self.matrix.SwapOnVSync(offscreenCanvas)
            time.sleep(5) 
#############################################################################################################################
        offscreenCanvas = self.matrix.CreateFrameCanvas()
        slogansText = slogans[random.randint(0,len(slogans)-1)]
        #
        githubCall.setup()
        bugsnagCall.setup()
        #
        for cnum in xrange(0,2):
            graphics.DrawText(offscreenCanvas, fontBig, 36, 12, green, slogansText)
            graphics.DrawText(offscreenCanvas, fontBig, 34, 26, blue, commands.getoutput('hostname -I'))
            drawSquare(offscreenCanvas,white)
            offscreenCanvas = self.matrix.SwapOnVSync(offscreenCanvas)

        githubLoaded = githubCall.hydrate()
        bugsnagLoaded = bugsnagCall.hydrate()
        while True:
            showGif(offscreenCanvas, "./bear.gif",0.1)
            if githubLoaded == True and bugsnagLoaded == True: break
        while True:
            githubOverview(offscreenCanvas)
            bugsnagOverview(offscreenCanvas)
        


# Main function
if __name__ == "__main__":
    parser = main()
    if (not parser.process()):
            parser.print_help()
