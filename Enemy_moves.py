

class Move:
    def __init__(self, _type, chance, effect_multiplier, function):
        self.type = _type
        self.chance = chance
        self.effect_multiplier = effect_multiplier
        self.function = function


def kill(battle_data, move_data):
    targets = sorted(battle_data[0], key=lambda _: _.health)
    targets[0].health -= 4


attack = Move("damage", 100, 1, kill)
