"""
Core.py
--

Center file.
This file defines some base variables for the tkinter window and the Settings object.
This file imports only tkinter and no files from within Destined folder.

"""

from tkinter import *
# Window and screen (canvas) creation:
win = Tk()
scr = Canvas(win, width=1536, height=864, bd=0, highlightthickness=0, bg="#040C35")
scr.configure(width=1920, height=1080)
scr.pack()
win.attributes("-fullscreen", True)
scr.configure(xscrollincrement=1)
scr.configure(yscrollincrement=1)

# Core.can_escape variable used by menu functions for when the player can/cannot open some menus:
can_escape = True


# necessary definitions:
def __pass():
    """Internal function for passing.
    Necessary since the builtin pass cannot be given as variable."""
    pass


class Empty:
    """Empty class for symple objects to store data in."""
    pass


# Settings object base values (only used in case of incomplete Settings.txt file):
Settings = Empty()
Settings.upKey = "w"
Settings.rightKey = "d"
Settings.downKey = "s"
Settings.leftKey = "a"
Settings.interactKey = "r"
Settings.inventoryKey = "i"
Settings.escapeKey = "Escape"
