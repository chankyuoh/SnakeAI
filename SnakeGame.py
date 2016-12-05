from SnakeGUI import SnakeGUI
from SnakeLogic import SnakeLogic

class SnakeGame(object):
    def __init__(self):
        self.GUI = SnakeGUI()
        self.logic = SnakeLogic()
        self.board = []
    def tick(self):
        #self.logic.moveInDirection()
        return
    def updateBoard(self):
        self.board = self.logic.getBoard()
        self.GUI.update(self.board)
game = SnakeGame()
