"""
Status_effects.py
--

This file holds all status effects in a single class.
Examples of how to use are shown at the bottom of the file.
"""


class Effect:
    def __init__(self, time, effect, duration):
        """
        Effect class:

        Used to define any status effect given for combat.

        * Time: defines when to trigger:
            - "start",
            - "end",
            - "always",
            - 0 (never/unique).
        * Effect: defines effect function (included in class)
        * Duration: defines how long effect lasts
        """
        self.time = time
        self.tick = getattr(self, effect)
        self.duration = duration
        self.effect = effect

    def empowered(self, data):
        """Empowered effect, allows spell casts to trigger additional effects.\n
        * No effect function as all is defined within next spell cast."""
        pass

    def regenerating(self, data):
        """Regenerating effect, regains 5 health of effected."""
        data[2].health += 5
        if data[2].health > data[2].max_health:
            data[2].health = data[2].max_health
        self.duration -= 1

    def regenerating_empowered(self, data):
        """Regenerating effect [empowered], regains 9 health of effected."""
        data[2].health += 9
        if data[2].health > data[2].max_health:
            data[2].health = data[2].max_health
        self.duration -= 1

    def enchanted_weapon(self, _):
        """Enchanted weapon effect, adds 4 post-calculation damage to melee attacks."""
        self.duration -= 1
        return 4

    def enchanted_weapon_empowered(self, _):
        """Enchanted weapon effect [empowered], adds 8 pre-calculation damage to melee attacks."""
        self.duration -= 1
        return 8

    def barrier(self, _):
        """Barrier effect, adds small damage taken decrease to effected."""
        self.duration -= 1
        return 0.2

    def weakened(self, _):
        """Weakened effect, adds small damage taken increase to effected."""
        self.duration -= 1
        return -0.25

    def burning(self, data):
        """Burning effect, deals minor damage to effected."""
        data[2].health *= 0.96                       # deals 4 % of current health damage
        data[2].health = round(data[2].health - 4)   # deals 4 exact damage and rounds number.

        self.duration -= 1

    def venom(self, data):
        """Venom effect, deals minor damage to effected"""
        data[2].health -= 5
        self.duration -= 1

    def venom_empowered(self, data):
        """Venom effect [empowered], deals slightly more than minor damage to effected."""
        data[2].health -= 6
        self.duration -= 1

    def stasis_effect(self, _):
        """Stasis effect, stops effected from taking their turn.
        * No effect function as all is defined on turn taken."""
        self.duration -= 1

    def strength(self, _):
        """Strength effect, adds to damage modifier on melee attacks."""
        self.duration -= 1
        return 0.2

    def shielded(self, _):
        """Shielded effect, stops deal_damage function from dealing damage to effected."""
        self.duration -= 1

    def resistance(self, _):
        """Resistance effect, adds small damage taken decrease to effected."""
        self.duration -= 1
        return 0.2

    def staminaless(self, _):
        """Staminaless effect, decreases stamina cost for melee attacks of effected.
        * See use in Battle.py for effect code."""
        self.duration -= 1

    def defending(self, _):
        """Defending effect, adds damage taken decrease to effected."""
        return 0.4

    def opponent_enchanted_weapon(self, _):
        """Enchanted weapon effect, adds 4 post-calculation damage to melee attacks. [for foes]"""
        self.duration -= 1
        return 4


'''
empowered = Effect(0, "empowered", True)
regenerating = Effect("start", "regenerating", 3)
Effect("attacking", "strength", 4)
Effect("attacked", "resistance", 5)
Effect("end", "staminaless", 5)
'''  # Effect examples
