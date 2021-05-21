

class Tile():

    def __init__(self, loc: tuple = (None, None), number: int = None, mine: bool = False, covered: bool = True, flag: bool = False):
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

    # overload equation operation
    def __eq__(self, other):
        if (self.loc == other.loc):
            return True

        else:
            return False

    # print the tile
    def __repr__(self):
        # return f"{self.loc} {1 if self.covered else 0}"
        return f"{self.loc} {1 if self.covered else 0} {self.number}"
        # return f"Mine: {self.mine}, Covered: {self.covered}, Flag: {self.flag}, Number: {self.number}, Loc: {self.loc}\n"

# ic| tile: (0, 1) 0 0
# ic| tile: (1, 2) 0 0
# ic| tile: (2, 3) 0 1
# ic| tile: (2, 2) 0 1
# ic| tile: (2, 1) 0 0
# ic| tile: (3, 2) 0 1
# ic| tile: (3, 1) 0 0
# ic| tile: (4, 2) 0 1
# ic| tile: (4, 1) 0 0
# ic| tile: (4, 0) 0 0
# ic| tile: (3, 0) 0 0
# ic| tile: (2, 0) 0 0
# ic| tile: (1, 3) 0 0
# ic| tile: (2, 4) 0 1
# ic| tile: (1, 4) 0 0
# ic| tile: (0, 4) 0 0
# ic| tile: (0, 3) 0 0
# ic| tile: (1, 1) 0 0
# ic| tile: (1, 0) 0 0
# ic| tile: (0, 2) 0 0
# ic| tile: (0, 0) 0 0