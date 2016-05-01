import hunting.sim.items.core as items
from hunting.sim.entities import GameObject
from hunting.constants import *


class Equipment(items.Item):
    def __init__(self, slot, effects, is_equipped=False, item_type=ITEM_EQUIPMENT):
        if item_type != ITEM_EQUIPMENT:  # TODO: Very awkward! Maybe wrap in factory function?
            raise ValueError()

        super().__init__(item_type=item_type, max_uses=None)
        self.slot = slot
        self.effects = effects
        self.is_equipped = is_equipped

    def can_equip(self, target: GameObject):
        slots = target.fighter.equipment_slots
        return self.slot in slots and (not self.is_equipped) and slots[self.slot] is None

    def can_dequip(self, target: GameObject):
        slots = target.fighter.equipment_slots
        return self.slot in slots and self.is_equipped and slots[self.slot] is self.owner

    def can_use(self, user: GameObject, target: GameObject, level_map):
        return self.can_equip(target) or self.can_dequip(target)

    def _use(self, user, target, level_map):
        if not self.can_use(user, target, level_map):
            raise ValueError('Cannot equip this equipment! ', self.owner.name, target.name)

        if self.can_equip(target):
            self.is_equipped = True
            target.fighter.equipment_slots[self.slot] = self.owner
            for effect in self.effects:
                target.fighter.add_effect(effect)
        elif self.can_dequip(target):
            self.is_equipped = False
            target.fighter.equipment_slots[self.slot] = None
            for effect in self.effects:
                target.fighter.remove_effect(effect)
