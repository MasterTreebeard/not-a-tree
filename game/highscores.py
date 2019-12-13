import tkinter as tk
class Displayscores:
    def __init__(self):
        self.swin = tk.Tk()
        self.swin.minsize(width=250,height=150)
        self.swin.maxsize(width=250,height=300)
        self.swin.title("High Scores")
        self.but = tk.Button(self.swin, text='Exit',command=self.selfkill)
        self.text = tk.Label(self.swin)
        infile = open('high-scores.txt','r')
        lines = infile.readlines()
        nline = []
        for line in lines:
            nline.append(line)
        self.text['text'] = ''.join(nline) 
        self.but.pack()
        self.text.pack()
    def selfkill(self):
        self.swin.destroy()
