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
from collections import Counter


class Tile():

    def __init__(self, loc: tuple = (None, None), number: int = '.', mine: bool = False, covered: bool = True, flag: bool = False):
        self.mine = mine
        self.covered = covered
        self.flag = flag
        self.number = number
        # Setting the tile id upon creation
        self.loc = loc

    def getLoc(self):
        return self.loc
    
    def setLoc(self, loc: tuple):
        self.loc = loc

    def getNumber(self) -> int:
        return self.number

    def setNumber(self, num: int):
        self.number = num

    def isMine(self) -> bool:
        return self.mine
    
    def setMine(self, mine: bool):
        self.mine = mine

    def isCovered(self) -> bool:
        return self.covered

    def coverTile(self):
        self.covered = True
    
    def uncoverTile(self):
        self.covered = False

    def isFlagged(self):
        return self.flag

    def flagTile(self):
        self.flag = True

    def unflagTile(self):
        self.flag = False

    # print the tile
    def __repr__(self):
        # return f"{self.number}"
        return f"{self.loc}{self.number}"
        # return f"Mine: {self.mine}, Covered: {self.covered}, Flag: {self.flag}, Number: {self.number}, Loc: {self.loc}\n"

class Equation:
    def __init__(self, variables=list(), number=0):
        self.variables = variables
        self.number = number

    def __repr__(self):
        return f"{self.variables} {self.number}"

    def __eq__(self, other):
        def compare(x, y): return Counter(x) == Counter(y)
        if compare(self.variables, other.variables) and self.number == other.number:
            # if self.variables == other.variables and self.number == other.number:
            return True

        else:
            return False

    def compare(self, other_eq):
        eq = Equation()

        eq1 = self
        eq2 = other_eq

        if set(eq1.variables).issubset(set(eq2.variables)):
            eq.variables = list(set(eq2.variables) - set(eq1.variables))
            eq.number = eq2.number - eq1.number

        return eq

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
        self.__flagTiles = list()
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

        # Uncover all the safe tiles
        if self.__safeTiles:
            self.__curTile = self.__safeTiles.pop()
            self.exploreTile(self.__curTile)

            return Action(AI.Action.UNCOVER, self.__curTile.loc[0], self.__curTile.loc[1])

        elif self.__flagTiles:
            self.__curTile = self.__flagTiles.pop()
            self.exploreTile(self.__curTile)

            return Action(AI.Action.FLAG, self.__curTile.loc[0], self.__curTile.loc[1])

        # No more safe tiles
        else:
            for tile in self.__exploredTiles:
                if tile.getNumber() > 0:
                    covered_tiles = self.getCoveredTiles(tile)
                    flagged_tiles = self.getFlaggedTiles(tile)

                    if tile.getNumber() == len(covered_tiles) + len(flagged_tiles) and len(covered_tiles) != 0:

                        self.__curTile = covered_tiles.pop()
                        self.exploreTile(self.__curTile)

                        return Action(AI.Action.FLAG, self.__curTile.loc[0], self.__curTile.loc[1])

                    else:

                        if tile.getNumber() == len(flagged_tiles) and len(covered_tiles) != 0:
                            self.__safeTiles.extend(covered_tiles)
                            self.__curTile = self.__safeTiles.pop()
                            self.exploreTile(self.__curTile)

                            return Action(AI.Action.UNCOVER, self.__curTile.loc[0], self.__curTile.loc[1])

        #####################################################
        ############### PUT CSP LOGIC IN HERE ###############
        #####################################################

        eqs = list()

        for tile in self.__exploredTiles:
            frontier = False
            flag_count = 0
            neighbors = self.getNeighbors(tile)
            variables = list()

            for neighbor in neighbors:
                if neighbor.getNumber() == '.':
                    frontier = True
                    variables.append(neighbor)

                if neighbor.getNumber() == -1:
                    flag_count += 1

            if frontier and tile.getNumber() != -1:
                eq = Equation(variables, tile.getNumber() - flag_count)
                eqs.append(eq)

        eqs = self.runCSP(eqs)
        extracted = self.extractEqs(eqs)

        for eq in extracted:
            if eq.number == 1:
                self.__flagTiles.extend(eq.variables)

            elif eq.number == 0:
                self.__safeTiles.extend(eq.variables)

        if self.__safeTiles:
            self.__curTile = self.__safeTiles.pop()
            self.exploreTile(self.__curTile)

            return Action(AI.Action.UNCOVER, self.__curTile.loc[0], self.__curTile.loc[1])

        ######################################################
        ######################################################
        ######################################################

        if self.checkWinningStatus():
            return Action(AI.Action.LEAVE)

        # Random move
        if not self.__safeTiles:
            action = AI.Action.UNCOVER
            self.__curTile = random.choice(self.__unexploredTiles)
            self.exploreTile(self.__curTile)

            return Action(action, self.__curTile.loc[0], self.__curTile.loc[1])

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
                    if -1 < x < col_size and -1 < y < row_size and not (x == cur_x and y == cur_y):
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

    def runCSP(self, eqs):

        for eq1 in eqs:
            for eq2 in eqs:

                eq = eq1.compare(eq2)

                if eq not in eqs and eq.variables:
                    eqs.append(eq)

                if len(eq.variables) == eq.number:
                    for i in range(len(eq.variables)):
                        eq_new = Equation([eq.variables[i]], 1)
                        if eq_new not in eqs and eq_new.variables:
                            eqs.append(eq_new)

                if len(eq.variables) > 0 and eq.number == 0:
                    for i in range(len(eq.variables)):
                        eq_new = Equation([eq.variables[i]], 0)
                        if eq_new not in eqs and eq_new.variables:
                            eqs.append(eq_new)

        return eqs

    def extractEqs(self, eqs):
        extracted = list()
        for eq in eqs:
            if len(eq.variables) == 1:
                extracted.append(eq)

        return extracted
