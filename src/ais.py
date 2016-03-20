class MonsterAI(object):
    def __init__(self, level):
        self.owner = None
        self.level = level

    def take_turn(self):
        self.owner.log.log_begin_turn(self.owner.oid)
        self._take_turn()

    def _take_turn(self):
        raise NotImplementedError('Subclass this before usage please.')


class TestMonster(MonsterAI):
    def _take_turn(self):
        enemies = self.level.get_objects_outside_faction(self.owner.faction)
        if len(enemies) > 0:
            distances = {self.owner.distance_to(e): e for e in enemies}
            closest_distance = min(distances)
            closest_enemy = distances[closest_distance]
            if closest_distance <= 1.5:
                self.owner.fighter.attack(closest_enemy)
            else:
                self.owner.move_towards(closest_enemy.x, closest_enemy.y, self.level)
