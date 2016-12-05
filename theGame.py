from tkinter import *
from tkinter import ttk
WIDTH = 500
HEIGHT = 500


class helloApp:
    def __init__(self,master):
        self.frame = ttk.Frame(master)
        self.label = ttk.Label(master,text="Hi tkinter")
        self.label.grid(row =0 , column =0, columnspan =2)



        ttk.Button(master, text = "TEXAS",command = self.texasHi).grid(row=1,column=0)
        ttk.Button(master, text ="HAWAII",command = self.hawaiiHi).grid(row=1,column = 1)
        self.frameSet()

    def texasHi(self):
        self.label.config(text = "howdy tkinter")

    def hawaiiHi(self):
        self.label.config(text ="aloha tkinter")

    def frameSet(self):
        self.frame.pack()
        self.frame.config(height=100, width=300)
        self.frame.config(relief=RIDGE)
        ttk.Button(self.frame, text='Click Me').pack()
        self.frame.config(padding=(30, 15))
        ttk.LabelFrame(root, height=100, width=200, text='My Frame').pack()





root = Tk()
app = helloApp(root)
root.mainloop()
