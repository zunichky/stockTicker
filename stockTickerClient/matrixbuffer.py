#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Matrix Buffer to compute output
"""

import time
import math

import threading
import collections

class MatrixBuffer:

	ALIGN_LEFT   = -1
	ALIGN_CENTER = 0
	ALIGN_RIGHT  = 1

	def __init__(self, ledConfiguration, font, char_spacing=0):
		self.rows = ledConfiguration.rows
		self.cols = ledConfiguration.columns
		self.font = font
		self.ledConfiguration = ledConfiguration
		self.charSpacing = char_spacing
		self.displayDeque= collections.deque()
		
		self.matrix = [[0 for c in range(self.cols)] for r in range(self.rows)]

	def get_rows(self):
		return self.rows

	def get_cols(self):
		return self.cols

	def get_matrix(self):
		return self.matrix

	def write_pixel(self, r, c, value):
		if r >= 0 and r < self.rows and c >=0 and c < self.cols:
			self.matrix[r][c] = value

	def write_char(self, r, c, char, color):
		char_data = self.font.get_char(char)
		row = r
		for n in char_data:
			col = c
			for p in list(bin(n)[2:].zfill(8)):
				if p == '0':
					self.write_pixel(row, col, (0,0,0))
				else:
					self.write_pixel(row, col, color)
					
				col = col + 1
			row = row + 1

	def write_deque_at(self, row, col, str):
		#TODO: CHANGE ME ONCE FIXED. I'm adding a row to center the text
		row = row + 1
		for c in str:
			self.write_char(row, col, c[0], c[1])
			col = col + self.font.get_width() + self.charSpacing

	def write_string_at(self, row, col, str, color):
		#TODO: CHANGE ME ONCE FIXED. I'm adding a row to center the text
		row = row + 1
		for c in str:
			self.write_char(row, col, c, color)
			col = col + self.font.get_width() + self.charSpacing

	def write_string(self, str, color, align=ALIGN_LEFT):		
		if len(str) > self.cols:
			str = str[0:self.cols]

		if align == self.ALIGN_LEFT:
			self.write_string_at(0, 1, str, color)
		elif align == self.ALIGN_RIGHT:
			self.write_string_at(0, self.cols - len(str) * (self.font.get_width() + self.charSpacing), str, color)
		elif align == self.ALIGN_CENTER:
			self.write_string_at(0, int( (self.cols - len(str) * (self.font.get_width() + self.charSpacing)) / 2 ), str, color )

	def scroll_string(self, inputStr, color, delay=0.01, startAtBeginning=True, blink=False):
		if (startAtBeginning == True):
			offsetBeginning = math.ceil(self.cols / self.font.get_width())
			#add spaces in front of text to make sure the text is on the far right side
			inputStr = (' ' * offsetBeginning) + inputStr
			
		# start scrolling
		self.clear()
		for st in range(len(inputStr)):
			timeToBlink = 0
			for offset in range(self.font.get_width() + self.charSpacing):
				#self.clear()
				if ( not blink or timeToBlink < 2):
					self.write_string_at(0, -offset, inputStr[st:], color)
					if (blink):
						timeToBlink += 1
				else:
					#want to blink for 2 iterations, while keeping the txt scrolling
					if (timeToBlink == 3):
						timeToBlink = 0
					else:
						timeToBlink += 1

				self.show()
				time.sleep(delay)

		self.clear()
		self.show()

	def clear(self):
		for r in range(self.rows):
			for c in range(self.cols):
				self.matrix[r][c] = 0

	def show(self):
		self.ledConfiguration.display(self.matrix)

class InfiniteScroll:
		def __init__(self, matrixBuffer, delay = .01):
			self.displayText = list()
			self.running = False
			self.matrixBuffer = matrixBuffer
			self.delay = delay
			self.color = (255,0,0)
			self.spliceCount = 0
		
		def addText(self, text, color):
			for x in text:
				self.displayText.append((x, color))
			self.displayText.append((' ', (0,0,0)))
		
		def start(self):
			self.thread = threading.Thread(target=self._infiniteRunningWithColor)
			self.running = True
			self.thread.start()

		def stop(self):
			self.running = False
			self.clearLiveTextBuffer()

		def clearText(self):
			self.displayText = list()
			self.clearLiveTextBuffer()
			self.spliceCount = 0
		
		def clearAndAddText(self, text, color, waitForTextToFinsh = False):
			if (waitForTextToFinsh):
				self.waitForFinish()
			self.spliceCount = 0
			self.displayText = list()
			self.addText(text, color)

		def clearLiveTextBuffer(self):
			offsetBeginning = math.ceil(self.matrixBuffer.cols / self.matrixBuffer.font.get_width())
			#add spaces in front of text to make sure the text is on the far right side
			self.displayDeque= collections.deque(maxlen=offsetBeginning)
			for x in range(offsetBeginning):
				self.displayDeque.append((' ',(0,0,0)))
		
		def waitForFinish(self):
			#TODO: rewrite for a more clever way
			#Using events would be nice
			while (self.spliceCount != 0):
				time.sleep(.1)

		def _infiniteRunningWithColor(self):
			self.matrixBuffer.clear()
			self.clearLiveTextBuffer()
			
			self.spliceCount = 0

			while (self.running):
				for offset in range(self.matrixBuffer.font.get_width() + self.matrixBuffer.charSpacing):
					self.matrixBuffer.write_deque_at(0, -offset, self.displayDeque )
					self.matrixBuffer.show()
					time.sleep(self.delay)

				if (len(self.displayText) > 0):
					self.displayDeque.append(self.displayText[self.spliceCount])
				else:
					self.displayDeque.append((' ', (0,0,0 )))
					
				self.spliceCount = self.spliceCount + 1
				if (self.spliceCount >= len(self.displayText)):
					self.spliceCount = 0

			self.matrixBuffer.clear()
			self.matrixBuffer.show()