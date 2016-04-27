import tdl
import itertools
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
    def __init__(self, level_tiles=None):
        self.log = LevelLog()
        self._width = None  # type: int
        self._height = None  # type: int
        self._all_objects = []
        self._map_set = False
        self._map = None
        self._factions = {}

        if level_tiles is not None:
            self.set_map(level_tiles)

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

    def a_star_path(self, x0, y0, x1, y1, force_pathable_endpoint=True):
        """Draw a A* path from the start coordinates to the end coordinates.

        :param x0: Starting x position.
        :param y0: Starting y position.
        :param x1: Ending x position. Need not be pathable.
        :param y1: Ending y position. Need not be pathable.
        :param force_pathable_endpoint: If True, treats the ending coordinates as pathable regardless of the actual status of
        the coordinates.
        :return: A vector of (x, y) pairs to the nearest adjacent square to (x1, y1) from (x0, y0). If there is no way
        to reach a square adjacent to (x1, y1) it will return an empty vector.
        """
        def cost_fn(x, y):
            if (not self.is_blocked(x, y)) or (force_pathable_endpoint is True and x == x1 and y == y1):
                return 1
            else:
                return 0
        finder = tdl.map.AStar(self._width, self._height, cost_fn)
        return finder.get_path(x0, y0, x1, y1)

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
        if x < 0 or y < 0 or x >= self._width or y >= self._height or self._map[x][y].blocks:
            return True
        for o in self._all_objects:
            if o.x == x and o.y == y:
                return True
        return False

    def get_adjacent_squares(self, x, y, remove_blocked=True):
        return [(x + x1, y + y1) for x1, y1 in itertools.product(range(-1, 2), range(-1, 2))
                if not (remove_blocked and self.is_blocked(x + x1, y + y1)) and not (x1 == 0 and y1 == 0)]

    def build_flood_fill_cost_map(self, x, y):
        cost_map = {(x, y): 0}
        nodes = [(x, y)]
        while len(nodes) > 0:
            next_nodes = []
            for node in nodes:
                next_cost = cost_map[node] + 1
                adjacent = self.get_adjacent_squares(node[0], node[1])
                for square in adjacent:
                    if square not in cost_map:
                        cost_map[square] = next_cost
                        next_nodes.append(square)
            nodes = next_nodes
        return cost_map

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
