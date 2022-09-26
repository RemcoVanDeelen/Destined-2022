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
