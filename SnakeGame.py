from SnakeGUI import SnakeGUI
from SnakeLogic import SnakeLogic
from tkinter import *
class SnakeGame(object):
    def __init__(self):
        self.GUI = SnakeGUI()
        self.logic = SnakeLogic()
    def run(self):
        """starts the game by starting TkInter's timerFired method"""
        self.GUI.timerFired(self.logic)
    def updateGUI(self):
        """Updates the Board array in the GUI class to match the Logic class' board"""
        self.GUI.updateBoard(self.logic.getBoard())
    def makeNewGame(self):
        self.logic.loadSnakeBoard(10)
    def isGameOver(self):
        return self.logic.gameOver
game = SnakeGame()
game.updateGUI()
game.run()
game.GUI.root.mainloop()