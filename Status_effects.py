class Effect:
    def __init__(self, time, effect, duration):
        """
        Effect class:

        Used to define any status effect given.

        - time: defines when to trigger
        - effect: defines effect function (included in class)
        - duration: defines how long effect lasts
        """
        self.time = time
        self.tick = getattr(self, effect)
        self.duration = duration
        self.effect = effect

    def empowered(self, data):
        pass

    def regenerating(self, data):
        data[2].health += 5                             # FILLER healing.
        if data[2].health > data[2].max_health:
            data[2].health = data[2].max_health
        self.duration -= 1

    def regenerating_empowered(self, data):
        data[2].health += 8                             # FILLER healing.
        if data[2].health > data[2].max_health:
            data[2].health = data[2].max_health
        self.duration -= 1

    def foresight_effect(self, _):                   # FILLER function.
        self.duration -= 1

    def opponent_foresight_effect(self, _):          # FILLER function.
        self.duration -= 1

    def enchanted_weapon(self, _):
        self.duration -= 1
        return 4                                        # FILLER damage.

    def enchanted_weapon_empowered(self, _):
        self.duration -= 1
        return 8                                        # FILLER damage.

    def barrier_effect(self, _):                 # FILLER function.
        self.duration -= 1

    def opponent_barrier_effect(self, _):                 # FILLER function.
        self.duration -= 1

    def opponent_barrier_effect_empowered(self, _):          # FILLER function.
        self.duration -= 1

    def weakened(self, _):
        self.duration -= 1
        return -0.25

    def burning(self, data):
        data[2].health -= 4                         # FILLER damage (should be %).
        self.duration -= 1

    def venom(self, data):
        data[2].health -= 4                         # FILLER damage.
        self.duration -= 1

    def venom_empowered(self, data):
        data[2].health -= 6                         # FILLER damage.
        self.duration -= 1

    def stasis_effect(self, _):
        self.duration -= 1

    def strength(self, _):                       # FILLER function.
        self.duration -= 1
        return 0.2

    def shielded(self, _):                       # FILLER function.
        self.duration -= 1

    def resistance(self, _):                       # FILLER function.
        self.duration -= 1
        return 0.2

    def staminaless(self, _):                       # FILLER function.
        self.duration -= 1

    def defending(self, _):
        return 0.3


'''
empowered = Effect(0, "empowered", True)

regenerating = Effect("start", "regenerating", 3)
regenerating_empowered = Effect("start", "regenerating_empowered", 3)

foresight_effect = Effect("?", "foresight_effect", 4)          # FILLER function < and v both.
opponent_foresight_effect = Effect("?", "opponent_foresight_effect", 4)

enchanted_weapon = Effect("attacking", "enchanted_weapon", 2)
enchanted_weapon_empowered = Effect("attacking", "enchanted_weapon_empowered", 2)

barrier_effect = Effect("?", "barrier_effect", 4)
opponent_barrier_effect = Effect("?", "opponent_barrier_effect", 4)
opponent_barrier_effect_empowered = Effect("?", "opponent_barrier_effect_empowered", 4)

weakened = Effect("end", "weakened", 4)

burning = Effect("end", "burning", 3)

venom_effect = Effect("end", "venom", 3)
venom_effect_empowered = Effect("always", "venom_empowered", 3)

stasis_effect = Effect(0, "stasis_effect", 2)

Effect("attacking", "strength", 4)

Effect("attacked", "shielded", 3)

Effect("attacked", "resistance", 5)

Effect("end", "staminaless", 5)
'''  # Effect examples
