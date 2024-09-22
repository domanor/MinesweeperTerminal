class Tag:
    MINE = 0
    FLAG = 1
    QUESTION = 2
    NOTHING = 3
    NUMBER = 4
    EMPTY = 5


signTo = {
    Tag.MINE: "[M]",
    Tag.FLAG: "[F]",
    Tag.QUESTION: "[?]",
    Tag.NOTHING: "[ ]",
    Tag.NUMBER: lambda n: f"[{n}]",
    Tag.EMPTY: "   ",
}
