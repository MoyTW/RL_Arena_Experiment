from hunting.sim.entities import GameObject
import hunting.sim.skills as skills
import hunting.constants as c

OBJECTIVE_ELIMINATE = 'eliminate'
OBJECTIVE_PROTECT = 'protect'
OBJECTIVE_FORTIFY = 'fortify'
OBJECTIVE_FLEE = 'flee'


class Objective:
    def __init__(self, objective):
        self.objective = objective


class ObjectiveEliminate(Objective):
    def __init__(self, target, objective=OBJECTIVE_ELIMINATE):
        super().__init__(objective=objective)
        self.target = target


class ObjectiveProtect(Objective):
    def __init__(self, target, objective=OBJECTIVE_PROTECT):
        super().__init__(objective=objective)
        self.target = target


class ObjectiveFortify(Objective):
    def __init__(self, x, y, radius, enemy_direction, friendly_direction, objective=OBJECTIVE_FORTIFY):
        super().__init__(objective=objective)
        self.x = x
        self.y = y
        self.radius = radius
        self.enemy_direction = enemy_direction
        self.friendly_direction = friendly_direction


class ObjectiveEscape(Objective):
    def __init__(self, objective=OBJECTIVE_FLEE):
        super().__init__(objective=objective)


class Behaviour:
    def __init__(self, ai):
        self.ai = ai  # type: MonsterAI

    def can_execute(self):
        raise NotImplementedError()

    def execute(self):
        raise NotImplementedError()


class BehaviourCloseDistance(Behaviour):
    def can_execute(self):
        return not self.ai.owner.is_adjacent(self.ai.target)

    def execute(self):
        target = self.ai.target  # type: GameObject
        self.ai.owner.move_towards(target.x, target.y, self.ai.level)


class BehaviourBasicMelee(Behaviour):
    def can_execute(self):
        return self.ai.owner.is_adjacent(self.ai.target)

    def execute(self):
        self.ai.owner.fighter.attack(self.ai.target)  # TODO: I don't really like this degree of chaining.


class BehaviourUseActiveSkill(Behaviour):
    def __init__(self, ai, skill: skills.ActiveSkill):
        super().__init__(ai)
        self.skill = skill

    def can_execute(self):
        return self.skill.can_use(self.ai.owner, self.ai.target)

    def execute(self):
        self.skill.use(self.ai.owner, self.ai.target)


class BehaviourUseThrowingItems(Behaviour):
    def is_usable_throwing_item(self, item: GameObject):
        i = item.item
        return i.item_type == c.ITEM_THROWING and i.can_use(self.ai.owner, self.ai.target, self.ai.level)

    def get_usable_throwing_items(self):
        inventory = self.ai.owner.inventory
        if inventory is not None:
            return [i for i in inventory.get_usable_items() if self.is_usable_throwing_item(i)]
        else:
            return None

    def can_execute(self):
        usables = self.get_usable_throwing_items()
        return usables is not None and len(usables) > 0

    def execute(self):
        self.get_usable_throwing_items()[0].item.use(self.ai.owner, self.ai.target, self.ai.level)


class MonsterAI(object):
    def __init__(self, level):
        self.level = level
        self.owner = None
        self.objective = None

    def take_turn(self):
        self.owner.log.log_begin_turn(self.owner.oid)
        self.assess_objective()
        self._take_turn()
        self.owner.log.log_end_turn(self.owner.oid)
        self.owner.fighter.end_turn()

    def assess_objective(self):
        raise NotImplementedError()

    def _take_turn(self):
        raise NotImplementedError('Subclass this before usage please.')

    @property
    def target(self):
        return self.objective.target


class DummyAI(MonsterAI):
    def assess_objective(self):
        pass

    def _take_turn(self):
        pass


class TestMonster(MonsterAI):
    def __init__(self, level):
        super().__init__(level)
        self.eliminate_behaviours = [BehaviourBasicMelee(self), BehaviourUseThrowingItems(self),
                                     BehaviourCloseDistance(self)]

    def assess_objective(self):
        enemies = self.level.get_objects_outside_faction(self.owner.faction)

        if len(enemies) > 0:
            distances = {self.owner.distance_to(e): e for e in enemies}
            closest_distance = min(distances)
            closest_enemy = distances[closest_distance]
            self.objective = ObjectiveEliminate(target=closest_enemy)

    def _take_turn(self):
        if isinstance(self.objective, ObjectiveEliminate):
            for b in self.eliminate_behaviours:
                if b.can_execute():
                    b.execute()
                    break
