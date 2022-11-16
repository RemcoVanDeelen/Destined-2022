from Test_room_definitions import *
# Final file, this is the file to execute.
# All files are imported through Test_room_definitions so Tiles have access to all functions.

# Defines globals for save function,
global_list = globals()

# sets player room,
Player1.room = Room_1

# opens main menu
open_main_menu()

# and runs mainloop.
win.mainloop()
