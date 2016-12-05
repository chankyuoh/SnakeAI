from tkinter import *
from SnakeLogic import SnakeLogic
class SnakeGUI(object):
    def __init__(self):
        self.boardSize = 10
        self.snakeBoard = []
        self.root = Tk()
        self.canvas = Canvas(self.root, width=(self.boardSize*31), height=(self.boardSize*31))
        self.canvas.pack()
        self.root.canvas = self.canvas.canvas = self.canvas
        self.newGame = Button(self.root, text='newGame').pack()
        self.CPUGame = Button(self.root, text='CPUGame').pack()
        self.root.bind("<Key>", self.keyPressed)  # binds keyEvent to the function keyPressed()

    def updateBoard(self,board):
        self.snakeBoard = board
        self.drawSnakeBoard()

    def timerFired(self):
        """controls tick time of the game
        1) Keeps moving the snake in the given direction at the given delay intervals"""
        delay = 150  # milliseconds tick time
        # change the delay variable to adjust game speed

        if self.gameStarted and not self.gameOver:

            if self.computerPlay == True:
                self.calculateAstar()
                self.setDirection()
                self.redrawAll()
            else:
                if self.direction == "Left":
                    self.moveSnake(0, -1)
                elif self.direction == "Right":
                    self.moveSnake(0, 1)
                elif self.direction == "Up":
                    self.moveSnake(-1, 0)
                elif self.direction == "Down":
                    self.moveSnake(1, 0)
                self.redrawAll()

        # pause for a bit, and then call timerFired again
        self.canvas.after(delay, self.timerFired, self.canvas)


    def drawSnakeBoard(self):
        """Take the 2D list board, and visualizes it into the GUI"""
        for row in range(self.boardSize):
            for col in range(self.boardSize):
                self.drawSnakeCell(row, col)

    def drawSnakeCell(self, row, col):
        """Helper function for drawSnakeBoard
           Draws the cell, which is represented as a rectangle, in the GUI
           if cell is where the snake is at, it has blue oval
           if cell is where the food is at, it has yellow oval"""
        margin = 5
        cellSize = 30
        left = margin + col * cellSize
        right = left + cellSize
        top = margin + row * cellSize
        bottom = top + cellSize
        self.canvas.create_rectangle(left, top, right, bottom, fill="white")
        if (self.snakeBoard[row][col] > 0):
            # draw part of the snake body
            self.canvas.create_oval(left, top, right, bottom, fill="blue")
        elif self.snakeBoard[row][col] == -1:
            self.canvas.create_oval(left, top, right, bottom, fill="yellow")
        elif self.snakeBoard[row][col] == -2:
            self.canvas.create_oval(left, top, right, bottom, fill="red")
        return

    def redrawAll(self):
        """Deletes the current snakeBoard, and redraws a new snakeBoard with changed values
           1) if game is over, then draws the gameOverScreen overlay"""
        self.canvas.delete(ALL)
        self.drawSnakeBoard()
#        if self.gameOver:
#            self.drawSnakeBoard()
#            self.gameOverScreen()
#        else:
#            self.drawSnakeBoard()

    def keyPressed(self, event):
        """Input: Keyboard event
        1) Sets the direction data member given corresponding arrow-key event
        2) game starts from the moment key is pressed also"""
        self.direction = event.keysym
        self.gameStarted = True

    def getDirection(self):
        return self.direction

