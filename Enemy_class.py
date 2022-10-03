from random import randint


class Foe:
    def __init__(self, speed, max_health, evasion, soul, moves, name, display):
        # Stats
        self.speed = speed  # Speed stat for turn order,
        self.health = max_health  # Current health,
        self.max_health = max_health  # Maximum health,
        self.evasion = evasion  # percent chance to avoid being hit,
        self.soul = soul  # Soul received on kill,
        self.moves = moves  # List of moves,
        self.name = name  # Name
        self.status = []  # Current status effects
        self.display = display

    def turn(self, _data):
        percent = []
        for move in self.moves:
            '''possible_targets = []
            if move.type == "heal-self":
                if 0 > self.health < self.max_health-2*100/95:
                    possible_targets.append(self)
            if move.type == "heal-ally":
                for ally in _data[1]:
                    if 0 > ally.health < ally.max_health*100/95:
                        possible_targets.append(ally)
            if move.type == "damage":
                possible_targets = _data[0]
            '''
            for _ in range(0, move.chance):
                percent.append(move)
        rng = randint(0, len(percent))
        percent[rng-1].function(_data, percent[rng-1])
        print(self.name, percent[rng-1].type)


class Move:
    def __init__(self, _type, chance, effect_multiplier, function):
        self.type = _type
        self.chance = chance
        self.effect_multiplier = effect_multiplier
        self.function = function


def harm(battle_data, move_data):
    targets = sorted(battle_data[0], key=lambda _: _.health)
    targets[0].health -= 4 * move_data.effect_multiplier


def heal_ally(battle_data, move_data):
    targets = sorted(battle_data[1], key=lambda _: _.health)
    targets[0].health += 4 * move_data.effect_multiplier
    if targets[0].health > targets[0].max_health:
        targets[0].health = targets[0].max_health


attack = Move("damage", 100, 1, harm)
attack2 = Move("damage", 50, 1, harm)
heal = Move("heal-ally", 50, 5, heal_ally)

from tkinter import PhotoImage
foe_img = PhotoImage(file="images/Battle_GUI/FoeTest.png").zoom(5, 5).subsample(2, 2)
Test_foe1 = Foe(8, 20, 0, 5, [attack], "TEST_FOE_NAME1", foe_img)
Test_foe2 = Foe(12, 15, 10, 5, [attack2, heal], "TEST_FOE_NAME2", foe_img)
Test_foe3 = Foe(5, 25, 0, 5, [attack], "TEST_FOE_NAME3", foe_img)
