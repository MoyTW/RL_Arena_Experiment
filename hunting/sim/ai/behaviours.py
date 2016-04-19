from hunting.sim.entities import GameObject
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