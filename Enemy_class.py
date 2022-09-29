from random import randint


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

    def turn(self, _data):
        percent = []
        for move in self.moves:
            for _ in range(0, move.chance):
                percent.append(move)
        rng = randint(0, 100)
        percent[rng-1].function(_data, percent[rng-1])


class Move:
    def __init__(self, _type, chance, effect_multiplier, function):
        self.type = _type
        self.chance = chance
        self.effect_multiplier = effect_multiplier
        self.function = function


def kill(battle_data, move_data):
    targets = sorted(battle_data[0], key=lambda _: _.health)
    targets[0].health -= 4 * move_data.effect_multiplier


attack = Move("damage", 100, 1, kill)
