from Battle import *
import Enemy_moves

'''
for _ in range(0, 10):
    for f in range(1, 20):
        if win.winfo_screenwidth()/32*_/f == win.winfo_screenwidth()/32*_//f == 48:
            size = [f, _]
            print(size)
'''  # Small function that prints out all possible sizes for 48x48 pixel objects. (zoom, subsample)

# battle([Player("tag")], [Foe(8, 20, 10, 5, [Enemy_moves.attack], "Speed=8"), Foe(5, 25, 0, 5, [Enemy_moves.attack], "Speed=5")], "tt")

Room_1.load()
Player1 = Player("Player1")
Player1.disp.roll()
win.bind("<w>", Player1.move)
win.bind("<d>", Player1.move)
win.bind("<s>", Player1.move)
win.bind("<a>", Player1.move)
win.bind("<r>", Player1.interact)

win.bind("<Escape>", exit)
win.mainloop()
