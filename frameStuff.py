#!/usr/bin/python3
# frame.py by Barron Stone
# This is an exercise file from Python GUI Development with Tkinter on lynda.com

from tkinter import *
from tkinter import ttk


class Board:
    def __init__(self,master):
        self.frame = ttk.Frame(master)
        self.frame.pack()
        self.frameSet()
        self.newGame = ttk.Button(root, command=self.startNewGame, text='newGame').pack()
        self.computerPlay = ttk.Button(root, text='CPU play').pack()

    def frameSet(self):
        self.frame.config(height=1000, width=900)
        self.frame.config(relief=RIDGE)

    def startNewGame(self):
        newButton = ttk.Button(self.frame, text = "INSIDE THE FRAME").grid(row=0,column=2)
        self.frame.config(padding = (300, 150))







root = Tk()
app = Board(root)
app.startNewGame()

#frame.config(padding = (100, 200))
#ttk.LabelFrame(root, height = 100, width = 200, text = 'My Frame').pack()

root.mainloop()
