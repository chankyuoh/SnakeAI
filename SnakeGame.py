from SnakeGUI import SnakeGUI
from SnakeLogic import SnakeLogic

class SnakeGame(object):
    def __init__(self):
        self.GUI = SnakeGUI()
        self.logic = SnakeLogic()
        self.board = []
    def timerFired(self):
        #self.logic.moveInDirection()
        direction = self.GUI.getDirection()
        if direction != "":
            self.logic.makeMove(direction)
            self.updateGUIBoard()
            # self.GUI.timerFired()
            delay = 150  # milliseconds tick time
            self.GUI.canvas.after(delay, self.timerFired(), self.canvas)
        return
    def updateGUIBoard(self):
        self.board = self.logic.getBoard()
        self.GUI.updateBoard(self.board)
game = SnakeGame()
game.updateGUIBoard()
game.timerFired()
game.GUI.root.mainloop()