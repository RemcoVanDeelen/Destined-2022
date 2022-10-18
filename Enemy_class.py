from random import randint
from tkinter import PhotoImage


class AI:
    def __init__(self):
        """AI for Foe class.\n
        Requires definition of .turn function."""
        self.turn = None


class Foe:
    def __init__(self, speed=10, max_health=20, evasion=10, soul=5, moves: list = [None], name=":undefined_foe_name:", display: PhotoImage = None, ai=None):
        """Class for enemies.\n
        For stats and turn actions,\n
        -- 3 Objects should be made per foe."""
        # Stats
        self.speed = speed  # Speed stat for turn order,
        self.health = max_health  # Current health,
        self.max_health = max_health  # Maximum health,
        self.evasion = evasion  # percent chance to avoid being hit,
        self.soul = soul  # Soul received on kill,
        self.moves = moves  # List of moves,
        self.name = name  # Name
        self.status = []  # Current status effects
        self.display = display

        self.ai = ai
        self.turn = self.ai.turn
        self.met_requirements = []


class Move:
    def __init__(self, _type, chance, effect_multiplier, function, sequence={"suppressors": [], "requirements": []}):
        """Class for foe actions.\n
        Types are:

        - Damage,
        - Heal self,
        - Heal ally,
        - Heal any,
        - Pass,

        A sequence is required for scripted turns.\n
        They define when these do what and what comes next."""
        self.type = _type
        self.chance = chance
        self.effect_multiplier = effect_multiplier
        self.function = function
        self.sequence = sequence


def en_act_damage1(data, move):
    """Enemy action dealing 4 base_dmg to the lowest health player."""

    # - Pick target -
    # target is player with the lowest health.
    target = sorted(data[0], key=lambda _: _.health)[0]

    # - Deal damage -
    deal_damage(attacker=data[2], target=target, exact_damage=4*move.effect_multiplier)

    if "attacked" not in  data[2].met_requirements:
        data[2].met_requirements.append("attacked")


def en_act_pass(data, move):
    print(data[2].name, "passed")
    if "attacked" in data[2].met_requirements:
        data[2].met_requirements.remove("attacked")


def en_act_heal(data, move):
    print(data[2].name, "healed self")
    data[2].health = data[2].max_health


def turn_basic(data):
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
            print("suppressed:", move.type, ":", move.function)
            continue

        for _ in range(0, move.chance):
            percent.append(move)

    if not percent:
        print("mandatory pass due to no available turns: ", end="#")
        en_act_pass(data, en_act_pass)
    else:
        rng = randint(0, len(percent)) - 1
        percent[rng].function(data, percent[rng])


AI_basic = AI()
AI_basic.turn = turn_basic

# Example move set: [Move("Pass", 100, 1, en_act_pass, sequence=
#                   {"requirements": ["data[2].health>10"],
#                   "suppressors": ["data[0][0].health<10"]})]

foe_test_img = PhotoImage(file="images/Battle_GUI/FoeTest.png").zoom(5, 5).subsample(2, 2)
dummy_test_img = PhotoImage(file="images/Battle_GUI/Enemies/Dummy_foe.png").zoom(5, 5).subsample(2, 2)

pas = Move("Pass", 100, 1, en_act_pass, sequence={"suppressors": ["data[2].health<10"], "requirements": []})
heal = Move("Heal", 100, 1, en_act_heal, sequence={"suppressors": [], "requirements": ["data[2].health<10"]})
Dummy = Foe(max_health=50, ai=AI_basic, moves=[pas, heal], display=dummy_test_img, name="Training dummy")  # This foe always passes unless their health < 10, then they heal to full health (50).

atk = Move("damage", 80, 1.5, en_act_damage1)
pas = Move("pass", 20, 1, en_act_pass, sequence={"suppressors": [], "requirements": ["attacked"]})
test_foe1 = Foe(5, 25, 0, 5, [atk, pas], ":Test foe 1:", foe_test_img, AI_basic)  # This foe has a 20% chance to pas if the previous turn was an attack.
test_foe2 = Foe(5, 15, 0, 5, [atk, heal], ":Test foe 2:", foe_test_img, AI_basic)  # This foe has a 56% chance to heal to full when damaged.

from Battle import deal_damage
