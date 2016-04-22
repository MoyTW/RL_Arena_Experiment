import hunting.constants as c


class Objective:
    def __init__(self, objective_name):
        self.objective_name = objective_name


class ObjectiveEliminate(Objective):
    def __init__(self, target, objective_name=c.OBJECTIVE_ELIMINATE):
        super().__init__(objective_name=objective_name)
        self.target = target


class ObjectiveProtect(Objective):
    def __init__(self, target, objective_name=c.OBJECTIVE_PROTECT):
        super().__init__(objective_name=objective_name)
        self.target = target


class ObjectiveFortify(Objective):
    def __init__(self, x, y, radius, enemy_direction, friendly_direction, objective_name=c.OBJECTIVE_FORTIFY):
        super().__init__(objective_name=objective_name)
        self.x = x
        self.y = y
        self.radius = radius
        self.enemy_direction = enemy_direction
        self.friendly_direction = friendly_direction


class ObjectiveKite(Objective):
    def __init__(self, target, objective_name=c.OBJECTIVE_KITE):
        super().__init__(objective_name=objective_name)
        self.target = target


class ObjectiveEscape(Objective):
    def __init__(self, objective_name=c.OBJECTIVE_FLEE):
        super().__init__(objective_name=objective_name)


class MonsterAI(object):
    def __init__(self, level, objectives_to_behaviours):
        self.level = level
        self.objectives_to_behaviours = objectives_to_behaviours
        self.owner = None  # type: GameObject
        self.objective = None

    def execute_objective(self):
        if self.objective is not None:
            behaviours_for_objective = self.objectives_to_behaviours[self.objective.objective_name]
            for b in behaviours_for_objective:
                if b.can_execute():
                    b.execute()
                    break

    def take_turn(self):
        self.owner.log.log_begin_turn(self.owner.oid)
        self.assess_objective()
        self.execute_objective()
        self.owner.log.log_end_turn(self.owner.oid)
        self.owner.fighter.end_turn()

    def assess_objective(self):
        raise NotImplementedError()

    @property
    def target(self):
        return self.objective.target
