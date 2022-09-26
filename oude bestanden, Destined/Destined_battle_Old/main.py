import random
import spells
import inventory_data


# weapon definitions
class weapon:

    def __init__(self, damagestat, speed, equipped):
        self.damagestat = damagestat
        self.speed = speed
        self.equipped = equipped


weapon_none = weapon(5, 10, True)

weapon_DDaggers = weapon(7, 20, False)

weapon_SSword = weapon(9, 15, False)

weapon_Sword = weapon(10, 10, False)

weapon_BAxe = weapon(12, 6, False)

weapon_Hammer = weapon(15, 1, False)


# player stats


class player:

    def __init__(self, name, health, max_health, stamina, max_stamina, Soul, Level, Soul_req, spells,
                 inventory_used, inventory, ingredient_pouch):
        self.name = name
        self.health = health
        self.max_health = max_health
        self.stamina = stamina
        self.max_stamina = max_stamina
        self.Soul = Soul
        self.Level = Level
        self.Soul_req = Soul_req
        self.spells = spells
        self.inventory_used = inventory_used
        self.inventory = inventory
        self.ingredient_pouch = ingredient_pouch


ingredient_pouch = []
inventory = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
known_spells = ["", "", "", "", ""]

Player1 = player("Player1", 20, 20, 20, 20, 0, 1, 20, known_spells, 0, inventory, ingredient_pouch)

# other stats
equippedweapon = weapon_none
light_difference = 0.8
heavy_difference = 1.2

# enemy definitions


class enemy:

    def __init__(self, name, battle_name, damagestat, speed, maxhealth_e, health_e):
        self.name = name
        self.battle_name = battle_name
        self.damagestat = damagestat
        self.speed = speed
        self.maxhealth_e = maxhealth_e
        self.health_e = health_e


enemy_Sheep = enemy("Sheep", "A SHEEP", 5, 10, 10, 10)
enemy_Orc = enemy("Orc", "AN ORC", 6, 8, 30, 30)

# action definitions


def learn_spell(spell_number, spell):
    known_spells[spell_number] = spell


def show_spells(user):
    if user.spells[0] != "":
        if user.spells[1] != "":
            if user.spells[2] != "":
                if user.spells[3] != "":
                    if user.spells[4] != "":
                        spell_message = user.spells[0] + ", " + user.spells[1] + ", " + user.spells[2] + \
                                        ", " + user.spells[3] + ", " + user.spells[4] + "."
                    else:
                        spell_message = user.spells[0] + ", " + user.spells[1] + ", " + user.spells[2] + \
                                        ", " + user.spells[3] + "."
                else:
                    spell_message = user.spells[0] + ", " + user.spells[1] + "," + user.spells[2] + "."
            else:
                spell_message = user.spells[0] + ", " + user.spells[1] + "."
        else:
            spell_message = user.spells[0] + "."
    else:
        spell_message = "None"
    return spell_message


def weapon_check():
    if weapon_none.equipped is True:
        equippedweapon = weapon_none
    elif weapon_Hammer.equipped is True:
        equippedweapon = weapon_Hammer
    elif weapon_BAxe.equipped is True:
        equippedweapon = weapon_BAxe
    elif weapon_Sword.equipped is True:
        equippedweapon = weapon_Sword
    elif weapon_SSword.equipped is True:
        equippedweapon = weapon_SSword
    else:
        equippedweapon = weapon_DDaggers
    return equippedweapon


def pickup(weapon):
    weapon_Hammer.equipped = False
    weapon_none.equipped = False
    weapon_BAxe.equipped = False
    weapon_DDaggers.equipped = False
    weapon_SSword.equipped = False
    weapon_Sword.equipped = False
    weapon.equipped = True
    weapon_check()


def battle(foe, user):
    user.stamina += user.max_stamina//5 * 4
    if user.stamina >= user.max_stamina:
        user.stamina = user.max_stamina
    stasis_counter = 0
    regen_counter = 0
    strength_counter = 0
    resistance_counter = 0
    shield = 0
    staminaless_counter = 0
    empowered = False
    held_weapon = weapon_check()
    if held_weapon.speed >= foe.speed:
        turn = True
    else:
        turn = False
    while user.health > 0 and foe.health_e > 0:
        if turn is True:
            if regen_counter >> 0:
                user.health += user.max_health//15
                if user.health >= user.max_health:
                    user.health = user.max_health
                regen_counter -= 1
            if staminaless_counter > 0:
                staminaless_counter -= 1
                if staminaless_counter == 0:
                    print("Your movement feels like normal again.")
            print("You currently have", user.health, "health. and", user.stamina, "stamina")
            action = input("What would you like to do? \n -Fight--Magic--Bag--Action- \n")
            if action == "Fight":
                fight_action = input("-Light- or -Heavy- attack? \n")
                if fight_action == "Light":
                    if staminaless_counter > 0:
                        if user.stamina >= 3:
                            user.stamina -= 3
                            dmg_dealt = (held_weapon.damagestat * light_difference)
                            if strength_counter >= 1:
                                dmg_dealt += 5
                                strength_counter -= 1
                            foe.health_e -= dmg_dealt
                            print("You dealt", dmg_dealt, "damage.")
                    elif user.stamina >= 5:
                        user.stamina -= 5
                        dmg_dealt = (held_weapon.damagestat * light_difference)
                        if strength_counter >= 1:
                            dmg_dealt += 5
                            strength_counter -= 1
                        foe.health_e -= dmg_dealt
                        print("You dealt", dmg_dealt, "damage.")
                    else:
                        print("Not enough stamina.")
                elif fight_action == "Heavy":
                    if staminaless_counter > 0:
                        if user.stamina >= 5:
                            user.stamina -= 5
                            dmg_dealt = (held_weapon.damagestat * heavy_difference)
                            if strength_counter >= 1:
                                dmg_dealt += 5
                                strength_counter -= 1
                            foe.health_e -= dmg_dealt
                            print("You dealt", dmg_dealt, "damage.")
                    elif user.stamina >= 8:
                        user.stamina -= 8
                        dmg_dealt = (held_weapon.damagestat * heavy_difference)
                        if strength_counter >= 1:
                            dmg_dealt += 5
                            strength_counter -= 1
                        foe.health_e -= dmg_dealt
                        print("You dealt", dmg_dealt, "damage.")
                    else:
                        print("Not enough stamina")
            elif action == "Magic":
                print("What spell would you like to cast? \n Known spells:", show_spells(user))
                cast_spell = input()
                try:
                    if known_spells.index(cast_spell) >= 0:
                        if cast_spell == "Regenerate":
                            regen_counter = spells.regenerate(regen_counter)
                        elif cast_spell == "Lightning":
                            spells.lightning(foe, empowered)
                        elif cast_spell == "Elemental volley":
                            spells.elemental_volley(foe, empowered)
                        elif cast_spell == "Stasis":
                            stasis_counter = spells.stasis(stasis_counter)
                        user.stamina += 4
                        if user.stamina > user.max_stamina:
                            user.stamina = user.max_stamina
                        empowered = False
                        if cast_spell == "Empower":
                            empowered = spells.empower()
                except ValueError:
                    print("Unknown spell")
            elif action == "Bag":
                print("What item would you like to use? \n Items:", inventory_data.check(user))
                used_item = input()
                if used_item == "Strength potion":
                    strength_counter = inventory_data.use(user, strength_counter, used_item, 0, False,
                                                          staminaless_counter)
                elif used_item == "Resistance potion":
                    resistance_counter = inventory_data.use(user, 0, used_item, resistance_counter, False,
                                                            staminaless_counter)
                elif used_item == "Shield potion":
                    shield = inventory_data.use(user, 0, used_item, 0, shield, staminaless_counter)
                elif used_item == "Staminaless potion":
                    staminaless_counter = inventory_data.use(user, 0, used_item, 0, False, staminaless_counter)
                else:
                    inventory_data.use(user, 0, used_item, 0, False, staminaless_counter)
                if user.stamina > user.max_stamina:
                    user.stamina = user.max_stamina
            elif action == "Action":
                print("Under development...")
                user.stamina += 10
            turn = False
        if turn is False:
            if foe.health_e >= 1:
                if stasis_counter == 0:
                    if resistance_counter == 0:
                        dice = random.randint((foe.damagestat//2), foe.damagestat)
                    else:
                        dice = random.randint((foe.damagestat // 2), foe.damagestat) // 1.8
                        resistance_counter -= 1
                    if shield > 0:
                        shield -= 1
                        print("The shield potion protected you from getting hurt.")
                        if shield == 0:
                            print("The shield has been broken.")
                    else:
                        user.health -= dice
                        print("Foe dealt", dice, "damage.")
                else:
                    stasis_counter -= 1
                    print("The foe is unable to move!")
            turn = True
        if user.health <= 0:
            print("YOU HAVE BEEN DEFEATED BY", foe.battle_name)
        if foe.health_e <= 0:
            print("YOU HAVE DEFEATED", foe.battle_name)
    foe.health_e = foe.maxhealth_e


# Test weapon equipping
'''
equippedweapon = weapon_check()
print(equippedweapon.equipped, equippedweapon.damagestat)
pickup(weapon_Hammer)
equippedweapon = weapon_check()
print(equippedweapon.equipped, equippedweapon.damagestat)
pickup(weapon_DDaggers)
equippedweapon = weapon_check()
print(equippedweapon.equipped, equippedweapon.damagestat)
'''

# Test battle system
'''
pickup(weapon_SSword)

learn_spell(0, "Empower")
learn_spell(1, "Regenerate")
learn_spell(2, "Lightning")
learn_spell(3, "Elemental volley")
learn_spell(4, "Stasis")
battle(enemy_Sheep, Player1)
'''

# test inventory system
'''
inventory_data.pickup_item("Health potion", Player1)
inventory_data.pickup_item("Large health potion", Player1)
inventory_data.pickup_item("Stamina potion", Player1)
inventory_data.pickup_item("Vitality potion", Player1)
inventory_data.pickup_item("Staminaless potion", Player1)

print(inventory_data.check(Player1))
inventory_data.health_potion(Player1)
print(inventory_data.check(Player1))
'''

# test items and spells in battle system
pickup(weapon_Sword)

learn_spell(0, "Empower")
learn_spell(1, "Regenerate")
learn_spell(2, "Lightning")
learn_spell(3, "Elemental volley")
learn_spell(4, "Stasis")

inventory_data.pickup_item("Health potion", Player1)
inventory_data.pickup_item("Large health potion", Player1)
inventory_data.pickup_item("Vitality potion", Player1)
inventory_data.pickup_item("Stamina potion", Player1)
inventory_data.pickup_item("Large stamina potion", Player1)
inventory_data.pickup_item("Staminaless potion", Player1)
inventory_data.pickup_item("Resistance potion", Player1)
inventory_data.pickup_item("Shield potion", Player1)

battle(enemy_Orc, Player1)
battle(enemy_Orc, Player1)
