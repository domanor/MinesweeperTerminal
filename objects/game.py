from .cell import Cell
from .tag import Tag
import random


class SaperTerminal:

    def __init__(self, countColumn, countLine, countMine):
        if countColumn * countLine > 200: 
            raise Exception("field too big")

        self.running = True
        self.countLine = countLine
        self.countColumn = countColumn
        self.countMine = countMine
        self.countOpenCell = 0

        self.field = []
        for y in range(countLine):
            for x in range(countColumn):
                self.field.append(Cell((x, y)))

    def move(self, positionMove, action):
        if positionMove[0] >= self.countColumn or positionMove[1] >= self.countLine:
            return

        indCell = positionMove[0] + self.countColumn * positionMove[1]
        cell = self.field[indCell]
        
        if cell.clicked: 
            return

        if action == "-o":
            if cell.isMine():
                self.stop("loss")
                return

            neighbors, countMinesNear = self.getNeighbors(indCell)
            cell.openSelf(countMinesNear=countMinesNear)

            if countMinesNear == 0:
                self.openNeighboringEmptyCells(cell)

            self.checkWin()

        elif action == "-f":
            cell.putSomething(Tag.FLAG)

        elif action == "-q":
            cell.putSomething(Tag.QUESTION)

        elif action == "-c":
            cell.putSomething(Tag.NOTHING)

    def printField(self):
        print(end="   ")
        for col in range(self.countColumn): 
            print(f"{' '}{col + 1}{' ' * (0 if col // 9 else 1)}", end="")
        
        print()

        for cell in self.field:
            if cell.position[0] == 0:
                row = cell.position[1]
                print(f"{' ' * (0 if row // 9 else 1)}{row + 1}{' '}", end="")

            print(cell, end="")

            if cell.position[0] == self.countColumn - 1:
                print()

    def generateField(self, firstMove=None):
        neighbors = []
        if firstMove:
            indFirstMove = firstMove[0] + self.countColumn * firstMove[1]
            neighbors = self.getNeighbors(indFirstMove, getCountMinesNear=False)
        
        nowCountMine = 0

        while nowCountMine < self.countMine:
            randomPosition = (
                random.randint(0, self.countColumn - 1), 
                random.randint(0, self.countLine - 1))

            indRandomCell = randomPosition[0] + self.countColumn * randomPosition[1]
            randomCell = self.field[indRandomCell]

            if (randomPosition == firstMove) or (randomCell in neighbors) or randomCell.isMine():
                continue

            randomCell.doSelfMine()
            nowCountMine += 1   

    def getNeighbors(self, indCell, getCountMinesNear=True):
        row, col = divmod(indCell, self.countColumn)
        neighbors = []
        countMinesNear = 0

        for j in range(col - 1, col + 2):
            for i in range(row - 1, row + 2):
                if 0 <= i < self.countLine and 0 <= j < self.countColumn and (i != row or j != col):
                    cell = self.field[i * self.countColumn + j]
                    neighbors.append(cell)

                    if cell.isMine():
                        countMinesNear += 1

        if getCountMinesNear:
            return neighbors, countMinesNear

        else:
            return neighbors

    def checkWin(self):
        for cell in self.field:
            if not cell.clicked and not cell.isMine(): 
                return

        self.stop("win")

    def openNeighboringEmptyCells(self, mainCell):
        indMainCell = mainCell.position[0] + self.countColumn * mainCell.position[1]
        neighbors, countMinesNear = self.getNeighbors(indMainCell)
        mainCell.openSelf(countMinesNear=countMinesNear)

        if countMinesNear != 0:
            return 
    
        for cell in neighbors:
            if cell.clicked: 
                continue

            self.openNeighboringEmptyCells(cell)

    def stop(self, result=None):
        for cell in self.field:
            if cell.clicked: 
                continue
            cell.openSelf()

        self.result = result
        self.running = False
