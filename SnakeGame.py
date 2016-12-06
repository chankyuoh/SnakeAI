from SnakeGUI import SnakeGUI
from SnakeLogic import SnakeLogic
from tkinter import *
class SnakeGame(object):
    def __init__(self):
        self.GUI = SnakeGUI()
        self.logic = SnakeLogic()
        self.board = []
    def tick(self):
        self.GUI.timerFired(self.logic)
    def updateGUIBoard(self):
        self.board = self.logic.getBoard()
        self.GUI.updateBoard(self.board)
game = SnakeGame()
game.updateGUIBoard()
game.tick()
game.GUI.root.mainloop()