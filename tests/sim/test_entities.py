import unittest
import unittest.mock as mock
from hunting.sim.entities import *
from hunting.level.map import LevelMap, LevelTile
from hunting.level.log import LevelLog


class TestGameObject(unittest.TestCase):
    def setUp(self):
        self.level_map = LevelMap()
        self.level_map.set_map([[LevelTile() for _ in range(0, 5)] for _ in range(0, 5)])

    def test_movable_squares(self):
        eight_options = GameObject('1', self.level_map.log, 2, 2, 'eight')
        options = eight_options.movable_squares(self.level_map)
        self.assertEqual([[1, 1], [1, 2], [1, 3], [2, 1], [2, 3], [3, 1], [3, 2], [3, 3]], options)

        three_options = GameObject('2', self.level_map.log, 0, 0, 'three')
        options = three_options.movable_squares(self.level_map)
        self.assertEqual([[0, 1], [1, 0], [1, 1]], options)

        five_options = GameObject('3', self.level_map.log, 4, 2, 'five')
        options = five_options.movable_squares(self.level_map)
        self.assertEqual([[3, 1], [3, 2], [3, 3], [4, 1], [4, 3]], options)


class TestFighter(unittest.TestCase):
    def setUp(self):
        self.dodger = Fighter(max_hp=100, max_stamina=100, defense=0, power=0, xp=0, dodge=0)
        GameObject('1', LevelLog(), None, None, 'test', fighter=self.dodger)

    @mock.patch('random.randint')
    def test_receive_attack(self, rand_fn):
        # Misses
        rand_fn.return_value = 13
        self.dodger.receive_attack('', 0, 10)
        self.assertEqual(self.dodger.hp, 100)

        # Grazes
        rand_fn.return_value = 40
        self.dodger.receive_attack('', 0, 11)
        self.assertEqual(self.dodger.hp, 95)
        self.dodger.heal(5)

        # Hits
        rand_fn.return_value = 57
        self.dodger.receive_attack('', 0, 11)
        self.assertEqual(self.dodger.hp, 89)
        self.dodger.heal(11)

        # Crits
        rand_fn.return_value = 130
        self.dodger.receive_attack('', 0, 10)
        self.assertEqual(self.dodger.hp, 85)
        self.dodger.heal(15)

    def test_minimum_speed_is_one(self):
        self.assertEqual(Fighter(1, 1, 1, 1, 1, speed=-5).speed, 1)
        self.assertEqual(Fighter(1, 1, 1, 1, 1, speed=0).speed, 1)
