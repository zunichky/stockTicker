#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import socket
import os
import signal
import sys
from ledConfiguration import *
import board
import neopixel
import matrixbuffer
import weather

from bdffont import *

# matrix rows and cols in pixels
MATRIX_ROWS = 8
MATRIX_COLS = 75
RPI_HOSTNAME = "raspberrypi"
FIFO_PATH = "/tmp/matrix.fifo"
LED_PIN        = board.D18  # GPIO pin connected to the pixels (18 uses PWM!).
LED_BRIGHTNESS = .2         # Set to 0 for darkest and 1 for brightest
# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
LED_ORDER = neopixel.GRB
AUTO_WRITE = False

# define colors
COLOR_BLACK = (0,0,0)
COLOR_BLUE = (0,0,255)
COLOR_GREEN = (0,255,0)
COLOR_AQUA = (0,255,255)
COLOR_RED = (255,0,0)
COLOR_PURPLE = (255,0,255)
COLOR_YELLOW = (255,255,0)
COLOR_WHITE = (255,255,255)

configuration = LedConfiguration(LED_PIN, MATRIX_ROWS, MATRIX_COLS, LED_BRIGHTNESS, AUTO_WRITE, LED_ORDER)

# set display wrapper to either terminal or neopixel based on hostname
'''
if socket.gethostname() == RPI_HOSTNAME:
	from ledConfiguration import *
	
else:
	from terminalwrapper import *
	configuration = TerminalWrapper()
'''

font = BDFFont("fonts/5x7.bdf")
mb = matrixbuffer.MatrixBuffer(configuration, font)
#weather = weather.Weather()

# create fifo pipe
'''
try:
	os.mkfifo(FIFO_PATH, 0o666)
except OSError:
	pass
'''
loop = True

#fifo=open(FIFO_PATH, "r")

# capture kill signal
def signal_term_handler(signal, frame):
	global loop
	loop = False
 
signal.signal(signal.SIGTERM, signal_term_handler)

while loop:

	try:

		mb.clear()
		'''
		# current temperature
		mb.write_string(weather.get_current_temperature(), COLOR_YELLOW, mb.ALIGN_RIGHT)

		# today high and low
		high, low = weather.get_today_forecast()
		if high != "" and low !="":
			mb.write_string(high + "/" + low + "F", COLOR_YELLOW, mb.ALIGN_LEFT)

		mb.write_string(time.strftime("%-I:%M:%S"), COLOR_WHITE, mb.ALIGN_CENTER)
		'''

		mb.write_string("HI", COLOR_BLUE, mb.ALIGN_CENTER)

		mb.show()
		time.sleep(3)


		mb.scroll_string("HIII", COLOR_RED, delay=.02, startAtBeginning=True, blink=False)

		mb.show()

		#mb.write_string("PENN: $63.31", COLOR_GREEN, matrixbuffer.MatrixBuffer.ALIGN_CENTER)
		#mb.show()
		
		time.sleep(1)

		# check if there are any messages in queue
		# scroll if found
		'''
		line = fifo.readline()
		if line.strip() != "":
			mb.scroll_string(line[:256], COLOR_PURPLE,.1)
			mb.scroll_string(line[:256], COLOR_GREEN,.1)
			'''

	except KeyboardInterrupt:
		break
	
	except:
		pass

# cleanup
mb.clear()
mb.show()
#fifo.close()
