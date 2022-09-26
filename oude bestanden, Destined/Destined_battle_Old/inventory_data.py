
def pickup_item(item, user):
    if user.inventory_used <= 19:
        user.inventory[user.inventory_used] = item
        user.inventory_used += 1
    else:
        print("Inventory is full.")


def check(user):
    i_list = ""
    counter = user.inventory_used - 1
    while counter >= 0:
        if counter == 0:
            i_list += user.inventory[counter] + "."
        else:
            i_list += user.inventory[counter] + ", "
        counter -= 1
    return i_list


def use(user, strength, used_item, resistance, shield, staminaless_counter):
    try:
        if user.inventory.index(used_item) >= 0:
            if used_item == "Health potion":
                health_potion(user)
            if used_item == "Large health potion":
                large_health_potion(user)
            if used_item == "Stamina potion":
                stamina_potion(user)
            if used_item == "Large stamina potion":
                large_stamina_potion(user)
            if used_item == "Vitality potion":
                vitality_potion(user)
            if used_item == "Strength potion":
                strength = strength_potion(user, strength)
                if staminaless_counter > 0:
                    user.stamina += 8
                else:
                    user.stamina += 6
                return strength
            if used_item == "Resistance potion":
                resistance = resistance_potion(user, resistance)
                if staminaless_counter > 0:
                    user.stamina += 8
                else:
                    user.stamina += 6
                return resistance
            if used_item == "Shield potion":
                shield = shield_potion(user, shield)
                if staminaless_counter > 0:
                    user.stamina += 8
                else:
                    user.stamina += 6
                return shield
            if used_item == "Staminaless potion":
                staminaless_counter = staminaless_potion(user, staminaless_counter)
                user.stamina += 8
                return staminaless_counter
            if used_item == "Item":
                Item_action(user)
            if staminaless_counter > 0:
                user.stamina += 8
            else:
                user.stamina += 6
    except ValueError:
        print("You do not have that item")


def health_potion(user):
    user.health += 30
    if user.health >= user.max_health:
        user.health = user.max_health
    print("Your wounds close instantly.")
    item = user.inventory.index("Health potion")
    user.inventory.pop(item)
    user.inventory_used -= 1
    user.inventory += ""


def large_health_potion(user):
    user.health += 50
    if user.health >= user.max_health:
        user.health = user.max_health
    print("Your wounds close instantly.")
    item = user.inventory.index("Large health potion")
    user.inventory.pop(item)
    user.inventory_used -= 1
    user.inventory += ""


def stamina_potion(user):
    user.stamina += 16
    if user.stamina >= user.max_stamina:
        user.stamina = user.max_stamina
    print("You feel a newfound energy course through your body.")
    item = user.inventory.index("Stamina potion")
    user.inventory.pop(item)
    user.inventory_used -= 1
    user.inventory += ""


def large_stamina_potion(user):
    user.stamina += 35
    if user.stamina >= user.max_stamina:
        user.stamina = user.max_stamina
    print("You feel a newfound energy course through your body.")
    item = user.inventory.index("Large stamina potion")
    user.inventory.pop(item)
    user.inventory_used -= 1
    user.inventory += ""


def vitality_potion(user):
    user.max_health += 5
    item = user.inventory.index("Vitality potion")
    user.inventory.pop(item)
    user.inventory_used -= 1
    user.inventory += ""


def strength_potion(user, strength_counter):
    strength_counter += 4
    print("You feel stronger than before.")
    item = user.inventory.index("Strength potion")
    user.inventory.pop(item)
    user.inventory_used -= 1
    user.inventory += ""
    return strength_counter


def resistance_potion(user, resistance_counter):
    resistance_counter += 5
    print("resistance.txt")
    item = user.inventory.index("Resistance potion")
    user.inventory.pop(item)
    user.inventory_used -= 1
    user.inventory += ""
    return resistance_counter


def shield_potion(user, shield):
    shield += 3
    print("You feel invincible!")
    item = user.inventory.index("Shield potion")
    user.inventory.pop(item)
    user.inventory_used -= 1
    user.inventory += ""
    return shield


def staminaless_potion(user, staminaless_counter):
    staminaless_counter += 5
    print("Your movement feels much easier.")
    item = user.inventory.index("Staminaless potion")
    user.inventory.pop(item)
    user.inventory_used -= 1
    user.inventory += ""
    return staminaless_counter
