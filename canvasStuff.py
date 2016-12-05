# snake0.py

from tkinter import *
import random

class SnakeGame:
    def __init__(self):
        # Initialize root and the canvas for the GUI
        self.root = Tk()
        self.canvas = Canvas(self.root, width=310, height=310)
        self.canvas.pack()
        # Store canvas in root and in canvas itself for callbacks
        self.root.canvas = self.canvas.canvas = self.canvas
        self.newGame = Button(self.root, command = self.init, text='newGame').pack()



        # Initialize Data Members
        self.boardSize = 10
        self.snakeBoard = []
        self.snakeHead = {}
        self.snakeSegments = []
        self.snakeTail = {}
        self.nextTailPos = []
        self.direction = ""
        self.gameOver = False
        self.score = 0
        self.gameStarted = False


        self.root.bind("<Key>", self.keyPressed)
        self.init()

    def run(self):
        # set up events

        self.timerFired(self.canvas)
        # and launch the app
        self.root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)

    def snakeLength(self):
        highestVal = 0
        for row in range(self.boardSize):
            for col in range(self.boardSize):
                highestVal = max(highestVal,self.snakeBoard[row][col])
        return highestVal


    def setPositions(self):
        maxVal = self.snakeLength()
        self.snakeSegments = []
        for row in range(self.boardSize):
            for col in range(self.boardSize):
                if self.snakeBoard[row][col] == maxVal:
                    self.snakeHead['row'] = row
                    self.snakeHead['col'] = col
                    self.snakeHead['rank'] = maxVal
                elif self.snakeBoard[row][col] >= 1 and self.snakeBoard[row][col] < maxVal:
                    snakePart = {}
                    snakePart['row'] = row
                    snakePart['col'] = col
                    snakePart['rank'] = self.snakeBoard[row][col]
                    self.snakeSegments.append(snakePart)

        return


    def removeTail(self):
        for row in range(self.boardSize):
            for col in range(self.boardSize):
                if self.snakeBoard[row][col] > 0:
                    self.snakeBoard[row][col] -= 1



    def isGameOver(self,headRow,headCol):
        if headRow < 0 or headRow > self.boardSize-1:
            self.gameOver = True
            print ("GAMEOVER HIT WALL")
            return True
        if headCol < 0 or headCol > self.boardSize-1:
            self.gameOver = True
            print ("GAMEOVER HIT WALL")
            return True
        self.setPositions()
        for segment in self.snakeSegments:
            if segment['row'] == headRow and segment['col'] == headCol:
                return True
        return False


    def gameOverScreen(self):
        #self.canvas.delete(ALL)
        canvas_id = self.canvas.create_text(100, 50, anchor="nw")
        endText = "Game Over!\nYour score is:"+str(self.score)
        self.canvas.itemconfig(canvas_id, text=endText, fill='red')




    def moveSnake(self,rowDiff,colDiff):
        if not self.gameOver:
            self.setPositions()
            newHeadRow = self.snakeHead['row'] + rowDiff
            newHeadCol = self.snakeHead['col'] + colDiff
            headRank = self.snakeLength()
            print ("row",newHeadRow,"col: ",newHeadCol)
            if self.isGameOver(newHeadRow,newHeadCol):
                self.gameOver = True
                self.gameOverScreen()
                return
            if self.snakeBoard[newHeadRow][newHeadCol] == -1:
                self.snakeBoard[newHeadRow][newHeadCol] = headRank + 1
                self.score +=1
                self.makeFood()
                self.gameOver = self.isGameOver(newHeadRow, newHeadCol)
            else:
                self.removeTail()
                self.gameOver = self.isGameOver(newHeadRow, newHeadCol)
                self.snakeBoard[newHeadRow][newHeadCol] = headRank

            if not self.gameOver:
                print("GAME IS NOT OVER")


            else:
                print("Gameover")
                self.gameOverScreen()
                return
            self.setPositions()




    def makeFood(self):
        width = self.boardSize
        row = random.choice(range(width))
        col = random.choice(range(width))
        # if we are at a location where snake already exists, keep looking for random blank space
        while self.snakeBoard[row][col] != 0:
            row = random.choice(range(width))
            col = random.choice(range(width))

        self.snakeBoard[row][col] = -1





    def keyPressed(self, event):
        canvas = event.widget.canvas
        self.direction = event.keysym
        self.gameStarted = True
        """
        if self.direction == "Left":
            self.moveSnake(0, -1)
        elif self.direction == "Right":
            self.moveSnake(0, 1)
        elif self.direction == "Up":
            self.moveSnake(-1, 0)
        elif self.direction == "Down":
            self.moveSnake(1, 0)
        self.redrawAll()
        """





    def timerFired(self,canvas):
        delay = 200  # milliseconds

        if self.gameStarted:
            if self.direction == "Left":
                self.moveSnake(0, -1)
            elif self.direction == "Right":
                self.moveSnake(0, 1)
            elif self.direction == "Up":
                self.moveSnake(-1, 0)
            elif self.direction == "Down":
                self.moveSnake(1, 0)
            self.redrawAll()

        self.canvas.after(delay, self.timerFired, self.canvas)  # pause, then call timerFired again

    def redrawAll(self):
        self.canvas.delete(ALL)
        if self.gameOver:
            self.drawSnakeBoard()
            self.gameOverScreen()
        else:
            self.drawSnakeBoard()

    def drawSnakeBoard(self):
        for row in range(self.boardSize):
            for col in range(self.boardSize):
                self.drawSnakeCell(row, col)


        return

    def drawSnakeCell(self, row, col):
        # you write this!
        # hint: place a margin 5-pixels-wide around the board.
        # make each cell 30x30
        # draw a white square and then, if the snake is in the
        # cell, draw a blue circle.
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
        return

    def loadSnakeBoard(self,size):
        # you write this!
        # allocate the new self.snakeBoard 2d list as described
        # in the notes, and store it in the canvas's data
        # dictionary
        self.direction = 'Up'
        self.snakeBoard = [[0 for x in range(size)] for x in range(size)]
        self.snakeBoard[int(size/2)][int(size/2)] = 1

        self.makeFood()
        return


    def printInstructions(self):
        # you write this!
        # print the instructions
        print("Welcome to Snake Game!")
        print("Use the Arrow keys to move!")
        print("Press New Game to Restart your game!")
        print("Press ComputerPlay to watch the A* Algorithm Snake Player!")
        return

    def init(self):
        self.printInstructions()
        self.loadSnakeBoard(self.boardSize)
        self.redrawAll()




snakeGame = SnakeGame()
snakeGame.run()