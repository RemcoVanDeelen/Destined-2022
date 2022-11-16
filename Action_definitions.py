from Core import *
from random import randint
from Battle import end_turn, find_target, deal_damage
from Status_effects import *
import os


class Action:
    def __init__(self, function: str = "None",
                 img: PhotoImage = PhotoImage(file="images/Battle_GUI/Magic/1-SpellButtonTest-Regenerate.png".replace("/", os.sep)).zoom(2, 2),
                 value=0):
        """
        Class for defining player actions.\n
        The object can be put in inventory lists and holds:

        * Function (str name of function def),
        * Use cooldown,
        * Name (function variable),
        * Base store value.
        """
        self.use = getattr(self, function)
        self.image = img
        self.cooldown = 0
        self.name = function
        self.value = value

    # -   -  -  - - ---= SPELLS =--- - -  -  -   - #
    def regenerate(self, data):
        """Regenerate spell, grants regenerate effect to caster."""
        # Check empowered,
        empowered = next((_ for _ in data[2].status if _.effect == "empowered"), None)
        if empowered is not None:
            data[2].status.remove(empowered)
            empower.cooldown = 3

        # Grant effect,
            data[2].status.append(Effect("start", "regenerating_empowered", 3))
        else:
            data[2].status.append(Effect("start", "regenerating", 3))

        # start cooldown.
        self.cooldown = 3
        print(1, self.use)
        end_turn(3)

    def empower(self, data):
        """Empower spell, grants empowered effect to caster.\n
        * Cooldown started upon second spell cast."""
        # Grant effect.
        data[2].status.append(Effect(0, "empowered", True))
        self.cooldown = 999
        print(2, self.use)
        end_turn(3)

    def lightning(self, data):
        """Lightning spell, deals medium damage to target foe."""
        # obtain target,
        target = find_target(data[1])

        # check empowered,
        empowered = next((_ for _ in data[2].status if _.effect == "empowered"), None)
        if empowered is not None:
            data[2].status.remove(empowered)
            empower.cooldown = 3

        # deal damage,
            deal_damage(attacker=data[2], target=target, exact_damage=10, percent_damage=6, is_melee=False)
        else:
            deal_damage(attacker=data[2], target=target, exact_damage=8, percent_damage=4, is_melee=False)

        # start cooldown.
        self.cooldown = 3
        print(3, self.use)
        end_turn(3)

    def elemental_volley(self, data):
        """Elemental volley spell, deals small damage to random foes multiple times."""
        shards = 3
        # Check empowered,
        empowered = next((_ for _ in data[2].status if _.effect == "empowered"), None)
        if empowered is not None:
            data[2].status.remove(empowered)
            empower.cooldown = 3
            shards = 5

        shard_list = []
        # define the shards,
        for shard in range(0, shards):
            if randint(0, 1) == 1:
                shard = [6, 7]
            else:
                shard = [4, 5]
            shard_list.append(shard)

        # deal damage to random targets,
        for shard in shard_list:
            target = data[1][randint(0, len(data[1])-1)]
            deal_damage(attacker=data[2], target=target, is_melee=False, exact_damage=shard[0], percent_damage=shard[1])

        # start cooldown.
        self.cooldown = 4
        print(4, self.use)
        end_turn(3)

    def foresight(self, data):                                     # not implemented.
        """~NOT IMPLEMENTED~\n
        Foresight spell, would grant foresight de-buff to targets and foresight buff to caster."""
        # Grant effect,
        data[2].status.append(Effect("?", "foresight_effect", 4))

        # Check empowered,
        empowered = next((_ for _ in data[2].status if _.effect == "empowered"), None)
        if empowered is not None:
            data[2].status.remove(empowered)
            empower.cooldown = 3                         # FILLER cooldown.

        # Grant effect [2],
            for foe in data[1]:
                foe.status.append(Effect("?", "opponent_foresight_effect", 4))

        else:
            if len(data[1]) > 2:
                enemies = data[1][0:3]
                target = enemies[randint(0, 2)]
                enemies.remove(target)
                target.status.append(Effect("?", "opponent_foresight_effect", 4))
                target = enemies[randint(0, 1)]
                target.status.append(Effect("?", "opponent_foresight_effect", 4))
            else:
                for foe in data[1]:
                    foe.status.append(Effect("?", "opponent_foresight_effect", 4))

        # start cooldown.
        self.cooldown = 3                                # FILLER cooldown.
        print(5, self.use)
        end_turn(3)

    def stasis(self, data):
        """Stasis spell, grants stasis effect to target."""
        # obtain target,
        targets = []
        for foe in data[1]:
            if next((effect for effect in foe.status if effect.effect == "stasis_effect"), None) is None:
                targets.append(foe)
        target = find_target(targets)

        # Grant effect,
        target.status.append(Effect(0, "stasis_effect", 2))

        # check empowered,
        empowered = next((_ for _ in data[2].status if _.effect == "empowered"), None)
        if empowered is not None:
            data[2].status.remove(empowered)
            empower.cooldown = 3
            cd = 3
        else:
            cd = 5

        # start cooldown.
        self.cooldown = cd
        print(6, self.use)
        end_turn(3)

    def agility(self, data):                # not implemented
        """~NOT IMPLEMENTED~\n
        Agility spell [passive], increases player speed."""
        # Passive, increases speed,
        # should always be disabled, no effect.
        print(7, self.use)

    def weaken(self, data):
        """Weaken spell, grants weakened effect and deals minor damage to target."""
        # obtain target,
        target = find_target(data[1])

        # check empowered,
        empowered = next((_ for _ in data[2].status if _.effect == "empowered"), None)
        if empowered is not None:
            data[2].status.remove(empowered)
            empower.cooldown = 3                         # FILLER cooldown.

            deal_damage(attacker=data[2], target=target, exact_damage=3, percent_damage=4, is_melee=False)
            cd = 2                                      # FILLER cooldown.
        else:
            deal_damage(attacker=data[2], target=target, exact_damage=2, percent_damage=3, is_melee=False)
            cd = 3                                      # FILLER cooldown.

        # Grant effect
        target.status.append(Effect("end", "weakened", 4)),

        # start cooldown.
        self.cooldown = cd
        print(8, self.use)
        end_turn(3)

    def fireball(self, data):
        """Fireball spell, deals minor damage {and grants burning effect} to target."""
        # obtain target,
        target = find_target(data[1])

        # check empowered,
        empowered = next((_ for _ in data[2].status if _.effect == "empowered"), None)
        if empowered is not None:
            data[2].status.remove(empowered)
            empower.cooldown = 3                         # FILLER cooldown.

            # apply effect,
            target.status.append(Effect("end", "burning", 3))
            cd = 1                                       # FILLER cooldown.

        else:
            cd = 2                                       # FILLER cooldown.

        # deal damage,
        deal_damage(attacker=data[2], target=target, exact_damage=5, percent_damage=6, is_melee=False)

        # start cooldown.
        self.cooldown = cd
        print(9, self.use)
        end_turn(3)

    def stamina(self, data):                    # not implemented
        """~NOT IMPLEMENTED~\n
        Stamina spell [passive], increases player max_stamina."""
        # Passive, increases max_stamina,
        # should always be disabled, no effect.
        print(10, self.use)

    def whirlwind(self, data):
        """Whirlwind spell, deals minor damage to all foes."""
        # check empowered,
        empowered = next((_ for _ in data[2].status if _.effect == "empowered"), None)
        if empowered is not None:
            data[2].status.remove(empowered)
            empower.cooldown = 3                         # FILLER cooldown.

        # damage all opponents,
            for foe in data[1]:
                deal_damage(attacker=data[2], target=foe, exact_damage=8, percent_damage=14, is_melee=False)
        else:
            for foe in data[1]:
                deal_damage(attacker=data[2], target=foe, exact_damage=5, percent_damage=10, is_melee=False)

        # start cooldown.
        self.cooldown = 3                                # FILLER cooldown.
        print(11, self.use)
        end_turn(3)

    def enchant_weapon(self, data):
        """Enchant weapon spell, grants enchanted weapon effect to caster.\n
        * Cooldown starts after melee attacking."""
        # check empowered,
        empowered = next((_ for _ in data[2].status if _.effect == "empowered"), None)
        if empowered is not None:
            data[2].status.remove(empowered)
            empower.cooldown = 3                         # FILLER cooldown.

        # Grant effect,
            data[2].status.append(Effect("attacking", "enchanted_weapon_empowered", 2))
        else:
            data[2].status.append(Effect("attacking", "enchanted_weapon", 2))

        # start cooldown.
        self.cooldown = 999
        print(12, self.use)
        end_turn(3)

    def recover(self, data):
        """Recover spell, regains a little of the caster's stamina {and health}."""
        # check empowered,
        empowered = next((_ for _ in data[2].status if _.effect == "empowered"), None)
        if empowered is not None:
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
        print(13, self.use)
        end_turn(3)

    def venom(self, data):
        """Venom spell, grants venom effect to target."""
        # obtain target,
        target = find_target(data[1])

        # check empowered,
        empowered = next((_ for _ in data[2].status if _.effect == "empowered"), None)
        if empowered is not None:
            data[2].status.remove(empowered)
            empower.cooldown = 3                         # FILLER cooldown.

        # Grant effect,
            target.status.append(Effect("always", "venom_empowered", 5))
        else:
            target.status.append(Effect("end", "venom", 4))

        # start cooldown
        self.cooldown = 4
        print(14, self.use)
        end_turn(3)

    def focus(self, data):                              # not implemented
        """~NOT IMPLEMENTED~\n
        Focus spell [passive], decreases player spell and item cooldown by 1."""
        # passive, decreases spell and item cooldown,
        # should always be disabled.
        print(15, self.use)

    def calm(self, data):                               # Actions not implemented.
        """~NOT IMPLEMENTED~\n
        Calm spell, would be used to defeat foes without dealing damage, complementing the scrapped actions system."""
        # check empowered,
        # obtain target,
        # skip actions,
        # start cooldown.
        print(16, self.use)
        end_turn(3)

    def heal(self, data):
        """Heal spell, regains a moderate amount of the caster's health."""
        # check empowered,
        empowered = next((_ for _ in data[2].status if _.effect == "empowered"), None)
        if empowered is not None:
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
        print(17, self.use)
        end_turn(3)

    def barrier(self, data):                            # Not implemented
        """~NOT IMPLEMENTED~\n
        Barrier spell, would grant barrier de-buff to all foes and barrier buff to caster."""
        # Grant effect,
        data[2].status.append(Effect("?", "barrier_effect", 4))

        # check empowered,
        empowered = next((_ for _ in data[2].status if _.effect == "empowered"), None)
        if empowered is not None:
            data[2].status.remove(empowered)
            empower.cooldown = 3                         # FILLER cooldown.

        # Grant effect [2]
            for foe in data[1]:
                foe.status.append(Effect("?", "opponent_barrier_effect_empowered", 4))
        else:
            for foe in data[1]:
                foe.status.append(Effect("?", "opponent_barrier_effect", 4))

        # start cooldown.
        self.cooldown = 3                                # FILLER cooldown.
        print(18, self.use)
        end_turn(3)

    def chaotic_strike(self, data):
        """Chaotic strike spell, deals moderate damage to target at the cost of stamina rather than a cooldown."""
        # check empowered,
        empowered = next((_ for _ in data[2].status if _.effect == "empowered"), None)
        if empowered is not None:
            data[2].status.remove(empowered)
            empower.cooldown = 3

            dmg = 22
            pct_dmg = 12
            stamina_req = 12
            stamina_cost = 9
        else:
            dmg = 18
            pct_dmg = 9
            stamina_req = 16
            stamina_cost = 12

        # check stamina requirement,
        if data[2].stamina >= stamina_req:

            # obtain target,
            target = find_target(data[1])

            # deal damage to target,
            deal_damage(attacker=data[2], target=target, is_melee=False, exact_damage=dmg, percent_damage=pct_dmg)

            # take stamina.
            data[2].stamina -= stamina_cost
            print(19, self.use)
            end_turn(0)

    def siphon(self, data):
        """Siphon spell, deals minor damage to target and regains part of the dealt damage as health to the caster."""
        # obtain target,
        target = find_target(data[1])

        # check empowered,
        empowered = next((_ for _ in data[2].status if _.effect == "empowered"), None)
        if empowered is not None:
            data[2].status.remove(empowered)
            empower.cooldown = 3                         # FILLER cooldown.

            healing = deal_damage(attacker=data[2], target=target, is_melee=False, exact_damage=10, percent_damage=5)
        else:
            healing = deal_damage(attacker=data[2], target=target, is_melee=False, exact_damage=8, percent_damage=5) * 0.8

        # heal caster,
        data[2].health += round(healing)
        if data[2].health > data[2].max_health:
            data[2].health = data[2].max_health

        # start cooldown.
        self.cooldown = 3
        print(20, self.use)
        end_turn(3)

    def slow_time(self, data):            # Not implemented.
        """~NOT IMPLEMENTED~\n
        Slow time spell, would do one of the effect mentioned in spell def. True effect not decided and thus scrapped."""
        # check empowered,

        # increase player.speed temporarily (possibly with status effect),
        # redo turn order,
        # start cooldown, start effect duration. { or not }

        # or:

        # set double turn to True,
        # start cooldown, start effect duration. { or not }
        print(21, self.use)
        end_turn(3)

    # -   -  -  - - ---= ITEMS =--- - -  -  -   - #
    def health_potion(self, data):
        """Health potion item, regains a moderate amount of the user's health."""
        data[2].health += 15
        if data[2].health > data[2].max_health:
            data[2].health = data[2].max_health
        data[2].inventory.remove(self)
        self.cooldown = 3

        print("A", self.use)
        end_turn(3)

    def large_health_potion(self, data):
        """Large health potion item, regains a large amount of the user's health."""
        data[2].health += 30
        if data[2].health > data[2].max_health:
            data[2].health = data[2].max_health
        data[2].inventory.remove(self)
        self.cooldown = 3                           # FILLER cooldown.

        print("B", self.use)
        end_turn(3)

    def stamina_potion(self, data):
        """Stamina potion item, regains a moderate amount of the user's stamina."""
        data[2].stamina += 8
        if data[2].stamina > data[2].max_stamina:
            data[2].stamina = data[2].max_stamina
        data[2].inventory.remove(self)
        self.cooldown = 3                           # FILLER cooldown.

        print("C", self.use)
        end_turn(3)

    def large_stamina_potion(self, data):
        """Large stamina potion item, regains a large amount of the user's stamina."""
        data[2].stamina += 15
        if data[2].stamina > data[2].max_stamina:
            data[2].stamina = data[2].max_stamina
        data[2].inventory.remove(self)
        self.cooldown = 3                           # FILLER cooldown.

        print("D", self.use)
        end_turn(3)

    def strength_potion(self, data):
        """Strength potion item, grants strength effect to user."""
        data[2].status.append(Effect("attacking", "strength", 4))
        data[2].inventory.remove(self)
        self.cooldown = 3                           # FILLER cooldown.

        print("E", self.use)
        end_turn(3)

    def vitality_potion(self, data):
        """Vitality potion item, increases users max health and regains it."""
        data[2].health += 5
        data[2].max_health += 5
        data[2].inventory.remove(self)

        print("F", self.use)
        end_turn(3)

    def shield_potion(self, data):
        """Shield potion item, grants shielded effect to user."""
        data[2].status.append(Effect("attacked", "shielded", 3))
        data[2].inventory.remove(self)
        self.cooldown = 5                           # FILLER cooldown.

        print("G", self.use)
        end_turn(3)

    def resistance_potion(self, data):
        """Resistance potion item, grants resistance effect to user."""
        data[2].status.append(Effect("attacked", "resistance", 5))
        data[2].inventory.remove(self)
        self.cooldown = 3                           # FILLER cooldown.

        print("H", self.use)
        end_turn(3)

    def staminaless_potion(self, data):
        """Staminaless potion item, grants staminaless effect to user or increases its duration."""
        add = False
        for status in data[2].status:
            if status.effect == "staminaless":
                add = True
                status.duration += 5

        if not add:
            data[2].light_atk_cost -= 2
            data[2].heavy_atk_cost -= 2
            data[2].status.append(Effect("unique", "staminaless", 5))
        data[2].inventory.remove(self)
        self.cooldown = 3                           # FILLER cooldown.

        print("I", self.use)
        end_turn(3)


# - OBJECTS -
# Spells
regenerate = Action("regenerate", PhotoImage(file="images/Battle_GUI/Magic/1-SpellButtonTest-Regenerate.png".replace("/", os.sep)).zoom(2, 2))                       # 1
empower = Action("empower", PhotoImage(file="images/Battle_GUI/Magic/2-SpellButtonTest-Empower.png".replace("/", os.sep)).zoom(2, 2))                                # 2
lightning = Action("lightning", PhotoImage(file="images/Battle_GUI/Magic/3-SpellButtonTest-Lightning.png".replace("/", os.sep)).zoom(2, 2))                          # 3

elemental_volley = Action("elemental_volley", PhotoImage(file="images/Battle_GUI/Magic/4-SpellButtonTest-Elemental_volley.png".replace("/", os.sep)).zoom(2, 2))     # 4
# foresight = Action("foresight", PhotoImage(file="images/Battle_GUI/Magic/5-SpellButtonTest-Foresight.png".replace("/", os.sep)).zoom(2, 2))                          # 5

stasis = Action("stasis", PhotoImage(file="images/Battle_GUI/Magic/6-SpellButtonTest-Stasis.png".replace("/", os.sep)).zoom(2, 2))                                   # 6
# agility = Action("agility", PhotoImage(file="images/Battle_GUI/Magic/7-SpellButtonTest-Agility.png".replace("/", os.sep)).zoom(2, 2))                                # 7
weaken = Action("weaken", PhotoImage(file="images/Battle_GUI/Magic/8-SpellButtonTest-Weaken.png".replace("/", os.sep)).zoom(2, 2))                                   # 8

fireball = Action("fireball", PhotoImage(file="images/Battle_GUI/Magic/9-SpellButtonTest-Fireball.png".replace("/", os.sep)).zoom(2, 2))                             # 9

# stamina = Action("stamina", PhotoImage(file="images/Battle_GUI/Magic/10-SpellButtonTest-Stamina.png".replace("/", os.sep)).zoom(2, 2))                               # 10
whirlwind = Action("whirlwind", PhotoImage(file="images/Battle_GUI/Magic/11-SpellButtonTest-Whirlwind.png".replace("/", os.sep)).zoom(2, 2))                         # 11
enchant_weapon = Action("enchant_weapon", PhotoImage(file="images/Battle_GUI/Magic/12-SpellButtonTest-Enchant_weapon.png".replace("/", os.sep)).zoom(2, 2))          # 12

recover = Action("recover", PhotoImage(file="images/Battle_GUI/Magic/13-SpellButtonTest-Recover.png".replace("/", os.sep)).zoom(2, 2))                               # 13
venom = Action("venom", PhotoImage(file="images/Battle_GUI/Magic/14-SpellButtonTest-Venom.png".replace("/", os.sep)).zoom(2, 2))                                     # 14

# focus = Action("focus", PhotoImage(file="images/Battle_GUI/Magic/15-SpellButtonTest-Focus.png".replace("/", os.sep)).zoom(2, 2))                                     # 15
# calm = Action("calm", PhotoImage(file="images/Battle_GUI/Magic/16-SpellButtonTest-Calm.png".replace("/", os.sep)).zoom(2, 2))                                        # 16
heal = Action("heal", PhotoImage(file="images/Battle_GUI/Magic/17-SpellButtonTest-Heal.png".replace("/", os.sep)).zoom(2, 2))                                        # 17

# barrier = Action("barrier", PhotoImage(file="images/Battle_GUI/Magic/18-SpellButtonTest-Barrier.png".replace("/", os.sep)).zoom(2, 2))                      # 18

chaotic_strike = Action("chaotic_strike", PhotoImage(file="images/Battle_GUI/Magic/19-SpellButtonTest-Chaotic_strike.png".replace("/", os.sep)).zoom(2, 2))          # 19
siphon = Action("siphon", PhotoImage(file="images/Battle_GUI/Magic/20-SpellButtonTest-Siphon.png".replace("/", os.sep)).zoom(2, 2))                                  # 20
# slow_time = Action("slow_time", PhotoImage(file="images/Battle_GUI/Magic/21-SpellButtonTest-Slow_time.png".replace("/", os.sep)).zoom(2, 2))                         # 21

# Items
health_potion = Action("health_potion", PhotoImage(file="images/Inventory_GUI/ItemButtonTest-Health_potion.png".replace("/", os.sep)).zoom(2, 2), 8)                                    # A
large_health_potion = Action("large_health_potion", PhotoImage(file="images/Inventory_GUI/ItemButtonTest-Large_Health_potion.png".replace("/", os.sep)).zoom(2, 2), 10)                  # B

stamina_potion = Action("stamina_potion", PhotoImage(file="images/Inventory_GUI/ItemButtonTest-Stamina_potion.png".replace("/", os.sep)).zoom(2, 2), 8)                                 # C
large_stamina_potion = Action("large_stamina_potion", PhotoImage(file="images/Inventory_GUI/ItemButtonTest-Large_Stamina_potion.png".replace("/", os.sep)).zoom(2, 2), 10)               # D

strength_potion = Action("strength_potion", PhotoImage(file="images/Inventory_GUI/ItemButtonTest-Strength_potion.png".replace("/", os.sep)).zoom(2, 2), 15)                              # E

vitality_potion = Action("vitality_potion", PhotoImage(file="images/Inventory_GUI/ItemButtonTest-Vitality_potion.png".replace("/", os.sep)).zoom(2, 2), 20)                              # F

shield_potion = Action("shield_potion", PhotoImage(file="images/Inventory_GUI/ItemButtonTest-Shield_potion.png".replace("/", os.sep)).zoom(2, 2), 20)                                    # G
resistance_potion = Action("resistance_potion", PhotoImage(file="images/Inventory_GUI/ItemButtonTest-Resistance_potion.png".replace("/", os.sep)).zoom(2, 2), 15)                        # H

staminaless_potion = Action("staminaless_potion", PhotoImage(file="images/Inventory_GUI/ItemButtonTest-Staminaless_potion.png".replace("/", os.sep)).zoom(2, 2), 15)                     # I
