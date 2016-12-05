# events-example0.py

from tkinter import *

def mousePressed(event):
    canvas = event.widget.canvas
    redrawAll(canvas)

def keyPressed(event):
    canvas = event.widget.canvas
    redrawAll(canvas)

def timerFired(canvas):
    redrawAll(canvas)
    delay = 250 # milliseconds
    canvas.after(delay, timerFired, canvas) # pause, then call timerFired again

def redrawAll(canvas):
    canvas.delete(ALL)

def init(canvas):
    pass

########### copy-paste below here ###########

def run():
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=300, height=200)
    canvas.pack()
    # Store canvas in root and in canvas itself for callbacks
    root.canvas = canvas.canvas = canvas
    # Set up canvas data and call init
    canvas.data = { }
    init(canvas)
    # set up events
    root.bind("<Button-1>", mousePressed)
    root.bind("<Key>", keyPressed)
    timerFired(canvas)
    # and launch the app
    root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)

run()