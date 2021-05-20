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
        if (self.loc == other.loc) and (self.number == other.number):
            return True

        else:
            return False

    # print the tile
    def __repr__(self):
        return f"{self.loc}{self.covered}"
        # return f"Mine: {self.mine}, Covered: {self.covered}, Flag: {self.flag}, Number: {self.number}, Loc: {self.loc}\n"
