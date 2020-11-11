#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import socket
import os
import signal
import sys

from bdffont import *
from matrixbuffer import *
from weather import *

# matrix rows and cols in pixels
MATRIX_ROWS = 7
MATRIX_COLS = 20
RPI_HOSTNAME = "raspberrypi"
FIFO_PATH = "/tmp/matrix.fifo"

# define colors
COLOR_BLACK = (0,0,0)
COLOR_BLUE = (0,0,255)
COLOR_GREEN = (0,255,0)
COLOR_AQUA = (0,255,255)
COLOR_RED = (255,0,0)
COLOR_PURPLE = (255,0,255)
COLOR_YELLOW = (255,255,0)
COLOR_WHITE = (255,255,255)

# set display wrapper to either terminal or neopixel based on hostname
if socket.gethostname() == RPI_HOSTNAME:
	from neopixelwrapper import *
	display_wrapper = NeopixelWrapper()
else:
	from terminalwrapper import *
	display_wrapper = TerminalWrapper()

font = BDFFont("fonts/5x7.bdf")
mb = MatrixBuffer(MATRIX_ROWS, MATRIX_COLS, font, display_wrapper)
weather = Weather()

# create fifo pipe
try:
	os.mkfifo(FIFO_PATH, 0o666)
except OSError:
	pass

loop = True

fifo=open(FIFO_PATH, "r")

# capture kill signal
def signal_term_handler(signal, frame):
	global loop
	loop = False
 
signal.signal(signal.SIGTERM, signal_term_handler)

while loop:

	try:

		mb.clear()
		
		# current temperature
		mb.write_string(weather.get_current_temperature(), COLOR_YELLOW, mb.ALIGN_RIGHT)

		# today high and low
		high, low = weather.get_today_forecast()
		if high != "" and low !="":
			mb.write_string(high + "/" + low + "F", COLOR_YELLOW, mb.ALIGN_LEFT)

		mb.write_string(time.strftime("%-I:%M:%S"), COLOR_WHITE, mb.ALIGN_CENTER)

		mb.show()
		
		time.sleep(1)

		# check if there are any messages in queue
		# scroll if found
		line = fifo.readline()
		if line.strip() != "":
			mb.scroll_string(line[:256], COLOR_PURPLE,.1)
			mb.scroll_string(line[:256], COLOR_GREEN,.1)

	except KeyboardInterrupt:
		break
	
	except:
		pass

# cleanup
mb.clear()
mb.show()
fifo.close()
