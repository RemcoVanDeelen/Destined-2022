from player_related import *
from enemies import *

# battle effects


class EffectCounter:

    def __init__(self, counter, name):
        self.counter = counter
        self.name = name

    def count(self, user):
        if self.counter > 0:
            if self.name == "Regen":
                user.health += user.max_health//15
                self.counter -= 1
                if self.counter == 0:
                    print("The regeneration has stopped.")
            elif self.name == "Strength":
                return 1.5
            elif self.name == "Resistance":
                return 1.3
            elif self.name == "Stasis":
                print("The enemy was unable to move.")
        else:
            return 1


# battle simulation

def battle(foe, user, foe2=none, foe3=none):

    # effects
    regen = EffectCounter(0, "Regen")
    staminaless = EffectCounter(0, "Staminaless")
    stasis = EffectCounter(0, "Stasis")
    strength = EffectCounter(0, "Strength")
    resistance = EffectCounter(0, "Resistance")
    shield = EffectCounter(0, "Shield")
    empowered = False

    # turn decider

    if foe2 is none and foe3 is none:
        turn_order = [user, foe]
        turn_order.sort(key=lambda x: x.speed, reverse=True)
    elif foe3 is none:
        turn_order = [user, foe, foe2]
        turn_order.sort(key=lambda x: x.speed, reverse=True)
    else:
        turn_order = [user, foe, foe2, foe3]
        turn_order.sort(key=lambda x: x.speed, reverse=True)
    t_num = 0

    # simulation
    enemies_alive = foe.health + foe2.health + foe3.health

    while user.health > 0 and enemies_alive > 0:
        if t_num >= len(turn_order):
            t_num = 0
        turn = turn_order[t_num]

        target = none

        if turn is user:

            if user.stamina >= user.max_stamina:
                user.stamina = user.max_stamina

            # effect check
            regen.count(user)
            staminaless.count(user)
            if strength.counter != 0:
                strength.counter -= 1
                if strength.counter == 0:
                    print("Your strength returns to  normal.")
            if resistance.counter != 0:
                resistance.counter -= 1

            # potion cooldowns
            cooldown_num = user.bag_slots
            checked_items = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
            while cooldown_num >= 1:
                cooldown_num -= 1
                item = user.bag[cooldown_num]
                repeat = False
                try:
                    if checked_items.index(item.name) >= 0:
                        repeat = True
                except ValueError:
                    if repeat is False:
                        checked_items[cooldown_num] = item.name
                        if item.counter >= 1:
                            item.counter -= 1

            # actions
            print("You currently have", user.health, "health and", user.stamina, "stamina.")
            action = input("What would you like to do? \n -Fight--Magic--Bag--Action- \n")

            # Fight
            if action == "Fight":
                action = input("-Light- or -Heavy- attack? \n")

                # target system
                if foe3 is none and foe2 != none:
                    print("What enemy do you target? \n", foe.name, "{" + str(foe.health) + "}", "or", foe2.name, "{" +
                          str(foe2.health) + "}" + "?")
                    target = input()
                elif foe3 != none:
                    print("What enemy do you target? \n", foe.name, "{" + str(foe.health) + "}", ",", foe2.name, "{"
                          + str(foe2.health) + "}", "or", foe3.name, "{" + str(foe3.health) + "}" + "?")
                    target = input()
                if target == "foe2":
                    target = foe2
                elif target == "foe3":
                    target = foe3
                else:
                    if foe.health > 0:
                        target = foe
                    elif foe2.health > 0:
                        target = foe2
                    else:
                        target = foe3

                if action == "Light":

                    # Light
                    if staminaless.counter > 0:
                        if user.stamina >= user.weapon.light_cost + 2:
                            user.stamina -= user.weapon.light_cost + 2
                            damage = round(user.weapon.damage * 0.8 * strength.count(user))
                            if randint(0, 100) <= user.weapon.crit_chance:
                                damage *= 1.5
                                print("Critical hit!")
                            target.health -= damage
                            print("You dealt", damage, "damage.")
                    elif user.stamina >= user.weapon.light_cost:
                        user.stamina -= user.weapon.light_cost
                        damage = round(user.weapon.damage * 0.8 * strength.count(user))
                        if randint(0, 100) <= user.weapon.crit_chance:
                            damage *= 1.5
                            print("Critical hit!")
                        target.health -= damage
                        print("You dealt", damage, "damage.")
                    else:
                        print("Not enough stamina")
                if action == "Heavy":

                    # Heavy
                    if staminaless.counter > 0:
                        if user.stamina >= user.weapon.heavy_cost + 2:
                            user.stamina -= user.weapon.heavy_cost + 2
                            damage = round(user.weapon.damage * 1.25 * strength.count(user))
                            if randint(0, 100) <= user.weapon.crit_chance:
                                damage *= 1.5
                                print("Critical hit!")
                            target.health -= damage
                            print("You dealt", damage, "damage.")
                    elif user.stamina >= user.weapon.heavy_cost:
                        user.stamina -= user.weapon.heavy_cost
                        damage = round(user.weapon.damage * 1.2 * strength.count(user))
                        if randint(0, 100) <= user.weapon.crit_chance:
                            damage *= 1.5
                            print("Critical hit!")
                        target.health -= damage
                        print("You dealt", damage, "damage.")
                    else:
                        print("Not enough stamina")

            # Magic
            elif action == "Magic":
                print("What spell would you like to cast? \n Known spells:", )
                Regenerate.cast(Regenerate, Player1, empowered, stasis, regen, target=None)

            # Items
            elif action == "Bag":
                print("What item would you like to use? \n Items:", open_bag(user))
                check_item(input(), user, strength, resistance, shield)
                user.stamina += 5

            # Actions
            elif action == "Action":
                print("FILLER")
                # this also needs a copy of the target system
                user.stamina += 5

            if target != none:
                try:
                    if target.health <= 0:
                        print("You have defeated", target.name)
                except UnboundLocalError:
                    print("FILLER")
            t_num += 1

        else:
            if turn.health >= 1:
                if stasis.counter != 0:
                    stasis.count(user)
                else:
                    turn.turn(user, shield, resistance)
            t_num += 1

        if foe.health < 0:
            foe.health = 0
        if foe2.health < 0:
            foe2.health = 0
        if foe3.health < 0:
            foe3.health = 0
        enemies_alive = foe.health + foe2.health + foe3.health

    if user.health <= 0:
        print("YOU HAVE BEEN DEFEATED BY", turn.b_name)
    else:
        print("YOU HAVE DEFEATED ALL ENEMIES")
        user.soul += foe.soul + foe2.soul + foe3.soul
        print("You gained", foe.soul + foe2.soul + foe3.soul, "Soul... \n")
        user.level_up()
    foe.health = foe.max_health
    foe2.health = foe2.max_health
    foe3.health = foe3.max_health

