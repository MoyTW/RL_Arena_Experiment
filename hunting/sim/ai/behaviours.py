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
    def furthest_path(self, depth=None):
        """ Uses the dumbest possible algorithm to find a path away from a monster (scan literally every square). This
        will obviously have to be replaced. It's horrifying, really.

        :param depth: How many steps you would like the search to reach.
        :return: A list of (x, y) pairs indicating the furthest path.
        """
        level = self.ai.level  # type: LevelMap
        owner = self.ai.owner
        furthest = []
        furthest_distance = -1

        # TODO: Dear God.
        level.remove_object(owner)
        for x in range(level.width):
            for y in range(level.height):
                if len(level.a_star_path(owner.x, owner.y, x, y, False)) == 0:
                    pass
                else:
                    dist = len(level.a_star_path(x, y, self.ai.target.x, self.ai.target.y))
                    if dist == furthest_distance:
                        furthest.append([x, y])
                    elif dist > furthest_distance:
                        furthest_distance = dist
                        furthest.clear()
                        furthest.append([x, y])
        level.add_object(owner)

        if len(furthest) > 0:
            furthest_point = random.choice(furthest)
            return level.a_star_path(owner.x, owner.y, furthest_point[0], furthest_point[1])[0]
        else:
            return None

    def can_execute(self):
        self.next = self.furthest_path()
        return self.next

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