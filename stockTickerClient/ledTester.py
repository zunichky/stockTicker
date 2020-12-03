import time
import socket
import os
import signal
import sys

from bdffont import *
from matrixbuffer import *
from ledConfiguration import *
import board

# define colors
COLOR_BLACK = (0,0,0)
COLOR_BLUE = (0,0,255)
COLOR_GREEN = (0,255,0)
COLOR_AQUA = (0,255,255)
COLOR_RED = (255,0,0)
COLOR_PURPLE = (255,0,255)
COLOR_YELLOW = (255,255,0)
COLOR_WHITE = (255,255,255)
COLOR_LIGHTPINK = (255,182,193)

def main():
    print("----------------------------------------")
    print("Testing scrolling while live adding text")
    print("----------------------------------------")
    display_wrapper = LedConfiguration(board.D18, 8, 75, .1, False, neopixel.GRB)
    font = BDFFont("fonts/5x7.bdf")
    mb = MatrixBuffer(display_wrapper, font)
    

    useLocal = False
    if (useLocal):
        scroll = InfiniteScroll(mb, .04)
        print("Adding text HELLO WORLD in Yellow")
        scroll.addText("HELLO WORLD", COLOR_YELLOW)
        scroll.start()
        #This sleep is only used as an easy way to scroll through the whole text
        #before adding the new text. The real user should not use a blocking call
        # while waiting for text 
        time.sleep(10)
        print("Adding text NEW TEXT in Aqua")
        scroll.addText("NEW TEXT", COLOR_AQUA)
        time.sleep(10)
        scroll.stop()

        time.sleep(1)
        mb.clear()
        mb.show()
    else:
        #echo "TEXT&(255,255,0)" > input.txt 
        #echo "CLEAR&(255,0,0)" > input.txt 
        #echo "CLEARWAIT&(255,255,0)" > input.txt 
        
        cached_stamp = 0
        inputFile = "/home/pi/stockTicker/stockTickerClient/input.txt"
        scroll = InfiniteScroll(mb, .04)
        scroll.start()
        while (scroll.running):
            stamp = os.stat(inputFile).st_mtime
            if stamp != cached_stamp:
                cached_stamp = stamp
                with open(inputFile, 'r') as reader:
                    for line in reader:
                        line = line.strip()
                        splitList = line.split('&')
                        if (splitList[0].lower() == "clear"):
                            #scroll.clearText()
                            scroll.clearAndAddText("CLEAR", (255,255,255))
                        elif (splitList[0].lower() == "clearwait"):
                            #scroll.clearText(True)
                            scroll.clearAndAddText("NEW", (255,255,255), True)
                        elif (splitList[0].lower() == "end"):
                            scroll.stop()
                        else:
                            scroll.addText(splitList[0], eval(splitList[1]))
                time.sleep(1)


if __name__ == "__main__":
    main()