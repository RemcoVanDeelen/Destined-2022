from Menus import *

'''
for _ in range(0, 20):
    for f in range(1, 20):
        if win.winfo_screenwidth()/32*_/f == win.winfo_screenwidth()/32*_//f == 48:
            size = [(f, _)]
            print(size)
'''  # Small function that prints out all possible sizes for 48x48 pixel objects. (zoom, subsample)
# win.bind("<Key>", lambda event: print("<"+event.keysym+">"))

# Player1 = Player("Player1")        moved to = Test_room_definitions.py =
Player1.room = Room_1

open_main_menu()
win.mainloop()
