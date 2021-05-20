# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

import random
from AI import AI
from Action import Action

#########################################################################
from icecream import ic #################################################
from Tile import Tile####################################################
################# Make sure to put back Tile class here #################
#########################################################################

class MyAI(AI):

    ######################################################################
    ################# STORE LOCATIONS OF TILES AS (X, Y) #################
    ################# BUT INSIDE THE self.__tiles STORE  #################
    ################# IT AS (Y, X) TO MAKE IT EASY TO    #################
    ################# VISUALIZE                          #################
    ######################################################################

    def __init__(self, rowDimension, colDimension, totalMines, startX, startY):

        self.__rowDimension = rowDimension
        self.__colDimension = colDimension
        self.__tilesLeft = rowDimension * colDimension - 1
        self.__flagsLeft = totalMines
        self.__totalMines = totalMines
        self.__exploredTiles = list()       # Already explored tiles
        self.__unexploredTiles = list()     # Not yet explored
        self.__safeTiles = list()           # List of coordinate locations
        self.__flaggedTiles = list()
        self.__curX = startX                # X IS COLUMN
        self.__curY = startY                # Y IS ROW
        self.__tiles = list()

        self.done = False

        # Every tile is UNEXPLORED yet
        for row in self.__tiles:
            for tile in row:
                self.__unexploredTiles.append(tile)

        # Reverse the range because the row is counted from the bottom
        for row in reversed(range(rowDimension)):
            tileRow = list()
            for col in range(colDimension):
                tile = Tile(loc=(col, row))
                tileRow.append(tile)
            self.__tiles.append(tileRow)

        # The first tile starts at the given position. The tile is safe. It gets a number of 0
        startTile = Tile(loc=(startX, startY), number=0, covered=False)
        self.__tiles[startY][startX] = startTile

        # The first tile is explored
        self.exploreTile(startTile)

        # Set the safe tiles around the first tile that's given
        self.__safeTiles.append(self.getNeighbors(startTile))

    def getAction(self, number: int) -> "Action Object":

        self.printBoard()
        # self.uncoverSafeTiles()

        ic(self.__exploredTiles)
        ic(self.__safeTiles)

        return Action(AI.Action.LEAVE)

    # returns neighbors' locations
    def getNeighbors(self, tile) -> list:

        cur_x = tile.loc[0]
        cur_y = tile.loc[1]
        row_size = len(self.__tiles)
        col_size = len(self.__tiles[0])
        neighbors = list()

        if cur_x != None and cur_y != None:
            for x in range(cur_x - 1, cur_x + 2):
                for y in range(cur_y - 1, cur_y + 2):
                    if -1 < x < row_size and -1 < y < col_size and not (x == cur_x and y == cur_y):
                        neighbors.append( Tile(loc=(x, y)) )   # Add a tile with the tile location

        return neighbors

    # print the board
    def printBoard(self):
        ic(self.__tiles)

    # if the tile has a number of 0 add the neighboring tiles to the safe tile list.
    # Also, when the tile is explored, make sure to add that tile to the explored tile list.
    def uncoverSafeTiles(self):
        pass


    def exploreTile(self, explored_tile):
        self.__exploredTiles.append(explored_tile)

        for tile in self.__unexploredTiles:
            if tile == explored_tile:
                self.__unexploredTiles.remove(explored_tile)