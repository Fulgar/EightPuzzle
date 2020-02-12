# Course: CS4242
# Student name: Jason James
# Student ID: 000680066
# Assignment #: 2_2
# Due Date: October 18, 2019
# Signature: Jason James
# Score: _________________

class State:

	def __init__(self, tileList, g, h, movedTile):
		self.tileList = tileList
		self.g = g
		self.h = h
		self.movedTile = movedTile

	def getTileList(self):
		return self.tileList

	def setTileList(self, tileList):
		self.tileList = tileList

	def getG(self):
		return self.g

	def setG(self, g):
		self.g = g

	def getH(self):
		return self.h

	def setH(self, h):
		self.h = h

	def getF(self):
		if self.g is not None and self.h is not None:
			return int(self.g + self.h)
