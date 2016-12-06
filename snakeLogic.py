import random

class Node:
    def __init__(self,row,col):
        self.row = row
        self.col = col
        self.fVal = 0
        self.hVal = 0
        self.gVal = 0
        self.parent = None

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
    def getScore(self):
        return self.score

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

                #self.gameOverScreen()
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
                manDistance = abs(foodRow - row) + abs(foodCol - col)
                self.manhattanBoard[row][col] = manDistance

    def heuristic(self, node):
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
        return abs(node.row - self.foodPosition['row']) + abs(node.col - self.foodPosition['col'])

    def setNodeBoard(self):
        self.nodeBoard = [[0 for x in range(self.boardSize)] for x in range(self.boardSize)]
        for row in range(self.boardSize):
            for col in range(self.boardSize):
                self.nodeBoard[row][col] = Node(row, col)

    def neighborNodes(self, node):
        surroundNodes = []
        if node.row - 1 >= 0:
            top = self.nodeBoard[node.row - 1][node.col]
            surroundNodes.append(top)

        if node.col - 1 >= 0:
            left = self.nodeBoard[node.row][node.col - 1]
            surroundNodes.append(left)

        if node.col + 1 < self.boardSize:
            right = self.nodeBoard[node.row][node.col + 1]
            surroundNodes.append(right)

        if node.row + 1 < self.boardSize:
            bot = self.nodeBoard[node.row + 1][node.col]
            surroundNodes.append(bot)

        return surroundNodes

    def findMinNode(self, nodes):
        """Finds the node with the lowest fVal"""
        minNode = nodes[0]
        for node in nodes:
            if node.fVal < minNode.fVal:
                minNode = node
        return minNode

    def printPathList(self, end):
        while end.parent != None:
            self.pathList.append([end.row, end.col])
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
        goal = Node(self.foodPosition['row'], self.foodPosition['col'])
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
        if abs(nextRow - self.snakeHead['row']) == 0 and (nextCol - self.snakeHead['col']) == -1:  # left
            self.moveSnake(0, -1)
        elif abs(nextRow - self.snakeHead['row']) == 0 and (nextCol - self.snakeHead['col']) == 1:  # right
            self.moveSnake(0, 1)
        elif (nextRow - self.snakeHead['row']) == -1 and abs(nextCol - self.snakeHead['col']) == 0:  # up
            self.moveSnake(-1, 0)
        elif (nextRow - self.snakeHead['row']) == 1 and abs(nextCol - self.snakeHead['col']) == 0:  # down
            self.moveSnake(1, 0)

    def stall(self):
        if self.snakeHead['col'] - 1 >= 0 and self.snakeBoard[self.snakeHead['row']][
                    self.snakeHead['col'] - 1] <= 0:  # left
            self.moveSnake(0, -1)
        elif self.snakeHead['col'] + 1 < self.boardSize and self.snakeBoard[self.snakeHead['row']][
                    self.snakeHead['col'] + 1] <= 0:  # right
            self.moveSnake(0, 1)
        elif self.snakeHead['row'] - 1 >= 0 and self.snakeBoard[self.snakeHead['row'] - 1][
            self.snakeHead['col']] <= 0:  # up
            self.moveSnake(-1, 0)

        elif self.snakeHead['row'] + 1 < self.boardSize and self.snakeBoard[self.snakeHead['row'] + 1][
            self.snakeHead['col']] <= 0:  # down
            self.moveSnake(1, 0)
        else:
            print("stall has failed")
            self.gameOver = True
            return True


