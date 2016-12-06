import random

class SnakeLogic(object):
    def __init__(self):
        self.gameOver = False
        self.score = 0
        self.gameStarted = False


        self.boardSize = 10  # customize size for bigger/smaller board!
        self.snakeBoard = []  # 2D List representing the game board

        self.snakeHead = {}  # store the row, and col location of the snake's head
        self.snakeSegments = []  # store row,col location of the snake segments except the head
        self.direction = ""

        self.foodPosition = {}  # store the row,col location of the food
        self.obstaclePosition = {}

        self.loadSnakeBoard(self.boardSize)

    def isGameRunning(self):
        return self.gameStarted and not self.gameOver
    def isCPUplay(self):
        return self.comp
    def getBoard(self):
        return self.snakeBoard
    def snakeLength(self):
        """Returns the current length of the snake"""
        highestVal = 0
        for row in range(self.boardSize):
            for col in range(self.boardSize):
                highestVal = max(highestVal,self.snakeBoard[row][col])
        return highestVal

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

    def makeMove(self,direction):
        self.direction = direction
        if self.direction == "Left":
            self.moveSnake(0, -1)
        elif self.direction == "Right":
            self.moveSnake(0, 1)
        elif self.direction == "Up":
            self.moveSnake(-1, 0)
        elif self.direction == "Down":
            self.moveSnake(1, 0)

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

    def moveSnake(self, rowDiff, colDiff):
        """Input:
           rowDiff: the amount to move in the row (vertical) direction by
           colDiff: the amount to move in the col (horizontal) direction by
           Moves the snake by the given amount"""
        if not self.gameOver:
            self.setPositions()
            newHeadRow = self.snakeHead['row'] + rowDiff
            newHeadCol = self.snakeHead['col'] + colDiff
            headRank = self.snakeLength()
            if self.isGameOver(newHeadRow, newHeadCol):
                self.gameOver = True
                self.gameOverScreen()
                return
            if self.snakeBoard[newHeadRow][newHeadCol] == -1:
                self.snakeBoard[newHeadRow][newHeadCol] = headRank + 1
                self.score += 1
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

    def calculateManhattanBoard(self):
        foodRow = self.foodPosition['row']
        foodCol = self.foodPosition['col']
        self.manhattanBoard = [[0 for x in range(self.boardSize)] for x in range(self.boardSize)]
        for row in range(self.boardSize):
            for col in range(self.boardSize):
                manDistance = abs(foodRow-row) + abs(foodCol-col)
                self.manhattanBoard[row][col] = manDistance

    def makeObstacle(self):
        width = self.boardSize
        row = random.choice(range(width))
        col = random.choice(range(width))
        # if we are at a location where snake already exists, keep looking for random blank space
        while self.snakeBoard[row][col] != 0:
            row = random.choice(range(width))
            col = random.choice(range(width))

        self.snakeBoard[row][col] == -2

