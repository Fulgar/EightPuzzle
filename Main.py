# Course: CS4242
# Student name: Jason James
# Student ID: 000680066
# Assignment #: 2_2
# Due Date: October 18, 2019
# Signature: Jason James
# Score: _________________

from tkinter import *
import random
from Tile import *
import copy
import threading
import time
from State import *

def main():
	# Window Data
	root = Tk()
	root.title("Eight Puzzle")
	root.geometry('750x750')

	# Canvas Data
	canvasHeight = 750
	canvasWidth = 750
	canvas = Canvas(root, height=canvasHeight, width=canvasWidth, bg="gray")

	# Image variables
	img1 = PhotoImage(file="img/1.png")
	img2 = PhotoImage(file="img/2.png")
	img3 = PhotoImage(file="img/3.png")
	img4 = PhotoImage(file="img/4.png")
	img5 = PhotoImage(file="img/5.png")
	img6 = PhotoImage(file="img/6.png")
	img7 = PhotoImage(file="img/7.png")
	img8 = PhotoImage(file="img/8.png")
	imgBLANK = PhotoImage(file="img/BLANK.png")

	imgList = [img1, img2, img3, img4, img5, img6, img7, img8, imgBLANK]

	# Create and run separate thread to execute A* puzzle algorithm while main thread updates Tkinter GUI window
	solveThread = threading.Thread(target=solve, args=(canvas, imgList,))
	solveThread.setDaemon(True)
	solveThread.start()


	# GUI loop
	mainloop()

def solve(canvas, imgList):
	# Grid Lines
	vertLine1 = canvas.create_line(250, 0, 250, 750)
	vertLine2 = canvas.create_line(500, 0, 500, 750)
	hortLine1 = canvas.create_line(0, 250, 750, 250)
	hortLine2 = canvas.create_line(0, 500, 750, 500)

	# Tile Image Canvas Objects
	tileImgObjOne = canvas.create_image(0, 0, anchor=NW, image=imgList[0])
	tileImgObjTwo = canvas.create_image(0, 0, anchor=NW, image=imgList[1])
	tileImgObjThree = canvas.create_image(0, 0, anchor=NW, image=imgList[2])
	tileImgObjFour = canvas.create_image(0, 0, anchor=NW, image=imgList[3])
	tileImgObjFive = canvas.create_image(0, 0, anchor=NW, image=imgList[4])
	tileImgObjSix = canvas.create_image(0, 0, anchor=NW, image=imgList[5])
	tileImgObjSeven = canvas.create_image(0, 0, anchor=NW, image=imgList[6])
	tileImgObjEight = canvas.create_image(0, 0, anchor=NW, image=imgList[7])
	tileImgObjBLANK = canvas.create_image(0, 0, anchor=NW, image=imgList[8])

	tileImgObjList = [tileImgObjOne, tileImgObjTwo, tileImgObjThree, tileImgObjFour, tileImgObjFive, tileImgObjSix,
					  tileImgObjSeven, tileImgObjEight, tileImgObjBLANK]

	# Declaring tile objects
	tileOne = Tile(1, imgList[0], None, None, 1, 1, tileImgObjList[0])
	tileTwo = Tile(2, imgList[1], None, None, 2, 1, tileImgObjList[1])
	tileThree = Tile(3, imgList[2], None, None, 3, 1, tileImgObjList[2])
	tileFour = Tile(4, imgList[3], None, None, 3, 2, tileImgObjList[3])
	tileFive = Tile(5, imgList[4], None, None, 3, 3, tileImgObjList[4])
	tileSix = Tile(6, imgList[5], None, None, 2, 3, tileImgObjList[5])
	tileSeven = Tile(7, imgList[6], None, None, 1, 3, tileImgObjList[6])
	tileEight = Tile(8, imgList[7], None, None, 1, 2, tileImgObjList[7])
	tileBLANK = Tile(0, imgList[8], None, None, 2, 2, tileImgObjList[8])

	tileList = [tileOne, tileTwo, tileThree, tileFour, tileFive, tileSix, tileSeven, tileEight, tileBLANK]

	# Assign random tile positions
	startingPositions = [[1, 1], [1, 2], [1, 3], [2, 1], [2, 2], [2, 3], [3, 1], [3, 2], [3, 3]]
	random.shuffle(startingPositions)
	for tile in tileList:
		startingCoords = startingPositions.pop()
		tile.setCurrentX(startingCoords[0])
		tile.setCurrentY(startingCoords[1])

	canvas.pack()

	# Update GUI to display tiles in their current starting positions
	i = 0
	for tile in tileList:
		updateTileImg(tile, canvas, tileImgObjList)
		i += 1

	# A* Algorithm Starts Here
	g = 0  # Distance from initial state
	h = 0  # Distance from goal state
	openStateList = []
	closedStateList = []
	currentState = State(tileList, g, h, None)
	# While puzzle is not solved
	while isGoalState(tileList) is False:
		shiftingTile = None
		canvas.after(2000)
		# Determine current h value if state is initial state
		if g == 0:
			for tile in tileList:
				# In reality we do not count blank space as a tile so we do not compute its distance
				if tile is not tileBLANK:
					currentX = tile.getCurrentX()
					currentY = tile.getCurrentY()
					goalX = tile.getGoalX()
					goalY = tile.getGoalY()
					h += abs(goalY - currentY) + abs(goalX - currentX)
			currentState.setH(h)

		# Tiles that are adjacent to empty space
		adjacentTiles = getAdjacentTiles(tileBLANK, tileList)

		# Loop through different possible moves and add their states to
		for movingTile in adjacentTiles:
			fakeTileList = copy.deepcopy(tileList)
			fakeBlankTile = fakeTileList[8]
			fakeAdjacentTile = fakeTileList[fakeTileList.index(movingTile)]

			fakeTileList = fakeSwap(fakeBlankTile, fakeAdjacentTile, fakeTileList)
			fakeH = 0
			for fakeTile in fakeTileList:
				# In reality we do not count blank space as a tile so we do not compute its distance
				if fakeTile is not fakeTileList[fakeTileList.index(tileBLANK)]:
					fakeCurrentX = fakeTile.getCurrentX()
					fakeCurrentY = fakeTile.getCurrentY()
					fakeGoalX = fakeTile.getGoalX()
					fakeGoalY = fakeTile.getGoalY()
					fakeH += abs(fakeGoalY - fakeCurrentY) + abs(fakeGoalX - fakeCurrentX)
			print("fakeH = ", str(fakeH))
			fakeState = State(fakeTileList, g + 1, fakeH, movingTile)

			if closedStateList == []:
				openStateList.append(fakeState)
			else:
				for closedState in closedStateList:
					# If fakeState's tileList is the same as one that is in closedState, do not add to openList
					if fakeState.getTileList() is closedState.getTileList():
						pass
					else:
						openStateList.append(fakeState)

		if openStateList == []:
			print("Configuration unsolvable!")
			return
		else:
			minState = currentState
			minF = currentState.getF()
			for openState in openStateList:
				if openState.getF() <= minF:
					minState = openState
					minF = openState.getF()

			closedStateList.append(copy.deepcopy(currentState))

			for openState in openStateList:
				if openState is minState:
					i = 0
					for minStateTile in minState.getTileList():
						minStateTileID = minStateTile.getID()
						currentStateTile = getTileByID(minStateTileID, currentState.getTileList())
						if minStateTile.getCurrentX() != currentStateTile.getCurrentX() or\
								minStateTile.getCurrentY() != currentStateTile.getCurrentY() and minStateTile.getID() != 0:
							shiftingTile = minStateTile
							emptyTile = getTileByID(0, minState.getTileList())
							swap(shiftingTile, emptyTile, canvas, tileImgObjList)
							print(shiftingTile.getID())
						i += 1
					currentState = minState

				else:
					closedStateList.append(copy.deepcopy(openState))
					openStateList.remove(openState)

		h = currentState.getH()
		g = currentState.getG()
		canvas.pack()
	print("Puzzle complete!")

# Returns tile object in given tileList with specific ID number
def getTileByID(ID, tileList):
	for tile in tileList:
		if tile.getID() == ID:
			return tile
	print("ERROR: Could not find tile of ID: ", str(ID))

# Returns a list of all tiles adjacent to tile1
def getAdjacentTiles(tile1, tileList):
	adjacentList = []
	for tile2 in tileList:
		if isAdjacent(tile1, tile2) is True:
			adjacentList.append(tile2)
	return adjacentList


# Returns true if tile1 and tile2 are adjacent to each other
def isAdjacent(tile1, tile2):
	x1 = tile1.getCurrentX()
	y1 = tile1.getCurrentY()
	x2 = tile2.getCurrentX()
	y2 = tile2.getCurrentY()

	if x1 == x2 and abs(y1 - y2) == 1:
		return True
	elif y1 == y2 and abs(x1 - x2) == 1:
		return True
	else:
		return False


# Returns a new tileList without altering the current tileList or GUI
def fakeSwap(tile1, tile2, tileList):
	fakeTileList = copy.deepcopy(tileList)
	fakeTile1 = fakeTileList[fakeTileList.index(tile1)]
	fakeTile2 = fakeTileList[fakeTileList.index(tile2)]

	x1 = copy.deepcopy(fakeTile1.getCurrentX())
	y1 = copy.deepcopy(fakeTile1.getCurrentY())
	x2 = copy.deepcopy(fakeTile2.getCurrentX())
	y2 = copy.deepcopy(fakeTile2.getCurrentY())

	fakeTile1.setCurrentX(x2)
	fakeTile1.setCurrentY(y2)
	fakeTile2.setCurrentX(x1)
	fakeTile2.setCurrentY(y1)

	return fakeTileList


# Swaps the two tiles and updates their GUI position
def swap(tile1, tile2, canvas, tileImgObjList):
	x1 = copy.deepcopy(tile1.getCurrentX())
	y1 = copy.deepcopy(tile1.getCurrentY())
	x2 = copy.deepcopy(tile2.getCurrentX())
	y2 = copy.deepcopy(tile2.getCurrentY())

	tile1.setCurrentX(x2)
	tile1.setCurrentY(y2)
	tile2.setCurrentX(x1)
	tile2.setCurrentY(y1)

	updateTileImg(tile1, canvas, tileImgObjList)
	updateTileImg(tile2, canvas, tileImgObjList)


# Updates GUI position of a tile
def updateTileImg(tile, canvas, tileImgObjList):
	originalTag = copy.deepcopy(tile.getImgObjID())
	canvas.delete(tile.getImgObjID())
	x = (tile.getCurrentX() - 1) * 250
	y = (tile.getCurrentY() - 1) * 250

	tile.setImgObjID(canvas.create_image(x, y, anchor=NW, image=tile.getImage()))
	tileImgObjList[tileImgObjList.index(originalTag)] = tile.getImgObjID()


# Returns true if all tiles in tileList have reached their goal grid coordinates
def isGoalState(tileList):
	for tile in tileList:
		currentX = tile.getCurrentX()
		currentY = tile.getCurrentY()
		goalX = tile.getGoalX()
		goalY = tile.getGoalY()

		if currentX == goalX and currentY == goalY:
			pass
		else:
			return False

	return True


# Run driver program
if __name__ == "__main__":
	main()
