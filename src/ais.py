class MonsterAI(object):
    def __init__(self, level):
        self.owner = None
        self.level = level

    def take_turn(self):
        raise NotImplementedError('Subclass this before usage please.')


class TestMonster(MonsterAI):
    def take_turn(self):
        enemies = self.level.get_objects_outside_faction(self.owner.faction)
        distances = {self.owner.distance_to(e): e for e in enemies}
        closest_enemy = distances[min(distances)]
        self.owner.move_towards(closest_enemy.x, closest_enemy.y, self.level)
