import tdl

from hunting.level.log import LevelLog


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
        self.log = LevelLog()
        self._width = None
        self._height = None
        self._all_objects = []
        self._map_set = False
        self._map = None
        self._factions = {}

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def set_map(self, level_tiles):
        if self._map_set:
            raise ValueError('Cannot set map twice!')
        else:
            self._width = len(level_tiles)
            self._height = len(level_tiles[0])
            self._map = level_tiles
            self._map_set = True

    def pass_time(self, time):
        fighters = [o for o in self._all_objects if o.fighter is not None]
        for o in fighters:
            o.fighter.pass_time(time)

    def get_time_to_next_event(self):
        fighters = [o.fighter.time_until_turn for o in self._all_objects if o.fighter is not None]
        return min(fighters)

    def pass_time_to_next_event(self):
        time = self.get_time_to_next_event()
        self.pass_time(time)

    def get_objects_moving_now(self):
        fighters = [o for o in self._all_objects if o.fighter is not None and o.fighter.time_until_turn <= 0]
        return fighters

    def get_object_by_id(self, oid):
        matching = [o for o in self._all_objects if o.oid == oid]
        return matching[0]

    def add_faction(self, faction, faction_info):
        self._factions[faction] = faction_info

    def add_object(self, game_object):
        if game_object.faction not in self.get_factions():
            raise ValueError('Unknown faction!', game_object.faction)

        self._all_objects.append(game_object)

    def remove_object(self, game_object):
        self._all_objects.remove(game_object)

    def get_factions(self):
        return set(self._factions.keys())

    def get_faction_info(self, faction):
        return self._factions[faction]

    def get_objects_inside_faction(self, faction):
        return [o for o in self._all_objects if o.faction == faction]

    def get_objects_outside_faction(self, faction):
        return [o for o in self._all_objects if o.faction is not None and o.faction != faction]

    # TODO: Have some concept of 'edge of map' that is not 'blocked'?
    def is_blocked(self, x, y):
        if x < 0 or y < 0 or x >= self._width or y >= self._height:
            return True
        if self._map[x][y].blocks:
            return True
        for o in self._all_objects:
            if o.x == x and o.y == y:
                return True
        return False

    def has_los(self, x0, y0, x1, y1):
        # The TDL Bresenham includes the origin point and end points, necessitating the pop
        line = tdl.map.bresenham(x0, y0, x1, y1)
        line.pop(0)
        line.pop()

        for (x, y) in line:
            if self.is_blocked(x, y):
                return False
        return True

    # Allow by-index access
    def __getitem__(self, index):
        return self._map[index]

    def finalize(self):
        if not (self._width and self._height and self._map):
            raise ValueError('Level has not been fully populated!')
        elif len(self._all_objects) == 0:
            raise ValueError('There are no objects, something is wrong!')
        else:
            return True


def create_level_map():
    LevelMap()
