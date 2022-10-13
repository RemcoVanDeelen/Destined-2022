import gc

from Menus import *

'''
for _ in range(0, 20):
    for f in range(1, 20):
        if win.winfo_screenwidth()/32*_/f == win.winfo_screenwidth()/32*_//f == 48:
            size = [(f, _)]
            print(size)
'''  # Small function that prints out all possible sizes for 48x48 pixel objects. (zoom, subsample)

scr.tag_raise(Player1.tag)
# Player1 = Player("Player1")        moved to = Test_room_definitions.py =
Player1.room = Room_1

load(1)
Player1.disp.roll()
win.mainloop()
