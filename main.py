from Test_room_definitions import *

'''
for _ in range(0, 10):
    for f in range(1, 20):
        if win.winfo_screenwidth()/32*_/f == win.winfo_screenwidth()/32*_//f == 48:
            size = [f, _]
            print(size)
'''  # Small function that prints out all possible sizes for 48x48 pixel objects. (zoom, subsample)

Room_1.load()

Player1 = Player("Player1")
Player1.room = Room_1
Player1.spells = [
    Spell(PhotoImage(file="images/ButtonTest-spell.png").zoom(6, 6)),
    Spell(PhotoImage(file="images/ButtonTest-spell.png").zoom(6, 6)),
    Spell(PhotoImage(file="images/ButtonTest-spell.png").zoom(6, 6)),
]
Player1.inventory = [
    Spell(PhotoImage(file="images/ButtonTest-Item.png").zoom(4, 4)),
    Spell(PhotoImage(file="images/ButtonTest-Item.png").zoom(4, 4)),
    Spell(PhotoImage(file="images/ButtonTest-Item.png").zoom(4, 4)),
    Spell(PhotoImage(file="images/ButtonTest-Item.png").zoom(4, 4)),
    Spell(PhotoImage(file="images/ButtonTest-Item.png").zoom(4, 4)),
]
Player1.disp.roll()

win.bind("<w>", Player1.move)
win.bind("<d>", Player1.move)
win.bind("<s>", Player1.move)
win.bind("<a>", Player1.move)
win.bind("<r>", Player1.interact)

win.bind("<l>", lambda bound: battle([Player1], [Foe(8, 20, 10, 5, [attack], "Speed=8"), Foe(5, 25, 0, 5, [attack], "Speed=5")], "TestBackground"))

win.bind("<Escape>", exit)
win.mainloop()
