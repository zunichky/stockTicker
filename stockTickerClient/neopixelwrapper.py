#!/usr/bin/env python
# -*- coding: utf-8 -*-

import neopixel

class LedConfiguration:

	def __init__(self, GpioPin, Rows, Columns, LedBrightness=1, AutoWrite=False, RgbOrder=neopixel.GRB):
		self.strip = neopixel.NeoPixel(GpioPin, Rows * Columns, brightness=LedBrightness, auto_write=AutoWrite, pixel_order=RgbOrder)
		self.gpioPin = GpioPin
		self.rows = Rows
		self.columns = Columns
		self.brightness = LedBrightness
		self.autoWrite = AutoWrite
		self.rgbOrder = RgbOrder

	def matrix_to_array(self, matrix):
		arr = []
		rows = len(matrix)
		cols = len(matrix[0])
		for r in range(rows):
			for c in range(cols):
				if r % 2 == 1:
					arr.append(matrix[r][c])
				else:
					arr.append(matrix[r][ (self.columns - 1) -c] )

		return arr

	def display(self, matrix):
		arr = self.matrix_to_array(matrix)
		for i in range(len(arr)):
			self.strip[i] = arr[i]

		self.strip.show()



