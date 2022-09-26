from random import *

#    weapon definitions

# weapon class


class Weapon:

    def __init__(self, damage, speed, evasion, crit_chance, light_cost, heavy_cost, name):
        self.damage = damage
        self.speed = speed
        self.evasion = evasion
        self.crit_chance = crit_chance
        self.light_cost = light_cost
        self.heavy_cost = heavy_cost
        self.name = name

    def pickup(self, player):
        player.weapon = self
        player.speed = self.speed


# weapons

no_weapon = Weapon(6.5, 10, 10, 10, 5, 8, "An Illegal Item!")

DDaggers = Weapon(7, 20, 20, 5, 3, 6, "Double Daggers")

SSword = Weapon(9, 15, 15, 7.5, 4, 7, "Short Sword")

Sword = Weapon(10, 10, 10, 10, 5, 8, "Sword")

BAxe = Weapon(12, 6, 7.5, 15, 6, 9, "Battle Axe")

Hammer = Weapon(15, 1, 5, 20, 7, 10, "Hammer")


#    player definition


class Player:

    def __init__(self, soul, soul_req, level, health, max_health, stamina, max_stamina, bag, bag_slots, ingredients,
                 spells, weapon, spell_tags):
        self.soul = soul
        self.soul_req = soul_req
        self.level = level
        self.health = health
        self.max_health = max_health
        self.stamina = stamina
        self.max_stamina = max_stamina
        self.bag = bag
        self.bag_slots = bag_slots
        self.ingredients = ingredients
        self.spells = spells
        self.weapon = weapon
        self.speed = self.weapon.speed
        self.spell_tags = spell_tags

    def level_up(self):
        if self.soul >= self.soul_req:
            self.soul -= self.soul_req

            self.max_health += 5
            self.health += self.max_health // 4
            if self.health > self.max_health:
                self.health = self.max_health

            self.max_stamina += 5
            self.stamina += 5

            self.soul_req *= 1.5
            self.level += 1

            if self.level == 3 or 5 or 7 or 9:
                no_weapon.damage += 0.5
                DDaggers.damage += 0.5
                SSword.damage += 0.5
                Sword.damage += 0.5
                BAxe.damage += 0.5
                Hammer.damage += 0.5

            print("LEVEL UP, FILLER")


Bag = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
Ingredients = []
Spells = ()
spell_list = ["", "", "", "", ""]
Player1 = Player(0, 15, 1, 50, 50, 30, 30, Bag, 0, Ingredients, Spells, no_weapon, spell_list)

#    item definitions


# bag opening

def open_bag(user):
    i_list = ""
    counter = user.bag_slots - 1
    while counter >= 0:
        Cd = str(user.bag[counter].counter)
        if counter == 0:
            i_list += user.bag[counter].name + " {" + Cd + "}" + "."
        else:
            i_list += user.bag[counter].name + " {" + Cd + "}" + ", "
        counter -= 1
    return i_list

# item class


class Item:

    def __init__(self, name, cooldown):
        self.name = name
        self.cooldown = cooldown
        self.counter = 0

    def use(self, user, strength=0, resistance=0, shield=0):
        try:
            if user.bag.index(self) >= 0:
                if self.counter == 0:
                    user.bag_slots -= 1
                    user.bag.pop(user.bag.index(self))
                    user.bag += ""
                    item_effect(self, user, strength, resistance, shield)
                    self.counter = self.cooldown
                else:
                    print("This item is still under cooldown. \n Cooldown:", self.counter)
        except ValueError:
            print("You do not have that item.")

    def pickup(self, user):
        user.bag[user.bag_slots] = self
        user.bag_slots += 1


# items

health_potion = Item("Health potion", 2)

large_health_potion = Item("Large health potion", 3)

stamina_potion = Item("Stamina potion", 3)

large_stamina_potion = Item("Large stamina potion", 4)

vitality_potion = Item("Vitality potion", 5)

strength_potion = Item("Strength potion", 3)

resistance_potion = Item("Resistance potion", 3)

shield_potion = Item("Shield potion", 3)

staminaless_potion = Item("Staminaless potion", 3)

# item_class = Item("Name") #

# remaining item definitions


def check_item(item, user, strength, resistance, shield):
    if item == health_potion.name:
        health_potion.use(user)
    elif item == large_health_potion.name:
        large_health_potion.use(user)
    elif item == stamina_potion.name:
        stamina_potion.use(user)
    elif item == large_stamina_potion.name:
        large_stamina_potion.use(user)
    elif item == vitality_potion.name:
        vitality_potion.use(user)
    elif item == strength_potion.name:
        strength_potion.use(user, strength=strength)
    elif item == resistance_potion.name:
        resistance_potion.use(user, resistance=resistance)
    elif item == staminaless_potion.name:
        staminaless_potion.use(user)
    elif item == shield_potion.name:
        shield_potion.use(user, shield=shield)


def item_effect(item, user, strength=0, resistance=0, shield=0):

    if item == health_potion:
        user.health += 20
        if user.health >= user.max_health:
            user.health = user.max_health
        print("Your wounds close instantly.")

    if item == large_health_potion:
        user.health += 40
        if user.health >= user.max_health:
            user.health = user.max_health
        print("Your wounds close instantly.")

    if item == stamina_potion:
        user.stamina += 16
        print("You feel a newfound energy course through your body.")

    if item == large_stamina_potion:
        user.stamina += 35
        print("You feel a newfound energy course through your body.")

    if item == vitality_potion:
        user.max_health += 10
        user.health += 10
        print("You feel more healthy.")

    if item == strength_potion:
        strength.counter += 4
        print("You feel stronger than before.")

    if item == resistance_potion:
        resistance.counter += 5
        print("FILLER")

    if item == shield_potion:
        shield.counter += 3
        print("FILLER")


# Magic system

class Spell:

    def __init__(self, tag, name):
        self.tag = tag
        self.name = name
        self.cast = 5

    def learn(self, player, num):
        if num == 0:
            player.spells = self.name
        else:
            player.spells = (player.spells, ",", self.name)
        player.spell_tags[num] = self.tag

#'''
def regen_spell(spell, caster, empowered, stasis, regen, target=None):
    regen.counter += 3

def empower_spell(spell, caster, empowered, stasis, regen, target=None):
    empowered = True

def lightning_spell(spell, caster, empowered, stasis, regen, target=None):
    pass  # FILLER DAMAGE


def e_volley_spell(spell, caster, empowered, stasis, regen, target=None):
    pass  # FILLER MULTIPLE DAMAGE

def sitw_spell(spell, caster, empowered, stasis, regen, target=None):
    pass  # FILLER BUFF?

def stasis_spell(spell, caster, empowered, stasis, regen, target=None):
    stasis.counter += 2

def agile_passive(spell, caster, empowered, stasis, regen, target=None):
    caster.speed += 5

def weak_spell(spell, caster, empowered, stasis, regen, target=None):
    pass  # FILLER DEBUFF

def fireball_spell(spell, caster, empowered, stasis, regen, target=None):
    pass  # FILLER DAMAGE

def stamina_passive(spell, caster, empowered, stasis, regen, target=None):
    caster.max_stamina += 15
    caster.stamina += 15

def whirlwind_spell(spell, caster, empowered, stasis, regen, target=None):
    pass  # FILLER DAMAGE

def enchant_spell(spell, caster, empowered, stasis, regen, target=None):
    pass  # FILLER BEEG_DAMAGE_BUFF + 1

def recover_spell(spell, caster, empowered, stasis, regen, target=None):
    caster.health += caster.max_health//3
    if caster.health >= caster.max_health:
        caster.health = caster.max_health

def venom_spell(spell, caster, empowered, stasis, regen, target=None):
    pass  # FILLER SOMEHOW ADDS POISON TO AN ENEMY

Regenerate = Spell(1, "Regenerate")
Regenerate.cast = regen_spell
Empower = Spell(2, "Empower")
Empower.cast = empower_spell
Lightning = Spell(3, "Lightning")
Lightning.cast = lightning_spell

E_Volley = Spell(4, "Elemental volley")
E_Volley.cast = e_volley_spell
Straw_itW = Spell(5, "Straw in the wind")
Straw_itW.cast = sitw_spell

Stasis = Spell(6, "Stasis")
Stasis.cast = stasis_spell
Agility = Spell(7, "Agility")
Agility.cast = agile_passive
Weaken = Spell(8, "Weaken")
Weaken.cast = weak_spell

Fireball = Spell(9, "Fireball")
Fireball.cast = fireball_spell

Stamina = Spell(10, "Stamina")
Stamina.cast = stamina_passive
Whirlwind = Spell(11, "Whirlwind")
Whirlwind.cast = whirlwind_spell
Enchant = Spell(12, "Enchant weapon")
Enchant.cast = enchant_spell

Recover = Spell(13, "Recover")
Recover.cast = recover_spell
Venom = Spell(14, "Venom")
Venom.cast = venom_spell

Focus = Spell(15, "Focus")
# ---CONTINUE HERE---
Calm = Spell(16, "Calm")
Heal = Spell(17, "Heal")

Barrier = Spell(18, "Barrier")

C_Strike = Spell(19, "Chaotic strike")
Siphon = Spell(20, "Siphon")
TS_bubble = Spell(21, "Time-Slow-bubble")
# '''
