import random
from hunting.sim.entities import GameObject
from hunting.sim.ai.core import MonsterAI
from hunting.level.map import LevelMap
import hunting.sim.skills as skills
import hunting.constants as c


class Behaviour:
    def __init__(self, ai):
        self.ai = ai  # type: MonsterAI

    def can_execute(self):
        raise NotImplementedError()

    def execute(self):
        raise NotImplementedError()


class CloseDistance(Behaviour):
    def can_execute(self):
        return not self.ai.owner.is_adjacent(self.ai.target)

    def execute(self):
        target = self.ai.target  # type: GameObject
        self.ai.owner.move_towards(target.x, target.y, self.ai.level)


class OpenDistance(Behaviour):
    def __init__(self, ai, min_dist=1, max_dist=None):
        super().__init__(ai=ai)
        self.min_dist = min_dist
        self.max_dist = max_dist

    def furthest_path(self):
        """ Gets the shortest path to the furthest square from the target, and returns either the (x, y) coordinates or,
         None if it cannot kite.

        :param min_dist: The minimum distance between the owner and target. If the target enters this distance, the
        owner will stop kiting.
        :return: Either the first (x, y) step to the furthest square from the target, or None if there is no further
        path to run or the target has already reached min_dist squares of the owner.
        """
        level = self.ai.level  # type: LevelMap
        owner = self.ai.owner
        target = self.ai.target

        current_dist = len(level.a_star_path(target.x, target.y, owner.x, owner.y))
        if current_dist <= self.min_dist or current_dist > self.max_dist:
            return None

        owner_cost_map = level.build_flood_fill_cost_map(owner.x, owner.y)
        target_cost_map = level.build_flood_fill_cost_map(target.x, target.y)
        viable = [k for k, v in owner_cost_map.items()
                  if k not in target_cost_map or target_cost_map[k] - owner_cost_map[k] > self.min_dist]
        end = max(viable, key=lambda x: owner_cost_map[x])

        path = level.a_star_path(owner.x, owner.y, end[0], end[1])
        if len(path) > 0:
            return path[0]
        else:
            return None

    def can_execute(self):
        self.next = self.furthest_path()
        if self.next is not None:
            return True
        else:
            return False

    def execute(self):
        self.ai.owner.move_towards(self.next[0], self.next[1], self.ai.level)


class BasicMelee(Behaviour):
    def can_execute(self):
        return self.ai.owner.is_adjacent(self.ai.target)

    def execute(self):
        self.ai.owner.fighter.attack(self.ai.target)  # TODO: I don't really like this degree of chaining.


class UseActiveSkill(Behaviour):
    def __init__(self, ai, skill: skills.ActiveSkill):
        super().__init__(ai)
        self.skill = skill

    def can_execute(self):
        return self.skill.can_use(self.ai.owner, self.ai.target)

    def execute(self):
        self.skill.use(self.ai.owner, self.ai.target)


class UseAnyThrowingItem(Behaviour):
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