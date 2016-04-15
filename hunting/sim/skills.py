import hunting.constants as c
from hunting.sim.entities import GameObject
from hunting.sim.effects import PropertyEffect


class Skill:
    def __init__(self, skill_type, skill_name):
        self.skill_type = skill_type
        self.skill_name = skill_name


class PassiveSkill(Skill):
    def __init__(self, skill_name=None, skill_type=c.SKILL_PASSIVE):
        super().__init__(skill_type=skill_type, skill_name=skill_name)
        # TODO: Add effect on start

    # TODO: Return the desired effect
    def effect(self):
        raise NotImplementedError()


class ToggleSkill(Skill):
    def __init__(self, skill_name=None, skill_type=c.SKILL_TOGGLE):
        super().__init__(skill_type=skill_type, skill_name=skill_name)
        # TODO: Add effect on start

    def can_use(self):
        raise NotImplementedError()

    def use(self, user):
        raise NotImplementedError()


class ActiveSkill(Skill):
    def __init__(self, stamina_cost, skill_name=None, skill_type=c.SKILL_ACTIVE):
        super().__init__(skill_type=skill_type, skill_name=skill_name)
        self.stamina_cost = stamina_cost

    def can_use(self, user, target):
        return user.fighter.stamina >= self.stamina_cost and self._can_use(user, target)

    def _can_use(self, user, target):
        raise NotImplementedError()

    def use(self, user, target):
        if self.can_use(user, target):
            user.fighter.remove_stamina(self.stamina_cost)
            self._use(user, target)
        else:
            raise ValueError('attempting to use unusable skill, something with the AI broke!')

    def _use(self, user, target):
        raise NotImplementedError()


class PowerStrike(ActiveSkill):
    def __init__(self, accuracy_malus, power_bonus, stamina_cost, skill_type=c.SKILL_ACTIVE,
                 skill_name=c.SKILL_POWER_STRIKE):
        super().__init__(stamina_cost=stamina_cost, skill_name=skill_name, skill_type=skill_type)
        self.accuracy_malus = accuracy_malus
        self.power_bonus = power_bonus

    def _can_use(self, user: GameObject, target: GameObject):
        return user.is_adjacent(target)

    # TODO: Allow composite effects
    def _use(self, user: GameObject, target: GameObject):
        power_strike_power = PropertyEffect(c.PROPERTY_POWER, self.power_bonus, duration=0)
        power_strike_accuracy = PropertyEffect(c.PROPERTY_ACCURACY, self.accuracy_malus, duration=0)
        user.fighter.add_effect(power_strike_power)
        user.fighter.add_effect(power_strike_accuracy)
        user.fighter.attack(target)
