from Core import *
from random import randint
from Battle import end_turn, find_target


class Spell:
    def __init__(self, spell: str = "None",
                 img: PhotoImage = PhotoImage(file="images/Battle_GUI/ButtonTest-spell.png").zoom(6, 6)):

        self.cast = getattr(self, spell)
        self.image = img
        self.cooldown = 0

    def regenerate(self, data):
        # Check empowered,
        if empowered in data[2].status:
            data[2].status.remove(empowered)
            empower.cooldown = 3                        # FILLER cooldown.

        # Grant effect,
            data[2].status.append(regenerating_empowered)
        else:
            data[2].status.append(regenerating)

        # start cooldown.
        self.cooldown = 3                               # FILLER cooldown.
        print(1, self.cast)
        end_turn()

    def empower(self, data):
        # Grant effect.
        data[2].status.append(empowered)
        self.cooldown = True
        print(2, self.cast)
        end_turn()

    def lightning(self, data):
        # obtain target,
        target = find_target(data[1])

        # check empowered,
        if empowered in data[2].status:
            data[2].status.remove(empowered)
            empower.cooldown = 3                        # FILLER cooldown.

        # deal damage,
            target.health -= 15                         # FILLER damage.
        else:
            target.health -= 10                         # FILLER damage.

        # start cooldown.
        self.cooldown = 3                               # FILLER cooldown.
        print(3, self.cast)
        end_turn()

    def elemental_volley(self, data):
        shards = 3
        # Check empowered,
        if empowered in data[2].status:
            data[2].status.remove(empowered)
            empower.cooldown = 3                        # FILLER cooldown.
            shards = 5

        shard_list = []
        # define the shards,
        for shard in range(0, shards):
            if randint(0, 1) == 1:
                shard = 8                               # FILLER damage.
            else:
                shard = 4                               # FILLER damage.
            shard_list.append(shard)

        # deal damage to random targets,
        for shard in shard_list:
            target = data[1][randint(0, len(data[1])-1)]
            target.health -= shard

        # start cooldown.
        self.cooldown = 3                               # FILLER cooldown.
        print(4, self.cast)
        end_turn()

    def foresight(self, data):
        # Grant effect,
        data[2].status.append(foresight_effect)

        # Check empowered,
        if empowered in data[2].status:
            data[2].status.remove(empowered)
            empower.cooldown = 3                         # FILLER cooldown.

        # Grant effect [2],
            for foe in data[1]:
                foe.status.append(opponent_foresight_effect)

        else:
            if len(data[1]) > 2:
                enemies = data[1][0:3]
                target = enemies[randint(0, 2)]
                enemies.remove(target)
                target.status.append(opponent_foresight_effect)
                target = enemies[randint(0, 1)]
                enemies.remove(target)
                target.status.append(opponent_foresight_effect)
            else:
                for foe in data[1]:
                    foe.status.append(opponent_foresight_effect)

        # start cooldown.
        self.cooldown = 3                                # FILLER cooldown.
        print(5, self.cast)
        end_turn()

    def stasis(self, data):
        # obtain target,
        target = find_target(data[1])

        # Grant effect,
        target.status.append(stasis)

        # check empowered,
        if empowered in data[2].status:
            data[2].status.remove(empowered)
            empower.cooldown = 3                         # FILLER cooldown.
            cd = 2                                       # FILLER cooldown.
        else:
            cd = 4                                       # FILLER cooldown.

        # start cooldown.
        self.cooldown = cd
        print(6, self.cast)
        end_turn()

    def agility(self, data):
        # Passive, increases speed,
        # should always be disabled, no effect.
        print(7, self.cast)

    def weaken(self, data):
        # obtain target,
        target = find_target(data[1])

        # check empowered,
        if empowered in data[2].status:
            data[2].status.remove(empowered)
            empower.cooldown = 3                         # FILLER cooldown.

            dmg = 8                                     # FILLER damage.
            cd = 2                                      # FILLER cooldown.
        else:
            dmg = 5                                     # FILLER damage.
            cd = 3                                      # FILLER cooldown.

        # damage target,
        target.health -= dmg

        # Grant effect
        target.status.append(weakened),

        # start cooldown.
        self.cooldown = cd
        print(8, self.cast)
        end_turn()

    def fireball(self, data):
        # obtain target,
        target = find_target(data[1])

        # check empowered,
        if empowered in data[2].status:
            data[2].status.remove(empowered)
            empower.cooldown = 3                         # FILLER cooldown.

            # apply effect,
            target.status.append(burning)
            cd = 1                                       # FILLER cooldown.

        # damage target,
        else:
            target.health -= 6                           # FILLER damage.
            cd = 2                                       # FILLER cooldown.

        # start cooldown.
        self.cooldown = cd
        print(9, self.cast)
        end_turn()

    def stamina(self, data):
        # Passive, increases max_stamina,
        # should always be disabled, no effect.
        print(10, self.cast)

    def whirlwind(self, data):
        # check empowered,
        if empowered in data[2].status:
            data[2].status.remove(empowered)
            empower.cooldown = 3                         # FILLER cooldown.

        # damage all opponents,
            for foe in data[1]:
                foe.health -= 20                         # FILLER damage.
        else:
            for foe in data[1]:
                foe.health -= 10                         # FILLER damage.

        # start cooldown.
        self.cooldown = 3                                # FILLER cooldown.
        print(11, self.cast)
        end_turn()

    def enchant_weapon(self, data):
        # check empowered,
        if empowered in data[2].status:
            data[2].status.remove(empowered)
            empower.cooldown = 3                         # FILLER cooldown.

        # Grant effect,
            data[2].status.append(enchanted_weapon_empowered)
        else:
            data[2].status.append(enchanted_weapon)

        # start cooldown.
        self.cooldown = 3                               # FILLER cooldown.
        print(12, self.cast)
        end_turn()

    def recover(self, data):
        # check empowered,
        if empowered in data[2].status:
            data[2].status.remove(empowered)
            empower.cooldown = 3                         # FILLER cooldown.

        # regain stamina, possibly health too,
            data[2].health += 5                          # FILLER health.
            if data[2].health > data[2].max_health:
                data[2].health = data[2].max_health

            data[2].stamina += 15                        # FILLER stamina.
            if data[2].stamina > data[2].max_stamina:
                data[2].stamina = data[2].max_stamina

        else:
            data[2].stamina += 10                        # FILLER stamina.
            if data[2].stamina > data[2].max_stamina:
                data[2].stamina = data[2].max_stamina

        # start cooldown.
        self.cooldown = 3                                 # FILLER cooldown.
        print(13, self.cast)
        end_turn()

    def venom(self, data):
        # obtain target,
        target = find_target(data[1])

        # check empowered,
        if empowered in data[2].status:
            data[2].status.remove(empowered)
            empower.cooldown = 3                         # FILLER cooldown.

        # Grant effect,
            target.status.append(venom_effect_empowered)
        else:
            target.status.append(venom_effect)

        # start cooldown
        self.cooldown = 3                                # FILLER cooldown.
        print(14, self.cast)
        end_turn()

    def focus(self, data):
        # passive, decreases spell and item cooldown,
        # should always be disabled.
        print(15, self.cast)

    def calm(self, data):                               # Actions not yet defined.
        # check empowered,
        # obtain target,
        # skip actions,
        # start cooldown.
        print(16, self.cast)
        end_turn()

    def heal(self, data):
        # check empowered,
        if empowered in data[2].status:
            data[2].status.remove(empowered)
            empower.cooldown = 3                         # FILLER cooldown.

        # heal health,
            data[2].health += 15                         # FILLER health.
            if data[2].health > data[2].max_health:
                data[2].health = data[2].max_health
        else:
            data[2].health += 10                         # FILLER health.
            if data[2].health > data[2].max_health:
                data[2].health = data[2].max_health

        # start cooldown.
        self.cooldown = 3                                # FILLER cooldown.
        print(17, self.cast)
        end_turn()

    def barrier(self, data):
        # Grant effect,
        data[2].status.append(barrier_effect)

        # check empowered,
        if empowered in data[2].status:
            data[2].status.remove(empowered)
            empower.cooldown = 3                         # FILLER cooldown.

        # Grant effect [2]
            for foe in data[1]:
                foe.status.append(opponent_barrier_effect_empowered)
        else:
            for foe in data[1]:
                foe.status.append(opponent_barrier_effect)

        # start cooldown.
        self.cooldown = 3                                # FILLER cooldown.
        print(18, self.cast)
        end_turn()

    def chaotic_strike(self, data):                      # Stamina not yet defined.
        # check stamina requirement,
        # check empowered,
        # obtain target,
        # deal damage to target,
        # take stamina.
        print(19, self.cast)
        end_turn()

    def siphon(self, data):
        # obtain target,
        target = find_target(data[1])

        # check empowered,
        if empowered in data[2].status:
            data[2].status.remove(empowered)
            empower.cooldown = 3                         # FILLER cooldown.

            dmg = 15                                    # FILLER damage.
            healing = 15                                   # FILLER healing (should be %).
        else:
            dmg = 10                                    # FILLER damage.
            healing = 8                                    # FILLER healing (should be %).

        # deal damage to target,
        target.health -= dmg

        # heal caster,
        data[2].health += healing
        if data[2].health > data[2].max_health:
            data[2].health = data[2].max_health

        # start cooldown.
        self.cooldown = 3                               # FILLER cooldown
        print(20, self.cast)
        end_turn()

    def slow_time(self, data):
        # check empowered,                              # Effect not yet decided.

        # increase player.speed temporarily (possibly with status effect),
        # redo turn order,
        # start cooldown, start effect duration. { or not }

        # or:

        # set double turn to True,
        # start cooldown, start effect duration. { or not }
        print(21, self.cast)
        end_turn()


empower = Spell("empower", PhotoImage(file="images/Battle_GUI/ButtonTest-spell.png").zoom(6, 6))
regenerate = Spell("regenerate", PhotoImage(file="images/Battle_GUI/ButtonTest-spell.png").zoom(6, 6))
lightning = Spell("lightning", PhotoImage(file="images/Battle_GUI/ButtonTest-spell.png").zoom(6, 6))

elemental_volley = Spell("elemental_volley", PhotoImage(file="images/Battle_GUI/ButtonTest-spell.png").zoom(6, 6))
foresight = Spell("foresight", PhotoImage(file="images/Battle_GUI/ButtonTest-spell.png").zoom(6, 6))

stasis = Spell("stasis", PhotoImage(file="images/Battle_GUI/ButtonTest-spell.png").zoom(6, 6))
agility = Spell("agility", PhotoImage(file="images/Battle_GUI/ButtonTest-spell.png").zoom(6, 6))
weaken = Spell("weaken", PhotoImage(file="images/Battle_GUI/ButtonTest-spell.png").zoom(6, 6))

fireball = Spell("fireball", PhotoImage(file="images/Battle_GUI/ButtonTest-spell.png").zoom(6, 6))

stamina = Spell("stamina", PhotoImage(file="images/Battle_GUI/ButtonTest-spell.png").zoom(6, 6))
whirlwind = Spell("whirlwind", PhotoImage(file="images/Battle_GUI/ButtonTest-spell.png").zoom(6, 6))
enchant_weapon = Spell("enchant_weapon", PhotoImage(file="images/Battle_GUI/ButtonTest-spell.png").zoom(6, 6))

recover = Spell("recover", PhotoImage(file="images/Battle_GUI/ButtonTest-spell.png").zoom(6, 6))
venom = Spell("venom", PhotoImage(file="images/Battle_GUI/ButtonTest-spell.png").zoom(6, 6))

focus = Spell("focus", PhotoImage(file="images/Battle_GUI/ButtonTest-spell.png").zoom(6, 6))
calm = Spell("calm", PhotoImage(file="images/Battle_GUI/ButtonTest-spell.png").zoom(6, 6))
heal = Spell("heal", PhotoImage(file="images/Battle_GUI/ButtonTest-spell.png").zoom(6, 6))

barrier = Spell("elemental_volley", PhotoImage(file="images/Battle_GUI/ButtonTest-spell.png").zoom(6, 6))

chaotic_strike = Spell("chaotic_strike", PhotoImage(file="images/Battle_GUI/ButtonTest-spell.png").zoom(6, 6))
siphon = Spell("siphon", PhotoImage(file="images/Battle_GUI/ButtonTest-spell.png").zoom(6, 6))
slow_time = Spell("slow_time", PhotoImage(file="images/Battle_GUI/ButtonTest-spell.png").zoom(6, 6))

empowered = "FILLER"

regenerating = "FILLER"
regenerating_empowered = "FILLER"

foresight_effect = "FILLER"
opponent_foresight_effect = "FILLER"

enchanted_weapon = "FILLER"
enchanted_weapon_empowered = "FILLER"

barrier_effect = "FILLER"
opponent_barrier_effect = "FILLER"
opponent_barrier_effect_empowered = "FILLER"

weakened = "FILLER"

burning = "FILLER"

venom_effect = "FILLER"
venom_effect_empowered = "FILLER"