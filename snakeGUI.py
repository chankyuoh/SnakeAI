from tkinter import *

class snakeGUI(object):
    def __init__(self):
        self.root = Tk()

    def initGUI(self):
        self.initalizeCanvas()
        self.initializeButtons()

    def initializeCanvas(self):
        self.canvas = Canvas(self.root, width=(self.boardSize*31), height=(self.boardSize*31))
        self.canvas.pack()
        self.root.canvas = self.canvas.canvas = self.canvas
    def initializeButtons(self):
        self.newGame = Button(self.root, command=self.init, text='newGame').pack()
        self.CPUGame = Button(self.root, command=self.initCPU, text='CPUGame').pack()
        self.root.bind("<Key>", self.keyPressed)  # binds keyEvent to the function keyPressed(

