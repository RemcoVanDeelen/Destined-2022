from Test_room_definitions import *
from Action_definitions import *

'''
for _ in range(0, 20):
    for f in range(1, 20):
        if win.winfo_screenwidth()/32*_/f == win.winfo_screenwidth()/32*_//f == 48:
            size = [(f, _)]
            print(size)
'''  # Small function that prints out all possible sizes for 48x48 pixel objects. (zoom, subsample)

Room_1.load()
scr.tag_raise(Player1.tag)
# Player1 = Player("Player1")        moved to = Test_room_definitions.py =
Player1.room = Room_1
Player1.spells = [empower, elemental_volley, siphon, weaken, enchant_weapon]
Player1.inventory = [
    health_potion,
    large_health_potion,
    stamina_potion,
    large_stamina_potion,
    strength_potion,
    vitality_potion,
    shield_potion,
    resistance_potion,
    staminaless_potion
]
Player1.disp.roll()

win.bind("<w>", Player1.move)
win.bind("<d>", Player1.move)
win.bind("<s>", Player1.move)
win.bind("<a>", Player1.move)
win.bind("<r>", Player1.interact)

win.bind("<l>", lambda bound: battle([Player1], [test_foe1], "TestBackground"))

win.bind("<Escape>", exit)
win.mainloop()
