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
        self.__knownTilesLoc = list()       # Already known tiles
        self.__safeTilesLoc = list()         # List of coordinate locations
        self.__1TilesLoc = list()
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

        if number == 0:
            self.__safeTilesLoc.extend(loc for loc in self.getNeighbors(
                (self.__curX, self.__curY)) if loc not in self.__safeTilesLoc and loc not in self.__knownTilesLoc)
        
        elif number == 1:
            self.__1TilesLoc.append((self.__curX,self.__curY))

        # Keep track of the tiles by adding to a separate list

        self.__tiles[self.__curX][self.__curY] = (
            Tile((self.__curX, self.__curY), number, False, False, False))

        if self.__safeTilesLoc:

            safeTile = self.__safeTilesLoc.pop()
            self.__curX = safeTile[0]
            self.__curY = safeTile[1]

            # Uncover the safe tile
            action = Action(AI.Action.UNCOVER, self.__curX, self.__curY)
            self.__tilesLeft -= 1
            # Add to the known tile
            self.__knownTilesLoc.append((self.__curX, self.__curY))

            print (self.__knownTilesLoc)
            print (self.__safeTilesLoc)
            print (self.__1TilesLoc)
            return action

        elif self.__1TilesLoc:
            for testTile in self.__1TilesLoc:
                print(testTile)
                confirmedBombs = self.remainingTilesLogic((testTile[0], testTile[1]), 1)
                if confirmedBombs:
                    self.__1TilesLoc.remove(testTile)
                    action = Action(AI.Action.FLAG, confirmedBombs[0][0], confirmedBombs[0][1])
                    self.__knownTilesLoc.append((confirmedBombs[0][0], confirmedBombs[0][1]))
                    self.__tilesLeft -= 1
                    return action

        else:
            action = AI.Action.UNCOVER
            x = random.randrange(self.__colDimension)
            y = random.randrange(self.__rowDimension)

            return Action(action, x, y)

        return Action(AI.Action.LEAVE)

    # returns neighbors' locations
    def getNeighbors(self, tileLoc: tuple) -> list:

        cur_row = tileLoc[0]
        cur_col = tileLoc[1]
        row_size = len(self.__tiles)
        col_size = len(self.__tiles[0])
        neighborsLoc = list()

        if cur_row != None and cur_col != None:
            for r in range(cur_row - 1, cur_row + 2):
                for c in range(cur_col - 1, cur_col + 2):
                    if -1 < r < row_size and -1 < c < col_size and not (r == cur_row and c == cur_col):
                        neighborsLoc.append((r, c))

        return neighborsLoc

    def remainingTilesLogic(self, tileLoc: tuple, numBombs: int) -> list:
        
        counter = 0
        bombList = list()
        if tileLoc[0] != None and tileLoc[1] != None:
            for r in range(tileLoc[0] - 1, tileLoc[0] + 2):
                for c in range(tileLoc[1] - 1, tileLoc[1] + 2):
                    if -1 < r < self.__rowDimension and -1 < c < self.__colDimension and not (r == tileLoc[0] and c == tileLoc[1]):
                        if self.__tiles[r][c].covered == True:
                            counter += 1
                            bombList.append((r,c))
                            if counter > numBombs:
                                return            
        if counter < numBombs:
            print ("somethings fucked")
        if counter == numBombs:
            return bombList