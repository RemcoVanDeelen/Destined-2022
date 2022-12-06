"""
Enemy_class.py
--

This file holds all data regarding Enemies (Foes).
An enemy is defined by a Foe object holding an Ai function and multiple Move objects.
Each of these are defined and created within this file.

"""

from random import randint
from tkinter import PhotoImage
from Status_effects import *
from Battle import deal_damage, os


class Foe:
    def __init__(self,
                 speed: int = 10,
                 max_health: int = 20,
                 soul: int = 5,
                 moves: list = [],
                 name=":FOE_NAME:",
                 display: PhotoImage = None,
                 turn_ai=None,
                 description: str = ":FOE_DESCRIPTION:",
                 gold: tuple[int, int] = (0, 4)):
        """
        Class for holding all data for enemies.\n
        An enemy (Foe) can be fought against during battle.

        This class holds the simple stats for:
         * speed,
         * health, max_health, base_max_health,
         * soul,
         * gold drop range,
         - Status effects.

        It also holds the data for displays:
         * Display image,
         * Name,
         * Description.

        Lastly it holds function data on how it decides its actions:
         * Ai function,
         * Action (move) list,
         - Met requirements, prior turn.

        This class itself does not hold functions, instead all used functions are given as parameters.
        """
        # Stats
        self.speed = speed  # Speed stat for turn order (within range 2~28),
        self.health = max_health  # Current health,
        self.base_max_health = max_health  # base Maximum health (max_health resets to this after battles),
        self.max_health = max_health  # Current maximum health,
        self.soul = soul  # Soul received by player on kill,
        self.gold = gold  # range for Gold dropped on victory.
        self.moves = moves  # List of Move objects,
        self.name = name  # Name string,
        self.status = []  # Current status effects (see Status_effects.py),
        self.display = display  # Image used in combat.

        self.turn = turn_ai  # Turn function for deciding moves in combat,
        self.met_requirements = []  # List for met requirements, used when deciding turns.
        self.turn_prior = "passed"  # string tag of previous turn, used when deciding turns.
        self.description = description  # Descriptions string, displayed in info card on display click in combat.


class Move:
    def __init__(self,
                 _name: str,
                 chance: int,
                 effect_multiplier: float | int,
                 function,
                 sequence: dict = {"suppressors": [], "requirements": []}):
        """
        Class for foe action data sets.\n
        Foes use moves for their turns in combat.
        These moves are functions defined below the Ai definition.

        A Move object holds all data which the Ai function uses to decide what move to choose
        and all data for a move's strength (effect_multiplier) and effect (function).

        For more info on the other variables stored in this object, see the basic Ai function:
        'turn_ai_basic'.
        """
        self.name = _name
        self.chance = chance
        self.effect_multiplier = effect_multiplier
        self.function = function
        self.sequence = sequence


# Ai turn functions
def turn_ai_basic(data):
    """
    Basic Ai function.

    This function is used by all foes in the Demo and the example function for possible expansions later.

    --
    The Ai system is implemented in a way where different foes could use different Ai functions.
    This way more variety can be implemented to a large range of enemies.

    For the Demo version only 5 unique foes are made, and it was not necessary to add another Ai function.
    --

    This function decides what move to use based on:
     * Weight (chance),
     * Suppressors,
     * Requirements,

    For each move in the foes move list:

        It checks for values in the 'suppressors' list from the 'sequence' dictionary.
        Suppressors can be either an if statement within a string (case 1)
        or a value to be found in the foes 'met_requirements' list (case 2).
        If a suppressor is met (case 1) or found (case 2) the move is skipped
        and the system continues with the next move.

        Otherwise, the system checks for values in the 'requirements' list from the 'sequence' dictionary.
        Requirements are treated the same way as suppressors and can be both case 1 and case 2 again.
        Except the result is the opposite:
        if a requirement is NOT met (case 1) or NOT found (case 2) the move is skipped
        and the system continues with the next move.

        If no suppressors where met or found and all requirements are met and found,
        the moves is added to a list of possible moves.
        It is added to this list 'move.chance' times. Meaning move objects can have varying weights.

    After going through each move, a random move is picked from the list of possible moves
    and its function is called.
    If there are no moves in the list of possible moves the turn is passed.

    finally the moves name string is set as the foes turn_prior variable.
    """

    percent = []  # list of possible moves.
    for move in data[2].moves:

        # suppressor check:
        suppressed = False
        for suppressor in move.sequence["suppressors"]:
            # case 1:
            try:
                check = eval(suppressor)
            except (SyntaxError, NameError):
                check = False

            # case 2 and suppression stage 1:
            if suppressor in data[2].met_requirements or check:
                print("suppressor met, ", end="")
                suppressed = True
                break

        # requirement check:
        for requirement in move.sequence["requirements"]:

            # case 1:
            try:
                check = eval(requirement)
            except (SyntaxError, NameError):
                check = False

            # case 2 and suppression stage 1:
            if requirement not in data[2].met_requirements and not check:
                print("requirements not met,", end=" ")
                suppressed = True

        # suppression stage 2:
        if suppressed:
            print("suppressed:", move.name)
            continue

        # addition to list of possible moves:
        for _ in range(0, move.chance):
            percent.append(move)

    # move decision:
    if not percent:
        # in case of empty possible move list:
        print("mandatory pass due to no available turns: ", end="#")
        en_act_pass(data, en_act_pass)
        data[2].turn_prior = "passed"
    else:
        # choice of turn:
        rng = randint(0, len(percent)) - 1
        percent[rng].function(data, percent[rng])
        data[2].turn_prior = percent[rng].name


# Enemy action (en_act) functions:
def en_act_pass(data, _):
    """Function for passing turns, used when no other moves are possible."""
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
    print(f"{data[2].name} defends.")


def en_act_self_heal(data, move):
    """Function for healing some health of self, used by Field Foes."""
    print(f"{data[2].name} healed itself, {data[2].health} -> ", end="")
    data[2].health += round(8*move.effect_multiplier)
    if data[2].health > data[2].max_health:
        data[2].health = data[2].max_health
    print(data[2].health, "hp.")


def en_act_buff_health(data, move):
    """Function for increasing an allies max health, used by Field Foes."""
    target = data[1][randint(0, len(data[1])-1)]
    if target in [field_foe_support, field_foe_support2]:
        target = data[1][randint(0, len(data[1]) - 1)]
    pre_max, pre_current = target.max_health, target.health
    target.max_health += 10*move.effect_multiplier
    target.health += 5*move.effect_multiplier
    print(f"{data[2].name} increased {target.name} max health and healed it, "
          f"{pre_current}/{pre_max} -> {target.health}/{target.max_health} hp.")
    data[2].met_requirements.append("Buffed ally health")


def en_act_buff_damage(data, move):
    """Function for granting any ally the enchanted weapon effect, used by Field Foes."""
    target = data[1][randint(0, len(data[1])-1)]
    if target in [field_foe_support, field_foe_support2]:
        target = data[1][randint(0, len(data[1]) - 1)]
    for effect in target.status:
        if effect.effect == "opponent_enchanted_weapon":
            effect.duration += round(3*move.effect_multiplier)
            print(f"{data[2].name} extended {target.name} enchanted weapon.")
            break
    else:
        target.status.append(Effect("end", "opponent_enchanted_weapon", round(3*move.effect_multiplier)))
        print(f"{data[2].name} enchanted {target.name} weapon.")


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
        print(f"{data[2].name} attempted to heal any ally but then:")
        data[2].turn(data)


# - Enemy objects:
# Dummy:
dummy_img = PhotoImage(file="images/Battle_GUI/Enemies/Dummy_foe.png".replace("/", os.sep)).zoom(5, 5).subsample(2, 2)

dummy_heal = Move("Heal", 100, 1, en_act_heal, sequence={"suppressors": [], "requirements": ["data[2].health<10"]})

Dummy = Foe(5, 50, 1, [dummy_heal], "Training dummy", dummy_img, turn_ai_basic,
            "A harmless but sturdy foe. \n"
            "Many knights in training run from\n"
            "it on their first try.", (0, 0))
# This foe always passes unless their health < 10, then they heal to full health (50).

# Field enemies:
ff_offence_img = PhotoImage(file="images/Battle_GUI/Enemies/ff_offence.png".
                            replace("/", os.sep)).zoom(5, 5).subsample(2, 2)

ff_heavy_atk = Move("heavy atk", 3, 1, en_act_heavy_atk,
                    {"suppressors": ["data[2].turn_prior=='heavy atk'", "data[2].turn_prior=='double atk'"],
                     "requirements": []})
ff_light_atk = Move("light atk", 2, 1.25, en_act_light_atk)
ff_double_atk = Move("double atk", 3, 1, en_act_double_atk, {
    "suppressors": ["data[2].turn_prior=='heavy atk'", "data[2].turn_prior=='double atk'"],
    "requirements": []})

ff_offence_desc = "This speedy foe spends its turns\n" \
                  "performing heavy attacks,\n" \
                  "sometimes even twice in one turn."

field_foe_offence = Foe(12, 20, 3, [ff_light_atk, ff_heavy_atk, ff_double_atk],
                        "Offencive enemy A", ff_offence_img, turn_ai_basic, ff_offence_desc, (1, 4))
field_foe_offence2 = Foe(12, 20, 3, [ff_light_atk, ff_heavy_atk, ff_double_atk],
                         "Offencive enemy B", ff_offence_img, turn_ai_basic, ff_offence_desc, (1, 4))
# This foe is attack oriented, has medium health, is slightly faster than average and 3 on death.
# It chooses between a Heavy attack, a Light one and a small double hit. Following basic turn Ai.

ff_defence_img = PhotoImage(file="images/Battle_GUI/Enemies/ff_defence.png".
                            replace("/", os.sep)).zoom(5, 5).subsample(2, 2)

ff_defend = Move("defend", 2, 0, en_act_defend, {"suppressors": ["data[2].turn_prior=='defend'"], "requirements": []})
ff_self_heal = Move("self heal", 1, 0.6, en_act_self_heal,
                    {"suppressors": ["data[2].turn_prior=='defend"],
                     "requirements": ["data[2].health<data[2].max_health-5"]})

ff_defence_desc = "This foe can take many punches.\n" \
                  "Sometimes it spends a turn\n" \
                  "healing itself."

field_foe_defence = Foe(5, 35, 3, [ff_defend, ff_self_heal, ff_light_atk],
                        "Defencive enemy A", ff_defence_img, turn_ai_basic, ff_defence_desc, (0, 5))

field_foe_defence2 = Foe(5, 35, 3, [ff_defend, ff_self_heal, ff_light_atk],
                         "Defencive enemy B", ff_defence_img, turn_ai_basic, ff_defence_desc, (0, 5))
# This foe is defence oriented, has quite a bit of health, is very slow, and leaves 3 on death.
# It chooses between defending, a small self-heal and a light attack. Following basic turn Ai.

ff_support_img = PhotoImage(file="images/Battle_GUI/Enemies/ff_support.png".
                            replace("/", os.sep)).zoom(5, 5).subsample(2, 2)

ff_buff_health = Move("ally health buff", 9, 1, en_act_buff_health,
                      {"requirements": [], "suppressors": ["Buffed ally health"]})
ff_any_heal = Move("any heal", 4, 1, en_act_heal_any)
ff_enchant_weapon = Move("enchant weapon", 3, 1, en_act_buff_damage)
ff_light_atk_sup = Move("light atk", 4, 1, en_act_light_atk)

ff_support_desc = "This foe seems very fragile, but\n" \
                  "it can form quite the threat by\n" \
                  "supporting its allies."

field_foe_support = Foe(15, 18, 4, [ff_buff_health, ff_any_heal, ff_light_atk_sup, ff_enchant_weapon],
                        "Supporting enemy A", ff_support_img, turn_ai_basic, ff_support_desc, (0, 3))
field_foe_support2 = Foe(15, 18, 4, [ff_buff_health, ff_any_heal, ff_light_atk_sup, ff_enchant_weapon],
                         "Supporting enemy B", ff_support_img, turn_ai_basic, ff_support_desc, (0, 3))
# This foe is oriented around supporting allies, has medium-little health, is quite fast and leaves 4 soul on death.
# It chooses between a max_health buff to an ally, a damage buff to an ally, a heal-any move, and a light atk.

ff_power_img = PhotoImage(file="images/Battle_GUI/Enemies/ff_power.png".
                          replace("/", os.sep)).zoom(5, 5).subsample(2, 2)

ff_heavy_atk_power = Move("heavy atk", 3, 1.5, en_act_heavy_atk,
                          {"suppressors": ["data[2].turn_prior=='double atk'"], "requirements": []})
ff_double_atk_power = Move("double atk", 3, 1.5, en_act_double_atk,
                           {"suppressors": ["data[2].turn_prior=='double atk'"], "requirements": []})
ff_self_heal_power = Move("self heal", 1, 1, en_act_self_heal,
                          {"suppressors": ["data[2].turn_prior=='self heal'"],
                           "requirements": ["data[2].health<data[2].max_health-5"]})

field_foe_powerful = Foe(10, 45, 6, [ff_heavy_atk_power, ff_double_atk_power, ff_self_heal_power, ff_defend],
                         "Powerful enemy", ff_power_img, turn_ai_basic, "A Very powerful foe.\n"
                                                                        "It is advised to flee if it is not alone.\n"
                                                                        "Even if it is, proceed with caution.", (4, 10))
# This foe is all-round stronger than the others. Having a lot of health, medium speed and leaving 6 soul on death.
# It chooses between a heavy attack, a double attack, a self-heal and defending.
