from objects import SaperTerminal, textStart
from sys import argv
import os


def printGame(game, helpText=None):
    os.system("clear||cls")
    game.printField()
    if helpText:
        print(helpText, end="")


def main(count_cols=5, count_rows=5, count_mines=7):
    if count_cols*count_rows <= count_mines + 9:
        raise Exception("too many mines")

    game = SaperTerminal(count_cols, count_rows, count_mines)
    printGame(game, textStart)

    xPos, yPos, action = input().split()
    userMove = (int(xPos) - 1, int(yPos) - 1)

    game.generateField(firstMove=userMove)
    game.move(userMove, action)
    printGame(game, textStart)
    
    while game.running:
        xPos, yPos, action = input().split()
        userMove = (int(xPos) - 1, int(yPos) - 1)
        game.move(userMove, action)

        printGame(game, textStart)

    printGame(game)
    if game.result == "loss":
        print("You lost")
    elif game.result == "win":
        print("You win")


if __name__ == "__main__":
    if argv[1:]:
        try:
            main(int(argv[1]), int(argv[2]), int(argv[3]))
        except (IndexError, ValueError):
           print("parameters: NOTHING or [count columns] [count rows] [count mines]")
    else:
        main()
