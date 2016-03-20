import tdl


class LevelTile:
    def __init__(self, blocks=False, blocks_sight=None):
        self.blocks = blocks

        # If no sight parameter is passed in, sight blocking defaults to same as physical blocking
        if blocks_sight is None:
            self.blocks_sight = blocks
        else:
            self.blocks_sight = blocks_sight


class LevelMap:
    def __init__(self):
        self.width = None
        self.height = None
        self._all_objects = []
        self._map_set = False
        self._map = None

    def set_map(self, level_tiles):
        if self._map_set:
            raise ValueError('Cannot set map twice!')
        else:
            self._map = level_tiles
            self._map_set = True

    def get_object_by_id(self, oid):
        matching = [o for o in self._all_objects if o.oid == oid]
        return matching[0]

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

    def has_los(self, x0, y0, x1, y1):
        # The TDL Bresenham includes the origin point, necessitating the pop
        line = tdl.map.bresenham(x0, y0, x1, y1)
        line.pop(0)

        for (x, y) in line:
            if self.is_blocked(x, y):
                return False
        return True

    # Allow by-index access
    def __getitem__(self, index):
        return self._map[index]

    def finalize(self):
        if not (self.width and self.height and self._map):
            raise ValueError('Level has not been fully populated!')
        elif len(self._all_objects) == 0:
            raise ValueError('There are no objects, something is wrong!')
        else:
            return True


def create_level_map():
    LevelMap()
