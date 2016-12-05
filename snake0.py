# snake0.py

from tkinter import *
import random
import queue


# TODO: Add A* Algorithm
# TODO: Add niche case heuristics to help the snake out
# TODO: Change the GUI background to black, change snake color to green
# TODO: Add sound effects when snake dies and when food is eaten
# TODO: Add a scoreBoard .txt file that one can use to get high scores from
# TODO: Add pause, restart features, and a levels feature (easy, medium, hard)
# TODO: Add obstacles, and maybe power-ups
# TODO: Add outline of A star path


class Node(object):
    """A node representing a single part of the snake."""

    def __init__(self,row,col):
        self.row = row
        self.col = col
        self.fVal = 0
        self.hVal = 0
        self.gVal = 0
        self.parent = None


class SnakeGame:
    def __init__(self):
        # IS RCS WORKING?
        # Initialize Data Members
        self.nodeBoard = []
        self.boardSize = 10  # customize size for bigger/smaller board!
        self.snakeBoard = []  # 2D List representing the game board
        self.snakeHead = {}  # store the row, and col location of the snake's head
        self.snakeSegments = []  # store row,col location of the snake segments except the head
        self.direction = ""
        self.gameOver = False
        self.score = 0
        self.gameStarted = False
        self.foodPosition = {}  # store the row,col location of the food
        self.obstaclePosition = {}

        # A Star Algorithm related Data Members
        self.manhattanBoard = []
        self.pathList = []
        self.computerPlay = False

        # Initialize root, the canvas, and the buttons for the GUI
        self.root = Tk()
        self.canvas = Canvas(self.root, width=(self.boardSize*31), height=(self.boardSize*31))
        self.canvas.pack()
        self.root.canvas = self.canvas.canvas = self.canvas
        self.newGame = Button(self.root, command=self.init, text='newGame').pack()
        self.CPUGame = Button(self.root, command=self.initCPU, text='CPUGame').pack()
        self.root.bind("<Key>", self.keyPressed)  # binds keyEvent to the function keyPressed()

        # initialize the board and the game
        self.init()

    def run(self):
        """Runs the animation of the game (ticks)"""
        self.timerFired(self.canvas)
        self.root.mainloop()

    def init(self):
        """Initializes the game by loading the snakeBoard and drawing it in the GUI"""
        self.gameOver = False
        self.gameStarted = False
        self.computerPlay = False
        self.printInstructions()
        self.loadSnakeBoard(self.boardSize)
        self.score = 0
        self.redrawAll()


    def initCPU(self):
        """Initializes the game by loading the snakeBoard and drawing it in the GUI"""
        self.computerPlay = True
        self.gameOver = False
        self.gameStarted = False
        self.printInstructions()
        self.score = 0
        self.loadSnakeBoard(self.boardSize)
        self.redrawAll()


    def printInstructions(self):
        """print the instructions of the game in the Console"""
        print("Welcome to Snake Game!")
        print("Use the Arrow keys to move!")
        print("Press New Game to Restart your game!")
        print("Press CPUGame and then press any arrow key to watch the A* Algorithm Snake Player!")
        return

    def keyPressed(self, event):
        """Input: Keyboard event
        1) Sets the direction data member given corresponding arrow-key event
        2) game starts from the moment key is pressed also"""
        self.direction = event.keysym
        self.gameStarted = True

    def timerFired(self, canvas):
        """controls tick time of the game
        1) Keeps moving the snake in the given direction at the given delay intervals"""
        delay = 3  # milliseconds tick time
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

    # snakeBoardStuff
    #  Functions used to visualize 2D List into the GUI
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

    def loadSnakeBoard(self, size):
        """initializes the snakeBoard 2d List, and starts the snake in the middle of the board
           and places a food object a random place
           snakeBoard is a 2D List
           0 = empty space
           -1 = food
           >1 = snake"""
        self.snakeBoard = [[0 for x in range(size)] for x in range(size)]
        self.snakeBoard[int(size / 2)][int(size / 2)] = 1
        self.makeFood()
        self.makeObstacle()
        return

    def redrawAll(self):
        """Deletes the current snakeBoard, and redraws a new snakeBoard with changed values
           1) if game is over, then draws the gameOverScreen overlay"""
        self.canvas.delete(ALL)
        if self.gameOver:
            self.drawSnakeBoard()
            self.gameOverScreen()
        else:
            self.drawSnakeBoard()

    # snakeStuff
    def snakeLength(self):
        """Returns the current length of the snake"""
        highestVal = 0
        for row in range(self.boardSize):
            for col in range(self.boardSize):
                highestVal = max(highestVal,self.snakeBoard[row][col])
        return highestVal

    def setPositions(self):
        """sets the snakeHead, and snakeSegments data values (row,col info)"""
        maxVal = self.snakeLength()
        self.snakeSegments = []
        for row in range(self.boardSize):
            for col in range(self.boardSize):
                if self.snakeBoard[row][col] == maxVal:
                    self.snakeHead['row'] = row
                    self.snakeHead['col'] = col
                elif self.snakeBoard[row][col] >= 1 and self.snakeBoard[row][col] < maxVal:
                    snakePart = {}
                    snakePart['row'] = row
                    snakePart['col'] = col
                    self.snakeSegments.append(snakePart)

    def removeTail(self):
        """removes the tail of the snake by decreasing all the number values of the snake by one
        (tail has value 1, so it will become 0)"""
        for row in range(self.boardSize):
            for col in range(self.boardSize):
                if self.snakeBoard[row][col] > 0:
                    self.snakeBoard[row][col] -= 1

    def moveSnake(self,rowDiff,colDiff):
        """Input:
           rowDiff: the amount to move in the row (vertical) direction by
           colDiff: the amount to move in the col (horizontal) direction by
           Moves the snake by the given amount"""
        if not self.gameOver:
            self.setPositions()
            newHeadRow = self.snakeHead['row'] + rowDiff
            newHeadCol = self.snakeHead['col'] + colDiff
            headRank = self.snakeLength()
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

    def makeFood(self):
        """Creates a food object in the GUI at a position that is empty currently"""
        width = self.boardSize
        row = random.choice(range(width))
        col = random.choice(range(width))
        # if we are at a location where snake already exists, keep looking for random blank space
        while self.snakeBoard[row][col] != 0:
            row = random.choice(range(width))
            col = random.choice(range(width))

        self.snakeBoard[row][col] = -1
        self.foodPosition['row'] = row
        self.foodPosition['col'] = col
        self.calculateManhattanBoard()

    def makeObstacle(self):
        width = self.boardSize
        row = random.choice(range(width))
        col = random.choice(range(width))
        # if we are at a location where snake already exists, keep looking for random blank space
        while self.snakeBoard[row][col] != 0:
            row = random.choice(range(width))
            col = random.choice(range(width))

        self.snakeBoard[row][col] == -2

    # A star Algorithm
    def calculateManhattanBoard(self):
        foodRow = self.foodPosition['row']
        foodCol = self.foodPosition['col']
        self.manhattanBoard = [[0 for x in range(self.boardSize)] for x in range(self.boardSize)]
        for row in range(self.boardSize):
            for col in range(self.boardSize):
                manDistance = abs(foodRow-row) + abs(foodCol-col)
                self.manhattanBoard[row][col] = manDistance

    def heuristic(self,node):
        """calculates manhattan distance from the node to the food"""
        inf = float('inf')
        for snakePart in self.snakeSegments:
            snakeRow = snakePart['row']
            snakeCol = snakePart['col']
            if node.row == snakeRow and node.col == snakeCol:
                return inf
        headRow = self.snakeHead['row']
        headCol = self.snakeHead['col']
        if node.row == headRow and node.col == headCol:
            return inf

        headNode = Node(self.snakeHead['row'], self.snakeHead['col'])
        headNode.hval = inf
        self.nodeBoard[self.snakeHead['row']][self.snakeHead['col']] = headNode
        return abs(node.row-self.foodPosition['row']) + abs(node.col-self.foodPosition['col'])


    def setNodeBoard(self):
        self.nodeBoard = [[0 for x in range(self.boardSize)] for x in range(self.boardSize)]
        for row in range(self.boardSize):
            for col in range(self.boardSize):
                self.nodeBoard[row][col] = Node(row,col)


    def neighborNodes(self,node):
        surroundNodes = []
        if node.row-1 >=0:
            top = self.nodeBoard[node.row-1][node.col]
            surroundNodes.append(top)

        if node.col-1 >= 0:
            left = self.nodeBoard[node.row][node.col-1]
            surroundNodes.append(left)

        if node.col+1 < self.boardSize:
            right = self.nodeBoard[node.row][node.col+1]
            surroundNodes.append(right)

        if node.row+1 < self.boardSize:
            bot = self.nodeBoard[node.row+1][node.col]
            surroundNodes.append(bot)

        return surroundNodes

    def findMinNode(self,nodes):
        """Finds the node with the lowest fVal"""
        minNode = nodes[0]
        for node in nodes:
            if node.fVal < minNode.fVal:
                minNode = node
        return minNode

    def printPathList(self,end):
        while end.parent != None:
            self.pathList.append([end.row,end.col])
            end = end.parent
        self.pathList.reverse()




    # gVal = cost it took to get to the node
    # hVal = heuristical guess at how much it'll cost from this node to the goal
    # fVal = gVal + hVal
    def calculateAstar(self):
        self.pathList = []
        self.setPositions()
        self.setNodeBoard()
        openList = []
        closedList = []
        goal = Node(self.foodPosition['row'],self.foodPosition['col'])
        beginNode = self.nodeBoard[self.snakeHead['row']][self.snakeHead['col']]
        beginNode.gVal = 0
        beginNode.hVal = self.manhattanBoard[beginNode.row][beginNode.col]
        beginNode.fVal = beginNode.gVal + beginNode.hVal
        self.nodeBoard[beginNode.row][beginNode.col] = beginNode
        openList.append(beginNode)
        while len(openList) > 0:  # while openList is not empty
            current = self.findMinNode(openList)  # node in openList with lowest fVal
            #  if current == goal
            if current.row == goal.row and current.col == goal.col:
                self.printPathList(current)
                print (self.pathList)
                return self.pathList
            openList.remove(current)
            closedList.append(current)
            neighborsList = self.neighborNodes(current)

            for neighbor in neighborsList:  # for each neighbor of current
                if neighbor in closedList:
                    continue
                if neighbor not in openList:
                    neighbor.gVal = current.gVal + 1
                    neighbor.hVal = self.heuristic(neighbor)
                    neighbor.fVal = neighbor.gVal + neighbor.hVal
                    neighbor.parent = current
                    self.nodeBoard[neighbor.row][neighbor.col] = neighbor
                    openList.append(neighbor)
                else:
                    newGval = current.gVal + 1
                    if newGval < neighbor.gVal:
                        neighbor.gVal = newGval
                        neighbor.parent = current
                        self.nodeBoard[neighbor.row][neighbor.col] = neighbor

    def setDirection(self):
        nextLocation = self.pathList[0]
        nextRow = nextLocation[0]
        nextCol = nextLocation[1]
        if self.snakeBoard[nextRow][nextCol] > 0:
            stallSuccessful = self.stall()
            return
        if abs(nextRow-self.snakeHead['row']) == 0 and (nextCol-self.snakeHead['col']) == -1: # left
            self.moveSnake(0,-1)
        elif abs(nextRow - self.snakeHead['row']) == 0 and (nextCol - self.snakeHead['col']) == 1: # right
            self.moveSnake(0,1)
        elif (nextRow - self.snakeHead['row']) == -1 and abs(nextCol - self.snakeHead['col']) == 0: # up
            self.moveSnake(-1,0)
        elif (nextRow - self.snakeHead['row']) == 1 and abs(nextCol - self.snakeHead['col']) == 0: # down
            self.moveSnake(1,0)

    def stall(self):
        if self.snakeHead['col']-1 >= 0 and self.snakeBoard[self.snakeHead['row']][self.snakeHead['col']-1] <= 0:  # left
                self.moveSnake(0,-1)
        elif self.snakeHead['col']+1 < self.boardSize and self.snakeBoard[self.snakeHead['row']][self.snakeHead['col']+1] <= 0: # right
                self.moveSnake(0,1)
        elif self.snakeHead['row']-1 >= 0 and self.snakeBoard[self.snakeHead['row']-1][self.snakeHead['col']] <= 0: # up
            self.moveSnake(-1,0)

        elif self.snakeHead['row']+1 < self.boardSize and self.snakeBoard[self.snakeHead['row']+1][self.snakeHead['col']] <= 0: # down
            self.moveSnake(1,0)
        else:
            print("stall has failed")
            self.gameOver = True
            return True




    #  Game Over functions
    def isGameOver(self,headRow,headCol):
        """Output: Boolean
           Checks to see if the game is over
           1) Snake ran into a wall
           2) Snake ran into its own body segments"""
        if headRow < 0 or headRow > self.boardSize-1:
            self.gameOver = True
            return True
        if headCol < 0 or headCol > self.boardSize-1:
            self.gameOver = True
            return True
        self.setPositions()
        for segment in self.snakeSegments:
            if segment['row'] == headRow and segment['col'] == headCol:
                return True
        return False


    def gameOverScreen(self):
        """Outputs the Game Over screen in the GUI"""
        #self.canvas.delete(ALL)
        canvas_id = self.canvas.create_text(100, 50, anchor="nw")
        endText = "Game Over!\nYour score is:"+str(self.score)
        self.canvas.itemconfig(canvas_id, text=endText, fill='red')

snakeGame = SnakeGame()
snakeGame.run()