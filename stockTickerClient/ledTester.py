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

if __name__ == "__main__":
    main()



