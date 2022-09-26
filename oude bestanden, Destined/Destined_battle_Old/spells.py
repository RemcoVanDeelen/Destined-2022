import random


def regenerate(regen_counter):
    regen_counter += 3
    return regen_counter


def empower():
    empowered = True
    print("The elements have been aligned.")
    return empowered


def lightning(foe, empowered):
    if empowered is True:
        damage = foe.maxhealth_e / 4 * 1.4 + 4
        foe.health_e -= damage
    else:
        damage = foe.maxhealth_e/4 + 4
        foe.health_e -= damage
    print("You dealt", damage, "damage.")


def elemental_volley(foe, empowered):
    shard1 = random.randint(1, 2)
    shard2 = random.randint(1, 2)
    shard3 = random.randint(1, 2)
    if shard1 == 1:
        damage = foe.maxhealth_e / 8 + 3
    else:
        damage = foe.maxhealth_e / 10 + 2.5
    if shard2 == 1:
        damage2 = foe.maxhealth_e / 8 + 3
    else:
        damage2 = foe.maxhealth_e / 10 + 2.5
    if shard3 == 1:
        damage3 = foe.maxhealth_e / 8 + 3
    else:
        damage3 = foe.maxhealth_e / 10 + 2.5
    if empowered is True:
        shard4 = random.randint(1, 2)
        if shard4 == 1:
            damage4 = foe.maxhealth_e / 8 + 3
        else:
            damage4 = foe.maxhealth_e / 10 + 2.5
        print("You dealt", damage, ",", damage2, ",", damage3, "and", damage4, "damage.")
        total_damage = damage + damage2 + damage3 + damage4
    else:
        print("You dealt", damage, ",", damage2, "and", damage3, "damage.")
        total_damage = damage + damage2 + damage3
    foe.health_e -= total_damage


# def straw_in_the_wind():


def stasis(stasis_counter):
    stasis_counter += 2
    print("The foe has been put in stasis!")
    return stasis_counter


'''
def agility():


def weaken():


def fireball():


# def stamina():


def whirlwind():


def enchant_weapon():


def recover():


def venom():


def focus():


def calm():


# def heal():


# def barrier():


def chaotic_strike():


def siphon():


# def time_slow_bubble():
'''