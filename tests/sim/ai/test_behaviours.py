import unittest
import hunting.level.map as level
import tests.level.level_utils as utils
import hunting.sim.runner as runner
import hunting.sim.ai.ais as ais
from hunting.sim.entities import GameObject, Fighter


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

    def test_flees_basic(self):
        utils.set_level_to_string(self.level, ".....\n"
                                              ".####\n"
                                              ".....\n")
        self.runner.set_coordinates(2, 2)
        self.scary.set_coordinates(4, 2)
        for i in range(6):
            runner.run_turn(self.level)
        self.assertEqual((4, 0), (self.runner.x, self.runner.y))

    def test_fights_if_engaged(self):
        utils.set_level_to_string(self.level, ".....\n"
                                              ".####\n"
                                              ".....\n")
        self.runner.set_coordinates(3, 2)
        self.scary.set_coordinates(4, 2)
        for i in range(2):
            runner.run_turn(self.level)
        self.assertEqual((3, 2), (self.runner.x, self.runner.y))

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
        utils.set_level_to_string(self.level, ".........##\n"
                                              ".#####.#.##\n"
                                              "#...###..##\n"
                                              "####.###.##\n"
                                              "#####..#.##\n"
                                              "#######..##\n"
                                              "#########..")
        self.runner.set_coordinates(8, 5)
        self.scary.set_coordinates(10, 6)
        for i in range(9):
            runner.run_turn(self.level)
            print(self.runner.x, self.runner.y)
        self.assertEqual((1, 0), (self.runner.x, self.runner.y))
