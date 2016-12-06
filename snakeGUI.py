from tkinter import *
from SnakeLogic import SnakeLogic
class SnakeGUI(object):
    def __init__(self):
        self.boardSize = 10
        self.board = []
        self.root = Tk()
        self.canvas = Canvas(self.root, width=(self.boardSize*31), height=(self.boardSize*31))
        self.canvas.pack()
        self.direction = ""
        self.gameOver = False
        self.root.canvas = self.canvas.canvas = self.canvas
        self.newGame = Button(self.root, command=self.init, text='newGame').pack()
        self.CPUGame = Button(self.root, command=self.initCPU, text='CPUGame').pack()
        self.root.bind("<Key>", self.keyPressed)  # binds keyEvent to the function keyPressed()
        self.gameStarted = False
        self.isCPUGameClicked = False
        self.isNewGameClicked = False
        self.printInstructions()
        self.computerPlay = False

    def init(self):
        self.isNewGameClicked = True
    def initCPU(self):
        self.isCPUGameClicked = True
    def newGame(self):
        self.gameOver = False
        self.gameStarted = False
        self.computerPlay = False
        self.printInstructions()
        self.score = 0
        self.redrawAll()

    def updateBoard(self,board):

        self.canvas.delete(ALL)
        self.board = board
        self.drawSnakeBoard()
        #if self.gameOver:
        #    self.drawSnakeBoard()
        #    self.gameOverScreen()
        #else:
        #    self.drawSnakeBoard()

    def gameOverScreen(self,score):
        """Outputs the Game Over screen in the GUI"""
        #self.canvas.delete(ALL)
        canvas_id = self.canvas.create_text(100, 50, anchor="nw")
        endText = "Game Over!\nYour score is:"+str(score)
        self.canvas.itemconfig(canvas_id, text=endText, fill='red')


    def timerFired(self,logic):
        """delays the game by the tick time amount"""
        delay = 150  # milliseconds tick time
        # change the delay variable to adjust game speed
        if self.isNewGameClicked:
            self.isNewGameClicked = False
            self.computerPlay = False
            logic.gameOver = False
            logic.loadSnakeBoard(10)
            self.updateBoard(logic.getBoard())
            self.gameStarted = False

        if self.isCPUGameClicked:
            self.isCPUGameClicked = False
            logic.gameOver = False
            logic.loadSnakeBoard(10)
            self.gameStarted = False
            self.updateBoard(logic.getBoard())
            self.computerPlay = True
        if self.gameStarted and not logic.gameOver:
            if self.computerPlay:
                logic.calculateAstar()
                logic.setDirection()
                self.updateBoard(logic.getBoard())
                self.redrawAll()
            else:
                logic.makeMove(self.direction)
                self.updateBoard(logic.getBoard())
                self.redrawAll()
        elif logic.gameOver:
            self.gameOver = True
            self.gameOverScreen(logic.getScore())
        else:
            self.redrawAll()


        # pause for a bit, and then call timerFired again
        self.canvas.after(delay, self.timerFired, logic)


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
        board = self.board
        self.canvas.create_rectangle(left, top, right, bottom, fill="black")
        if (board[row][col] > 0):
            # draw part of the snake body
            self.canvas.create_oval(left, top, right, bottom, fill="green")
        elif board[row][col] == -1:
            self.canvas.create_oval(left, top, right, bottom, fill="yellow")
        elif board[row][col] == -2:
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
        print "KEY PRESSED " + self.direction
        self.gameStarted = True

    def getDirection(self):
        return self.direction

    def printInstructions(self):
        """print the instructions of the game in the Console"""
        print("Welcome to Snake Game!")
        print("Use the Arrow keys to move!")
        print("Press New Game to Restart your game!")
        print("Press CPUGame and then press any arrow key to watch the A* Algorithm Snake Player!")
        return

