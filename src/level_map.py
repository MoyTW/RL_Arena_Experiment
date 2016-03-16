import random


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

        return _map

    # Allow by-index access
    def __getitem__(self, index):
        return self._map[index]


def create_level_map():
    LevelMap()
