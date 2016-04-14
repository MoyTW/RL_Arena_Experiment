import hunting.constants as c


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

    def _use(self, user, target):
        raise NotImplementedError()


class PowerStrike(ActiveSkill):
    def __init__(self, accuracy_malus, power_bonus, stamina_cost, skill_type=c.SKILL_ACTIVE,
                 skill_name=c.SKILL_POWER_STRIKE):
        super().__init__(stamina_cost=stamina_cost, skill_name=skill_name, skill_type=skill_type)
        self.accuracy_malus = accuracy_malus
        self.power_bonus = power_bonus

    def _can_use(self, user, target):
        pass

    def _use(self, user, target):
        pass
