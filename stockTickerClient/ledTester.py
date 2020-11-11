import time
import socket
import os
import signal
import sys

from bdffont import *
from matrixbuffer import *
from neopixelwrapper import *

# define colors
COLOR_BLACK = (0,0,0)
COLOR_BLUE = (0,0,255)
COLOR_GREEN = (0,255,0)
COLOR_AQUA = (0,255,255)
COLOR_RED = (255,0,0)
COLOR_PURPLE = (255,0,255)
COLOR_YELLOW = (255,255,0)
COLOR_WHITE = (255,255,255)



def main():
    display_wrapper = NeopixelWrapper()
    font = BDFFont("fonts/5x7.bdf")
    mb = MatrixBuffer(7, 20, font, display_wrapper)
    
    mb.write_char(0,0,'I',COLOR_RED )
    mb.show()
    time.sleep(10)
    mb.clear()
    mb.show()

if __name__ == "__main__":
    main()



