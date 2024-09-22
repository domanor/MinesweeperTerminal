from .tag import Tag, signTo


class Cell:

    def __init__(self, position, type=Tag.NOTHING):
        self.position = position
        self.type = type
        self.clicked = False
        self.sign = signTo[Tag.NOTHING]

    def isMine(self):
        return self.type == Tag.MINE

    def openSelf(self, countMinesNear=0):
        self.clicked = True

        if self.isMine():
            self.sign = signTo[Tag.MINE]
            return

        if countMinesNear:
            self.sign = signTo[Tag.NUMBER](countMinesNear)

        else:
            self.sign = signTo[Tag.EMPTY]

    def putSomething(self, tag):
        self.sign = signTo[tag]

    def doSelfMine(self):
        self.type = Tag.MINE

    def __eq__(self, other):
        if isinstance(other, Cell):
            return self.position == other.position
        else:
            return self.position == other

    def __str__(self):
        return self.sign
