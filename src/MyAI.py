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

# Tile class


class Tile():

    def __init__(self, tile_loc: tuple = (None, None), number: int = None, mine: bool = False, covered: bool = True, flag: bool = False):
        self.mine = mine
        self.covered = covered
        self.flag = flag
        self.number = number
        # Setting the tile id upon creation
        self.loc = tile_loc

    def __repr__(self):
        return f"Mine: {self.mine}, Covered: {self.covered}, Flag: {self.flag}, Number: {self.number}, Loc: {self.loc}\n"


class MyAI(AI):

    def __init__(self, rowDimension, colDimension, totalMines, startX, startY):

        self.__rowDimension = rowDimension
        self.__colDimension = colDimension
        self.__tilesLeft = rowDimension * colDimension - 1
        self.__flagsLeft = totalMines
        self.__totalMines = totalMines
        self.__knownTilesLoc = list()       # Already known tiles
        self.__safeTileLoc = list()         # List of coordinate locations
        self.__flaggedTiles = list()
        self.__curX = startX                # X IS COLUMN
        self.__curY = startY                # Y IS ROW
        self.__tiles = list()

        self.done = False

        # Reverse the range because the row is counted from the bottom
        for row in reversed(range(rowDimension)):
            tileRow = []
            for col in range(colDimension):
                tile = Tile()
                tileRow.append(tile)
            self.__tiles.append(tileRow)

        self.__tiles[startY][startX] = Tile((startX, startY), 0)

    def getAction(self, number: int) -> "Action Object":



        return Action(AI.Action.LEAVE)

    # returns neighbors' locations
    def getNeighbors(self, tile) -> list:

        cur_row = tile.loc[0]
        cur_col = tile.loc[1]
        row_size = len(self.__tiles)
        col_size = len(self.__tiles[0])
        neighbors = list()

        if cur_row != None and cur_col != None:
            for r in range(cur_row - 1, cur_row + 2):
                for c in range(cur_col - 1, cur_col + 2):
                    if -1 < r < row_size and -1 < c < col_size and not (r == cur_row and c == cur_col):
                        neighbors.append( Tile(tile_loc=(r, c)) )   # Add a tile with the tile location

        return neighbors
