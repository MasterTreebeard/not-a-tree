import tkinter as tk
import sys
import highscores as hs

def run():
    m.win.destroy()
    import game
    sys.exit()

def scores():
    d = hs.Displayscores()
    
class Menu:
    def __init__(self):
        self.win = tk.Tk()
        self.win.minsize(width=250,height=150)
        self.win.maxsize(width=250,height=150)
        self.win.title("The Dungeon Master")
        but = tk.Button(self.win, text='Start Game',command=run)
        button = tk.Button(self.win, text='High Scores',command=scores)
        photo = tk.PhotoImage(file="sprites/main_character/cut_down/2.gif")
        label = tk.Label(image=photo)
        label.image = photo
        label.pack()
        but.pack()
        button.pack()

m = Menu()
tk.mainloop()
