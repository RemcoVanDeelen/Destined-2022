"""
main.py
--

Final file, this is the file to execute.
It prepares the variables for use and calls the starting functions open_main_menu() and mainloop().
All files are imported through Test_room_definitions so Tiles have access to all functions.

"""
from Test_room_definitions import *

# Defines globals for save function,
global_list = globals()

# sets player room (necessary because opening the main menu unloads the room),
Player1.room = Room_A

# opens main menu,
open_main_menu()

# loads previous settings
load("Settings")

# and runs mainloop.
print("=-- Destined action log: --=")
win.mainloop()
