from random import randint
from tkinter import PhotoImage
from Status_effects import *
from Battle import deal_damage, os


class Foe:
    def __init__(self, speed=10, max_health=20, soul=5, moves: list = [None], name=":undefined_foe_name:", display: PhotoImage = None, turn_ai=None):
        """Class for enemies.\n
        Holds the stats and turn actions of an enemy,\n
        -- Multiple objects should be made per foe if multiple can be encountered in one battle."""
        # Stats
        self.speed = speed  # Speed stat for turn order,
        self.health = max_health  # Current health,
        self.base_max_health = max_health
        self.max_health = max_health  # Maximum health,
        self.soul = soul  # Soul received on kill,
        self.moves = moves  # List of moves,
        self.name = name  # Name,
        self.status = []  # Current status effects,
        self.display = display  # Image used in combat.

        self.turn = turn_ai  # Turn function for combat,
        self.met_requirements = []  # Empty list for met requirements when deciding turns.
        self.turn_prior = "passed"


class Move:
    def __init__(self, _name, chance, effect_multiplier, function, sequence={"suppressors": [], "requirements": []}):
        """Class for foe actions.\n
        Holds stats for turn action and turn_ai.\n
        Names are used in interpreter tracing and turn_prior sequences.

        A sequence is required for scripted turns.\n
        This defines what cancels a move and what doesn't."""
        self.name = _name
        self.chance = chance
        self.effect_multiplier = effect_multiplier
        self.function = function
        self.sequence = sequence


# Ai turn functions
def turn_ai_basic(data):
    percent = []
    for move in data[2].moves:
        suppressed = False
        for suppressor in move.sequence["suppressors"]:

            try:
                check = eval(suppressor)
            except (SyntaxError, NameError):
                check = False

            if suppressor in data[2].met_requirements or check:
                print("suppressor met, ", end="")
                suppressed = True
                break

        for requirement in move.sequence["requirements"]:

            try:
                check = eval(requirement)
            except (SyntaxError, NameError):
                check = False

            if requirement not in data[2].met_requirements and not check:
                print("requirements not met,", end=" ")
                suppressed = True

        if suppressed:
            print("suppressed:", move.name)
            continue

        for _ in range(0, move.chance):
            percent.append(move)

    if not percent:
        print("mandatory pass due to no available turns: ", end="#")
        en_act_pass(data, en_act_pass)
        data[2].turn_prior = "passed"
    else:
        rng = randint(0, len(percent)) - 1
        percent[rng].function(data, percent[rng])
        data[2].turn_prior = percent[rng].name


# Enemy actions
def en_act_pass(data, _):
    """Function for passing turns, used by Training Dummy."""

    print(data[2].name, "passed")


def en_act_heal(data, _):
    """Function for healing to max health, used by Training Dummy."""
    print(data[2].name, f"healed self to full, {data[2].health} -> {data[2].max_health} hp")
    data[2].health = data[2].max_health


def en_act_heavy_atk(data, move):
    """Function for heavy damage attack, used by Field Foes."""
    deal_damage(data[2], data[0][0], False, 6*move.effect_multiplier)


def en_act_light_atk(data, move):
    """Function for light damage attack, used by Field Foes."""
    deal_damage(data[2], data[0][0], False, 4*move.effect_multiplier)


def en_act_double_atk(data, move):
    """Function for double light damage attack, used by Field Foes."""
    deal_damage(data[2], data[0][0], False, 4*move.effect_multiplier)
    deal_damage(data[2], data[0][0], False, 4*move.effect_multiplier)


def en_act_defend(data, _):
    """Function for defending, used by Field Foes."""
    data[2].status.append(Effect("start", "defending", 1))
    print(f"{data[2].name} defends")


def en_act_self_heal(data, move):
    """Function for healing some health of self, used by Field Foes."""
    print(f"{data[2].name} healed itself, {data[2].health} -> ", end="")
    data[2].health += 8*move.effect_multiplier
    if data[2].health > data[2].max_health:
        data[2].health = data[2].max_health
    print(data[2].health, "hp")


def en_act_buff_health(data, move):
    """Function for increasing an allies max health, used by Field Foes."""
    target = data[1][randint(0, len(data[1])-1)]
    if target == data[2]:
        target = data[1][randint(0, len(data[1]) - 1)]
    pre_max, pre_current = target.max_health, target.health
    target.max_health += 10*move.effect_multiplier
    target.health += 5*move.effect_multiplier
    print(f"{data[2].name} increased {target.name} max health and healed it, "
          f"{pre_current}/{pre_max} -> {target.health}/{target.max_health} hp.")
    data[2].met_requirements.append("Buffed ally health")


def get_current_health_percent(foe):
    """Internal function used in en_act_heal_ally."""
    return foe.health/foe.max_health


def en_act_heal_any(data, move):
    """Function for healing some health of any ally including self, used by Field Foes."""
    target_list = data[1].copy()
    target_list.sort(key=get_current_health_percent)
    for target in target_list:
        if target.health < target.max_health:
            print(f"{data[2].name} healed {target.name}. {target.health}", end="")
            target.health += 10*move.effect_multiplier
            if target.health > target.max_health:
                target.health = target.max_health
            print(f" -> {target.health} hp.")
            break
    else:
        print(f"{data[2].name} attempted to heal any ally but passed instead.")


# - Enemy objects:
# Dummy:
dummy_img = PhotoImage(file="images/Battle_GUI/Enemies/Dummy_foe.png".replace("/", os.sep)).zoom(5, 5).subsample(2, 2)

dummy_pass = Move("Pass", 100, 1, en_act_pass, sequence={"suppressors": ["data[2].health<10"], "requirements": []})
dummy_heal = Move("Heal", 100, 1, en_act_heal, sequence={"suppressors": [], "requirements": ["data[2].health<10"]})

Dummy = Foe(5, 50, 1, [dummy_pass, dummy_heal], "Training dummy", dummy_img, turn_ai_basic)                      # FOE
# This foe always passes unless their health < 10, then they heal to full health (50).

# Field enemies:
foe_test_img = PhotoImage(file="images/Battle_GUI/Enemies/FoeTest.png".replace("/", os.sep)).zoom(5, 5).subsample(2, 2)

ff_heavy_atk = Move("heavy atk", 3, 1, en_act_heavy_atk,
                    {"suppressors": ["data[2].turn_prior=='heavy atk'", "data[2].turn_prior=='double atk'"],
                     "requirements": []})
ff_light_atk = Move("light atk", 2, 1, en_act_light_atk)
ff_double_atk = Move("double atk", 3, 1, en_act_double_atk, {
    "suppressors": ["data[2].turn_prior=='heavy atk'", "data[2].turn_prior=='double atk'"],
    "requirements": []})

field_foe_offence = Foe(12, 20, 3, [ff_light_atk, ff_heavy_atk, ff_double_atk],
                        "Offencive enemy A", foe_test_img, turn_ai_basic)                                        # FOE
field_foe_offence2 = Foe(12, 20, 3, [ff_light_atk, ff_heavy_atk, ff_double_atk],
                         "Offencive enemy B", foe_test_img, turn_ai_basic)                                       # FOE
# This foe is attack oriented, has medium health, is slightly faster than average and 3 on death.
# It chooses between a Heavy attack, a Light one and a small double hit. Following basic turn Ai.

ff_defend = Move("defend", 2, 0, en_act_defend, {"suppressors": ["data[2].turn_prior=='defend'"], "requirements": []})
ff_self_heal = Move("self heal", 1, 0.6, en_act_self_heal,
                    {"suppressors": ["data[2].turn_prior=='defend"],
                     "requirements": ["data[2].health<data[2].max_health-5"]})

field_foe_defence = Foe(5, 35, 3, [ff_defend, ff_self_heal, ff_light_atk],
                        "Defencive enemy A", foe_test_img, turn_ai_basic)                                        # FOE

field_foe_defence2 = Foe(5, 35, 3, [ff_defend, ff_self_heal, ff_light_atk],
                         "Defencive enemy B", foe_test_img, turn_ai_basic)                                       # FOE
# This foe is defence oriented, has quite a bit of health, is very slow, and leaves 3 on death.
# It chooses between defending, a small self-heal and a light attack. Following basic turn Ai.

ff_buff_health = Move("ally health buff", 9, 1, en_act_buff_health,
                      {"requirements": [], "suppressors": ["Buffed ally health"]})
ff_any_heal = Move("any heal", 4, 1, en_act_heal_any)

field_foe_support = Foe(15, 18, 4, [ff_buff_health, ff_any_heal, ff_light_atk],
                        "Supporting enemy A", foe_test_img, turn_ai_basic)                                       # FOE
field_foe_support2 = Foe(15, 18, 4, [ff_buff_health, ff_any_heal, ff_light_atk],
                         "Supporting enemy B", foe_test_img, turn_ai_basic)                                      # FOE
# This foe is oriented around supporting allies, has medium-little health, is quite fast and leaves 4 soul on death.
# It chooses between a max_health buff to an ally, an heal-any move, and a light atk.

ff_heavy_atk_power = Move("double atk", 3, 1.5, en_act_heavy_atk,
                          {"suppressors": ["data[2].turn_prior=='double atk'"], "requirements": []})
ff_double_atk_power = Move("double atk", 3, 1.5, en_act_double_atk,
                           {"suppressors": ["data[2].turn_prior=='double atk'"], "requirements": []})
ff_self_heal_power = Move("self heal", 1, 1, en_act_self_heal,
                          {"suppressors": ["data[2].turn_prior=='self heal'"],
                           "requirements": ["data[2].health<data[2].max_health-5"]})

field_foe_powerful = Foe(10, 45, 6, [ff_heavy_atk_power, ff_double_atk_power, ff_self_heal_power, ff_defend],
                         "Powerful enemy", foe_test_img, turn_ai_basic)                                          # FOE
# This foe is all-round stronger than the others. Having a lot of health, medium speed and leaving 6 soul on death.
# It chooses between a heavy attack, a double attack, a self-heal and defending.
