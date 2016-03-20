from src.entities import GameObject


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
