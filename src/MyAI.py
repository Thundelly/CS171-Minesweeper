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
from pprint import pprint
from icecream import ic
from Tile import Tile
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
        self.__safeTiles = list()  # List of coordinate locations
        self.__mines = list()
        self.__flaggedTiles = list()
        self.__curTile = Tile()             # Current tile of focus / X IS COLUMN / Y IS ROW
        self.__tiles = list()

        # Reverse the range because the row is counted from the bottom
        for row in reversed(range(rowDimension)):
            tileRow = list()
            for col in range(colDimension):
                tileRow.append(Tile(loc=(col, row)))
            self.__tiles.append(tileRow)

        # Every tile is UNEXPLORED yet
        for row in self.__tiles:
            for tile in row:
                self.__unexploredTiles.append(tile)

        # The first tile starts at the given position. The tile is safe. It gets a number of 0
        self.__startTile = Tile(loc=(startX, startY), number=0, covered=False)
        self.__tiles[self.__rowDimension - 1 -
                     startY][startX] = self.__startTile
        self.__curTile = self.__startTile
        self.exploreTile(self.__curTile)

    def getAction(self, cur_tile_number: int) -> "Action Object":

        self.__curTile.setNumber(cur_tile_number)
        self.findSafeTiles(self.__curTile)

        # ic(self.__curTile)
        # ic(self.__safeTiles)

        # Uncover all the safe tiles
        if self.__safeTiles:
            self.__curTile = self.__safeTiles.pop()
            self.exploreTile(self.__curTile)

            # self.printBoard()
            return Action(AI.Action.UNCOVER, self.__curTile.loc[0], self.__curTile.loc[1])

        # No more safe tiles
        else:
            for tile in self.__exploredTiles:
                if tile.getNumber() > 0:
                    covered_tiles = self.getCoveredTiles(tile)
                    flagged_tiles = self.getFlaggedTiles(tile)

                    # ic(tile)
                    # ic(covered_tiles)
                    # ic(flagged_tiles)

                    if tile.getNumber() == len(covered_tiles) + len(flagged_tiles) and len(covered_tiles) != 0:
                        # ic(True)

                        self.__curTile = covered_tiles.pop()
                        self.exploreTile(self.__curTile)

                        return Action(AI.Action.FLAG, self.__curTile.loc[0], self.__curTile.loc[1])

                    else:
                        # ic(False)

                        if tile.getNumber() == len(flagged_tiles) and len(covered_tiles) != 0:
                            self.__safeTiles.extend(covered_tiles)

                            return Action(AI.Action)


        #####################################################
        ############### PUT CSP LOGIC IN HERE ###############
        #####################################################



        ######################################################
        ######################################################
        ######################################################
        
        if self.checkWinningStatus():
            return Action(AI.Action.LEAVE)
        # self.printBoard()


        # Random move
        if not self.__safeTiles:
            action = AI.Action.UNCOVER
            x = random.randrange(self.__colDimension)
            y = random.randrange(self.__rowDimension)

            return Action(action, x, y)

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
                        neighbors.append(
                            self.__tiles[self.__rowDimension - 1 - y][x])

        return neighbors

    def getCoveredTiles(self, tile):
        filtered = list()
        neighbors = self.getNeighbors(tile)

        for tile in neighbors:
            if tile.getNumber() == '.':
                filtered.append(tile)

        return filtered

    def getFlaggedTiles(self, tile):
        filtered = list()
        neighbors = self.getNeighbors(tile)

        for tile in neighbors:
            if tile.getNumber() == -1:
                filtered.append(tile)

        return filtered

    def checkWinningStatus(self):
        mine_count = 0
        for row in self.__tiles:
            for tile in row:
                if tile.getNumber() == -1:
                    mine_count += 1
    
        return mine_count == self.__totalMines

    # print the board
    def printBoard(self):
        # ic(self.__tiles)
        pprint(self.__tiles, width=120)
        pass

    def findSafeTiles(self, tile):

        if tile.getNumber() == 0:
            self.__safeTiles.extend(tile for tile in self.getNeighbors(
                tile) if tile not in self.__safeTiles and tile not in self.__exploredTiles)

        # Update the tile info
        tile.uncoverTile()
        self.__tiles[self.__rowDimension - 1 - tile.loc[1]][tile.loc[0]] = tile

    def exploreTile(self, tile):
        try:
            self.__exploredTiles.append(tile)
            self.__unexploredTiles.remove(tile)

        except ValueError:
            pass
