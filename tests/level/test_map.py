import unittest

from hunting.level.map import LevelTile, LevelMap


class TestPathfinding(unittest.TestCase):
    def test_basic_diagonal(self):
        level_map = LevelMap([[LevelTile() for _ in range(0, 5)] for _ in range(0, 5)])

        self.assertEqual([(1, 1), (2, 2), (3, 3), (4, 4)], level_map.a_star_path(0, 0, 4, 4))

    def test_paths_around_wall(self):
        level_map = LevelMap([[LevelTile() for _ in range(0, 3)] for _ in range(0, 5)])

        for x in range(1, 5):
            level_map[x][1].blocks = True

        self.assertEqual([(3, 0), (2, 0), (1, 0), (0, 1), (1, 2), (2, 2), (3, 2), (4, 2)],
                         level_map.a_star_path(4, 0, 4, 2))

    def tests_force_pathable_endpoint_parameter(self):
        level_map = LevelMap([[LevelTile(False, False)], [LevelTile(True, True)]])

        self.assertEqual([(1, 0)], level_map.a_star_path(0, 0, 1, 0, True))
        self.assertEqual([], level_map.a_star_path(0, 0, 1, 0, False))
