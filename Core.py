from tkinter import *

win = Tk()
scr = Canvas(win, width=1536, height=864, bd=0, highlightthickness=0, bg="#040C35")
scr.configure(width=1920, height=1080)
scr.pack()
win.attributes("-fullscreen", True)
scr.configure(xscrollincrement=1)
scr.configure(yscrollincrement=1)
global can_escape
can_escape = True


def __pass():
    pass
