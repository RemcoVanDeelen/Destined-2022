from random import *

# definitions


def attack_check(self):

    try:
        if self.actions.index("H-Damage") >= 0:
            heavy_weight = self.actions[self.actions.index("H-Damage") + 2]
    except ValueError:
        heavy_weight = 0
    try:
        if self.actions.index("Heal") >= 0:
            heal_weight = self.actions[self.actions.index("Heal") + 2]
    except ValueError:
        heal_weight = 0
    normal_weight = self.actions[self.actions.index("Damage") + 2]

    # dice roll
    dice = randint(0, 100)

    if 0 < dice <= heal_weight:
        if self.health == self.max_health:
            action = attack_check(self)
        else:
            action = "Heal"
    elif dice <= heal_weight + heavy_weight:
        action = "H-Damage"
        try:
            self.actions.index(action)
        except ValueError:
            action = "Damage"
    elif dice <= heal_weight + heavy_weight + normal_weight:
        action = "Damage"
    return action
# enemy class


class Enemy:

    def __init__(self, health, max_health, speed, damage, evasion, crit_chance, actions, name, b_name, soul):
        self.health = health
        self.max_health = max_health
        self.speed = speed
        self.damage = damage
        self.evasion = evasion
        self.crit_chance = crit_chance
        self.actions = actions
        self.name = name
        self.b_name = b_name
        self.soul = soul

    # turn in battle
    def turn(self, player, shield, resistance):

        # actions
        action = attack_check(self)
        if action == "Heal":
            if self.health != self.max_health:
                idx = self.actions.index(action) + 1
                self.health += self.damage * self.actions[idx]
                print(self.name, "healed themself for", self.damage * self.actions[idx], "health.")
                if self.health > self.max_health:
                    self.health = self.max_health
            else:
                attack_check(self)
        elif action == "Damage" or "H-Damage":
            idx = self.actions.index(action) + 1
            if shield.counter >= 1:
                shield.counter -= 1
                print("The shield potion blocked the enemies attack!")
                if shield.counter == 0:
                    print("The shield has been broken.")
            else:
                dmg_resist = resistance.count(player)
                if randint(0, 100) <= self.crit_chance:
                    player.health -= self.damage * self.actions[idx] * 1.5 // dmg_resist
                else:
                    player.health -= self.damage * self.actions[idx] // dmg_resist
                print(self.name, "dealt", self.damage * self.actions[idx] // dmg_resist, "damage.")


# enemies

sheep_actions = ["Damage", 1, 100]
sheep1 = Enemy(15, 15, 10, 5, 8, 2, sheep_actions, "Sheep", "A SHEEP", 5)
sheep2 = Enemy(15, 15, 10, 5, 8, 2, sheep_actions, "Sheep", "A SHEEP", 5)
sheep3 = Enemy(15, 15, 10, 5, 8, 2, sheep_actions, "Sheep", "A SHEEP", 5)

orc_actions = ["Damage", 1, 60,  "H-Damage", 1.2, 40]
orc1 = Enemy(30, 30, 8, 7, 0, 12, orc_actions, "Orc", "AN ORC", 10)
orc2 = Enemy(30, 30, 8, 7, 0, 12, orc_actions, "Orc", "AN ORC", 10)
orc3 = Enemy(30, 30, 8, 7, 0, 12, orc_actions, "Orc", "AN ORC", 10)


orc_s_actions = ["Damage", 1, 50, "Heal", 2, 50]
orc_shaman1 = Enemy(20, 20, 7, 4, 2, 5, orc_s_actions, "Orc shaman", "AN ORC SHAMAN", 10)
orc_shaman2 = Enemy(20, 20, 7, 4, 2, 5, orc_s_actions, "Orc shaman", "AN ORC SHAMAN", 10)
orc_shaman3 = Enemy(20, 20, 7, 4, 2, 5, orc_s_actions, "Orc shaman", "AN ORC SHAMAN", 10)

griffin_actions = ["Damage", 1, 50, "H-Damage", 1.2, 50]
griffin = Enemy(40, 40, 15, 12, 10, 10, griffin_actions, "Griffin", "A GRIFFIN", 15)

none = Enemy(0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
