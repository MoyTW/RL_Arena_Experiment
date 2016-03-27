import unittest
from hunting.sim.entities import *


class TestFighter(unittest.TestCase):
    def test_minimum_speed_is_one(self):
        self.assertEqual(Fighter(1, 1, 1, 1, base_speed=-5).speed, 1)
        self.assertEqual(Fighter(1, 1, 1, 1, base_speed=0).speed, 1)
