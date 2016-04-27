import unittest
import hunting.level.map as level
import tests.level.level_utils as utils
import hunting.sim.runner as runner
import hunting.sim.ai.ais as ais
from hunting.sim.entities import GameObject, Fighter
import hunting.constants as c


class TestOpenDistance(unittest.TestCase):
    def setUp(self):
        self.level = level.LevelMap()
        self.runner = GameObject('1', self.level.log, None, None, 'runner', faction='1',
                                 fighter=Fighter(100, 100, 5, 5, 100), ai=ais.RunnerMonster(self.level))
        self.level.add_faction('1', {})
        self.level.add_object(self.runner)
        self.scary = GameObject('2', self.level.log, None, None, 'scary', faction='2', fighter=Fighter(5, 100, 0, 1, 1),
                                ai=ais.TestMonster(self.level))
        self.level.add_faction('2', {})
        self.level.add_object(self.scary)

    def test_builds_flood_fill_cost_map(self):
        utils.set_level_to_string(self.level, ".....\n"
                                              ".####\n"
                                              ".....\n")
        # If you ever have another pathfinding algorithm (you will) actually definte a Pathfinder class or something!
        open_distance = self.runner.ai.objectives_to_behaviours[c.OBJECTIVE_KITE][0]  # DUMB
        self.runner.set_coordinates(0, 0)
        self.assertEqual({(0, 0): 0, (1, 0): 1, (2, 0): 2, (3, 0): 3, (4, 0): 4, (0, 1): 1, (0, 2): 2, (1, 2): 2,
                          (2, 2): 3, (3, 2): 4, (4, 2): 5},
                         open_distance.build_cost_map())

    def test_flees_basic(self):
        utils.set_level_to_string(self.level, ".....\n"
                                              ".####\n"
                                              ".....\n")
        self.runner.set_coordinates(3, 2)
        self.scary.set_coordinates(4, 2)
        for i in range(7):
            runner.run_turn(self.level)
        self.assertEqual((4, 0), (self.runner.x, self.runner.y))

    def test_flees_longest_path(self):
        utils.set_level_to_string(self.level, "###.\n"
                                              ".#.#\n"
                                              ".#.#\n"
                                              "#.##\n"
                                              "#.##\n"
                                              "#.##")
        self.runner.set_coordinates(1, 3)
        self.scary.set_coordinates(1, 5)
        for i in range(10):
            runner.run_turn(self.level)
        self.assertEqual((3, 0), (self.runner.x, self.runner.y))

    def test_can_approach_during_flight(self):
        utils.set_level_to_string(self.level, "......\n"
                                              ".####.\n"
                                              ".#.##.\n"
                                              ".#..#.\n"
                                              ".###.#\n"
                                              "##..##\n"
                                              "..####")
        self.runner.set_coordinates(3, 3)
        self.scary.set_coordinates(0, 6)
        for i in range(12):
            runner.run_turn(self.level)
        self.assertEqual((0, 4), (self.runner.x, self.runner.y))

    def test_takes_shortest_path_to_destination(self):
        utils.set_level_to_string(self.level, ".........#\n"
                                              ".#######.#\n"
                                              "#...####.#\n"
                                              "####.###.#\n"
                                              "#####..#.#\n"
                                              "#######..#\n"
                                              "#########.")
        self.runner.set_coordinates(8, 5)
        self.scary.set_coordinates(9, 6)
        for i in range(9):
            runner.run_turn(self.level)
        self.assertEqual((0, 0), (self.runner.x, self.runner.y))
