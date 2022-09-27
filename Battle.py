from random import randint
from Player_class import *


class Foe:
    def __init__(self, speed, max_health, evasion, soul, moves, name):
        # Stats
        self.speed = speed  # Speed stat for turn order,
        self.health = max_health  # Current health,
        self.max_health = max_health  # Maximum health,
        self.evasion = evasion  # percent chance to avoid being hit,
        self.soul = soul  # Soul received on kill,
        self.moves = moves  # List of moves,
        self.name = name  # Name
        self.status = []  # Current status effects

        for move in moves:
            setattr(self, move.__str__(), move)

    def turn(self, data):
        percent = []
        for move in self.moves:
            for _ in range(0, move.chance):
                percent.append(move)
        rng = randint(0, 100)
        percent[rng-1].function(data, percent[rng-1])


# imagery:
img_fight_button = PhotoImage(file="ButtonTest-Fight.png").zoom(6, 6)
img_magic_button = PhotoImage(file="ButtonTest-Magic.png").zoom(6, 6)
img_bag_button = PhotoImage(file="ButtonTest-Bag.png").zoom(6, 6)
img_action_button = PhotoImage(file="ButtonTest-Action.png").zoom(6, 6)

img_heavy_attack_button = PhotoImage(file="ButtonTest-Heavy_atk.png").zoom(6, 6)
img_light_attack_button = PhotoImage(file="ButtonTest-Light_atk.png").zoom(6, 6)

"""

'''
battle_frame = Frame(scr, width=scr.winfo_screenwidth() - 30, height=scr.winfo_screenheight() // 4 + 50)
battle_frame.place(x=15, y=1080 // 4 * 3 - 75)

text_frame = Frame(scr, width=scr.winfo_screenwidth() - 30, height=100, bg="#00FF00")
text_frame.place(x=15, y=1080 // 2 + 95)
'''  # background: (in lack of proper image, simple frames are placed. TestImage should come soon)

'''
fight_button = Button(scr, image=img_fight_button, borderwidth=0, highlightthickness=0)
magic_button = Button(scr, image=img_magic_button, borderwidth=0, highlightthickness=0)
bag_button = Button(scr, image=img_bag_button, borderwidth=0, highlightthickness=0)
action_button = Button(scr, image=img_action_button, borderwidth=0, highlightthickness=0)

fight_button.place(x=1920 / 5 - 48 * 3, y=845)
magic_button.place(x=1920 / 5 * 2 - 48 * 3, y=845)
bag_button.place(x=1920 / 5 * 3 - 48 * 3, y=845)
action_button.place(x=1920 / 5 * 4 - 48 * 3, y=845)
'''  # = Main button creation and placement =

'''
light_attack_button = Button(scr, image=img_light_attack_button, borderwidth=0, highlightthickness=0)
heavy_attack_button = Button(scr, image=img_heavy_attack_button, borderwidth=0, highlightthickness=0)

light_attack_button.place(x=1920 / 3 - 48 * 3, y=845)
heavy_attack_button.place(x=1920 / 3 * 2 - 48 * 3, y=845)
'''  # = Attack button creation and placement =

'''
class Spell:
    def __init__(self, img):
        self.image = img
        self.function = lambda: print("Test")


test = Player("test_player_object")
test.spells = [Spell(PhotoImage(file="ButtonTest-spell.png").zoom(6, 6)),
               Spell(PhotoImage(file="ButtonTest-spell.png").zoom(6, 6)),
               Spell(PhotoImage(file="ButtonTest-spell.png").zoom(6, 6)),
               Spell(PhotoImage(file="ButtonTest-spell.png").zoom(6, 6)),
               Spell(PhotoImage(file="ButtonTest-spell.png").zoom(6, 6))]

for spell in test.spells:
    button = Button(scr, image=spell.image, borderwidth=0, highlightthickness=0, command=spell.function)
    button.place(x=1920/(len(test.spells)+1)*(test.spells.index(spell)+1)-48*3, y=845)
'''  # = Magic button creation and placement =

'''
inventory_frame = Frame(scr, width=scr.winfo_screenwidth() - 40, height=scr.winfo_screenheight() // 4 + 40, bg="#554466")
inventory_frame.place(x=20, y=1080 // 4 * 3 - 70)
inventory_frame.pack_propagate(False)

test.inventory = [Spell(PhotoImage(file="ButtonTest-Item.png").zoom(6, 6)),
                  Spell(PhotoImage(file="ButtonTest-Item.png").zoom(6, 6)),
                  Spell(PhotoImage(file="ButtonTest-Item.png").zoom(6, 6)),
                  Spell(PhotoImage(file="ButtonTest-Item.png").zoom(6, 6)),
                  Spell(PhotoImage(file="ButtonTest-Item.png").zoom(6, 6)),
                  Spell(PhotoImage(file="ButtonTest-Item.png").zoom(6, 6)),
                  Spell(PhotoImage(file="ButtonTest-Item.png").zoom(6, 6)),
                  Spell(PhotoImage(file="ButtonTest-Item.png").zoom(6, 6)),
                  Spell(PhotoImage(file="ButtonTest-Item.png").zoom(6, 6)),
                  Spell(PhotoImage(file="ButtonTest-Item.png").zoom(6, 6)),
                  Spell(PhotoImage(file="ButtonTest-Item.png").zoom(6, 6)),
                  Spell(PhotoImage(file="ButtonTest-Item.png").zoom(6, 6)),
                  ]

temp_x = 0
temp_y = 1
for item in test.inventory:
    button = Button(inventory_frame, image=item.image, borderwidth=0, highlightthickness=0, command=item.function)

    temp_y += 1
    if test.inventory.index(item) % 3 == 0:
        temp_x += 1
        temp_y = 1
    button.place(x=temp_x*77*6-72*6, y=temp_y*16*6-16*6+10)
'''  # = Bag button creation and placement and other... requires revision =

"""  # ---------------- Display setting ----------------


def battle(players: list[Player], enemies: list[Foe], location):
    # Decide turn order:
    turn_order = []
    for _ in range(0, 30):
        turn_order.append(0)

    for player in players:
        rng = randint(player.speed - 2, player.speed + 2)
        while turn_order[rng] != 0:
            rng = randint(player.speed - 2, player.speed + 2)
        turn_order[rng] = player

    for foe in enemies:
        rng = turn_order.index(players[0])
        while turn_order[rng] != 0:
            rng = randint(foe.speed - 2, foe.speed + 2)
        turn_order[rng] = foe

    try:
        while True:
            turn_order.remove(0)
    except ValueError:
        turn_order.reverse()

    # Battle:
    living_foe = enemies[0:len(enemies)]
    living_players = players[0:len(players)]

    turn = 0
    turn_total = 0

    while len(living_players) > 0 and len(living_foe) > 0:
        battler = turn_order[turn]
        turn += 1
        turn_total += 1
        if turn >= len(turn_order):
            turn = 0

        if battler.health <= 0:
            continue

        # During turn
        for status_effect in battler.status:
            if status_effect.time == "start":
                status_effect.tick()
                if status_effect.count == 0:
                    battler.status.remove(status_effect)

        data = [living_players, living_foe]
        battler.turn(data)

        for status_effect in battler.status:
            if status_effect.time == "end":
                status_effect.tick()
                if status_effect.count == 0:
                    battler.status.remove(status_effect)

        # After turn
        for battler in turn_order:
            if battler.health <= 0:
                if battler in living_foe:
                    living_foe.remove(battler)
                elif battler in living_players:
                    living_players.remove(battler)
