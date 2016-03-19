import random
from src.entities import GameObject, Fighter
from src.ais import TestMonster


class LevelTile:
    def __init__(self, blocks=False, blocks_sight=None):
        self.blocks = blocks

        # If no sight parameter is passed in, sight blocking defaults to same as physical blocking
        if blocks_sight is None:
            self.blocks_sight = blocks
        else:
            self.blocks_sight = blocks_sight


class LevelMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._all_objects = []

        self._map = self._gen_map()

    def _gen_map(self):
        _map = [[LevelTile()
                 for _ in range(self.height)]
                for _ in range(self.width)]

        # Test columns
        for _ in range(20):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            _map[x][y].blocks = True
            _map[x][y].blocks_sight = True

        # Generate a couple of test monsters
        for _ in range(3):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            fighter_component = Fighter(hp=10, defense=0, power=1, xp=30, base_speed=100)
            ai_component = TestMonster(self)
            monster = GameObject(x, y, 'test monster', faction='1', blocks=True, fighter=fighter_component,
                                 ai=ai_component)
            self.add_object(monster)

        for _ in range(3):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            fighter_component = Fighter(hp=10, defense=0, power=1, xp=30, base_speed=100)
            ai_component = TestMonster(self)
            monster = GameObject(x, y, 'test monster', faction='2', blocks=True, fighter=fighter_component,
                                 ai=ai_component)
            self.add_object(monster)

        return _map

    def add_object(self, game_object):
        self._all_objects.append(game_object)

    def remove_object(self, game_object):
        self._all_objects.remove(game_object)

    def get_objects_inside_faction(self, faction):
        return [o for o in self._all_objects if o.faction == faction]

    def get_objects_outside_faction(self, faction):
        return [o for o in self._all_objects if o.faction is not None and o.faction != faction]

    def is_blocked(self, x, y):
        if self._map[x][y].blocks:
            return True
        for o in self._all_objects:
            if o.x == x and o.y == y:
                return True
        return False

    # Allow by-index access
    def __getitem__(self, index):
        return self._map[index]


def create_level_map():
    LevelMap()
