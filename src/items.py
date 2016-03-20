from src.entities import GameObject
from src.level_map import LevelMap


class Inventory:
    def __init__(self, max_size, carried_items):
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


class Item:
    def __init__(self, item_type):
        self.owner = None
        self.item_type = item_type

    def _use(self, user, target, level_map):
        raise NotImplementedError()

    def can_use(self, user: GameObject, target: GameObject, level_map):
        raise NotImplementedError()

    def use(self, user: GameObject, target: GameObject, level_map):
        """
        Use the item on the target.
        :param target: The target, usually a GameObject
        :param user : The entity using the item; distinct from owner, which is the GameObject the item is composed into
        :param level_map: The level map state
        :return: True if the item is been consumed, False if it has not
        """
        owner = self.owner  # type: GameObject
        owner.log.log_begin_item_use(owner.oid, user.oid, target.oid)
        self._use(user, target, level_map)
        owner.log.log_end_item_use(owner.oid)


class TestItem(Item):
    def __init__(self, item_type):
        super().__init__(item_type=item_type)

    def _use(self, user: GameObject, target: GameObject, level_map):
        target.fighter.heal(10)

    def can_use(self, user: GameObject, target: GameObject, level_map):
        return False


class ThrowingItem(Item):
    def __init__(self, item_type, item_power, item_range):
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
