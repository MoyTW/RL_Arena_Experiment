class MonsterAI(object):
    def __init__(self, level):
        self.owner = None
        self.level = level

    def take_turn(self):
        self.owner.log.log_begin_turn(self.owner.oid)
        self._take_turn()
        self.owner.log.log_end_turn(self.owner.oid)
        self.owner.fighter.end_turn()

    def _take_turn(self):
        raise NotImplementedError('Subclass this before usage please.')


class DummyAI(MonsterAI):
    def _take_turn(self):
        pass


class TestMonster(MonsterAI):
    def _take_turn(self):
        enemies = self.level.get_objects_outside_faction(self.owner.faction)

        if len(enemies) > 0:
            # Identify the closest enemy
            distances = {self.owner.distance_to(e): e for e in enemies}
            closest_distance = min(distances)
            closest_enemy = distances[closest_distance]

            # Inspect inventory for usable items
            if self.owner.inventory is not None:
                usable = self.owner.inventory.get_usable_items()
                throwing_items = [i for i in usable if i.item.can_use(self.owner, closest_enemy, self.level)]
            else:
                throwing_items = []

            # Attack if adjacent
            if closest_distance <= 1.5:
                self.owner.fighter.attack(closest_enemy)
            # Throw if you have a throwing item
            elif len(throwing_items) > 0:
                throwing_items[0].item.use(self.owner, closest_enemy, self.level)
            else:
                self.owner.move_towards(closest_enemy.x, closest_enemy.y, self.level)
