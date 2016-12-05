from SnakeGUI import SnakeGUI
from SnakeLogic import SnakeLogic

class SnakeGame(object):
    def __init__(self):
        self.GUI = SnakeGUI()
        self.logic = SnakeLogic()
        self.board = []
    def tick(self):
        #self.logic.moveInDirection()
        self.updateGUIBoard()
        direction = self.GUI.getDirection()
        self.logic.makeMove(direction)
        self.updateGUIBoard()
        self.GUI.timerFired()
        self.GUI.root.mainloop()
        return
    def updateGUIBoard(self):
        self.board = self.logic.getBoard()
        self.GUI.updateBoard(self.board)
game = SnakeGame()
game.updateGUIBoard()
game.tick()