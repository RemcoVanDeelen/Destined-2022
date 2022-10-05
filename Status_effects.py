class Effect:
    def __init__(self, time, effect, duration):
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

    def foresight_effect(self, data):                   # FILLER function.
        self.duration -= 1

    def opponent_foresight_effect(self, data):          # FILLER function.
        self.duration -= 1

    def enchanted_weapon(self, data):
        self.duration -= 1
        return 4                                        # FILLER damage.

    def enchanted_weapon_empowered(self, data):
        self.duration -= 1
        return 8                                        # FILLER damage.

    def barrier_effect(self, data):                 # FILLER function.
        self.duration -= 1

    def opponent_barrier_effect(self, data):                 # FILLER function.
        self.duration -= 1

    def opponent_barrier_effect_empowered(self, data):          # FILLER function.
        self.duration -= 1

    def weakened(self, data):
        self.duration -= 1

    def burning(self, data):
        data[2].health -= 4                         # FILLER damage (should be %).
        self.duration -= 1

    def venom(self, data):
        data[2].health -= 4                         # FILLER damage.
        self.duration -= 1

    def venom_empowered(self, data):
        data[2].health -= 6                         # FILLER damage.
        self.duration -= 1

    def stasis_effect(self, data):
        self.duration -= 1


'''
empowered = Effect(0, "empowered", True)

regenerating = Effect("start", "regenerating", 3)
regenerating_empowered = Effect("start", "regenerating_empowered", 3)

foresight_effect = Effect("?", "foresight_effect", 4)          # FILLER function < and v both.
opponent_foresight_effect = Effect("?", "opponent_foresight_effect", 4)

enchanted_weapon = Effect("attacking", "enchanted_weapon", True)
enchanted_weapon_empowered = Effect("attacking", "enchanted_weapon_empowered", True)

barrier_effect = Effect("?", "barrier_effect", 4)
opponent_barrier_effect = Effect("?", "opponent_barrier_effect", 4)
opponent_barrier_effect_empowered = Effect("?", "opponent_barrier_effect_empowered", 4)

weakened = Effect("end", "weakened", 4)

burning = Effect("end", "burning", 3)

venom_effect = Effect("end", "venom", 3)
venom_effect_empowered = Effect("always", "venom_empowered", 3)

stasis_effect = Effect(0, "stasis_effect", 2)
'''  # Effect examples
