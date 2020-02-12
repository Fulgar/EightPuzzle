# Course: CS4242
# Student name: Jason James
# Student ID: 000680066
# Assignment #: 2_2
# Due Date: October 18, 2019
# Signature: Jason James
# Score: _________________

from copy import deepcopy

class Tile:

	def __init__(self, ID, image, currentX, currentY, goalX, goalY, imgObjID):
		self.ID = ID
		self.image = image
		self.currentX = currentX
		self.currentY = currentY
		self.goalX = goalX
		self.goalY = goalY
		self.imgObjID = imgObjID


	def __eq__(self, other):
		return self.ID == other.ID

	def __deepcopy__(self, memo):
		ID = deepcopy(self.ID)
		currentX = deepcopy(self.currentX)
		currentY = deepcopy(self.currentY)
		goalX = deepcopy(self.goalX)
		goalY = deepcopy(self.goalY)
		imgObjID = deepcopy(self.imgObjID)
		return Tile(ID, self.image, currentX, currentY, goalX, goalY, imgObjID)

	def getID(self):
		return self.ID

	def getImage(self):
		return self.image

	def setImage(self, image):
		self.image = image

	def getCurrentX(self):
		return self.currentX

	def setCurrentX(self, currentX):
		self.currentX = currentX

	def getCurrentY(self):
		return self.currentY

	def setCurrentY(self, currentY):
		self.currentY = currentY

	def getGoalX(self):
		return self.goalX

	def setGoalX(self, goalX):
		self.goalX = goalX

	def getGoalY(self):
		return self.goalY

	def setGoalY(self, goalY):
		self.goalY = goalY

	def getImgObjID(self):
		return self.imgObjID

	def setImgObjID(self, imgObjID):
		self.imgObjID = imgObjID
