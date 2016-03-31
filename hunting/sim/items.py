from hunting.level.map import LevelMap
from hunting.sim.entities import GameObject
from hunting.constants import *


class Inventory:
    def __init__(self, max_size, carried_items=[]):
        self.max_size = max_size
        self._items = []
        for i in carried_items:
            self.add_item(i)

    def add_item(self, item: GameObject):
        if item.item is None and item.equipment is None:
            raise ValueError('Cannot add a GameObject to inventory if it has no item or equipment attribute!')

        if len(self._items) >= self.max_size:
            return False
        else:
            self._items.append(item)
            return True

    def get_usable_items(self):
        return [i for i in self._items if i.item is not None]

    def remove_item(self, item):
        self._items.remove(item)

    def __len__(self):
        return len(self._items)


class Item:
    def __init__(self, item_type, max_uses=1):
        self.owner = None
        self.item_type = item_type
        self.remaining_uses = max_uses
        self.max_uses = max_uses

    def _use(self, user, target, level_map):
        raise NotImplementedError()

    def can_use(self, user: GameObject, target: GameObject, level_map):
        raise NotImplementedError()

    def use(self, user: GameObject, target: GameObject, level_map):
        """
        Use the item on the target. Reduces the number of remaining usages by 1, and if it reaches 0, removes the item
        from the user's inventory.
        :param target: The target, usually a GameObject
        :param user : The entity using the item; distinct from owner, which is the GameObject the item is composed into
        :param level_map: The level map state
        """
        owner = self.owner  # type: GameObject
        owner.log.log_begin_item_use(owner.oid, user.oid, target.oid)
        self._use(user, target, level_map)
        if self.max_uses:
            self.remaining_uses -= 1
            if self.remaining_uses < 1:
                user.inventory.remove_item(owner)
        owner.log.log_end_item_use(owner.oid)


class Equipment(Item):
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
            raise ValueError('Cannot equip this equipment! ', self, target)

        if self.can_equip(target):
            self.is_equipped = True
            target.fighter.equipment_slots[self.slot] = self.owner
        elif self.can_dequip(target):
            self.is_equipped = False
            target.fighter.equipment_slots[self.slot] = None


class TestItem(Item):
    def __init__(self, item_type):
        super().__init__(item_type=item_type)

    def _use(self, user: GameObject, target: GameObject, level_map):
        target.fighter.heal(10)

    def can_use(self, user: GameObject, target: GameObject, level_map):
        return False


class ThrowingItem(Item):
    def __init__(self, item_power, item_range, item_type=ITEM_THROWING):
        if item_type != ITEM_THROWING:  # TODO: Very awkward! Maybe wrap in factory function?
            raise ValueError('ThrowingItem was passed a bad item_type!')

        super().__init__(item_type=item_type)
        self.item_power = item_power
        self.item_range = item_range

    def _use(self, user: GameObject, target: GameObject, level_map: LevelMap):
        if not self.can_use(user, target, level_map):
            return False

        target.fighter.take_damage(self.item_power)  # TODO: Add a is_direct parameter to this function call!

        # Throwing items are always consumed on use
        return True

    def can_use(self, user: GameObject, target: GameObject, level_map):
        target_range = user.distance_to(target)

        if target_range > self.item_range:
            return False
        elif not level_map.has_los(user.x, user.y, target.x, target.y):
            return False
        else:
            return True
