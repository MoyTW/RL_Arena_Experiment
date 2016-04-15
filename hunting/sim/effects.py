from hunting.constants import *


class Effect:
    """ Effects are anything which changes the state of the fighter, but which at some future point might be rolled
    back. This category includes but is not limited to buffs, debuffs, and equipment bonuses. """
    def __init__(self, effect_type, duration=None):
        self.effect_type = effect_type
        self.duration = duration


class PropertyEffect(Effect):
    def __init__(self, property_type, value, duration=None, effect_type=EFFECT_TYPE_PROPERTY):
        if effect_type != EFFECT_TYPE_PROPERTY:  # TODO: Very awkward! Validate input by schema to prevent?
            raise ValueError()

        super().__init__(effect_type=effect_type, duration=duration)
        self.property_type = property_type
        self.value = value
