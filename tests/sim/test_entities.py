import unittest
from hunting.sim.entities import *


class TestFighter(unittest.TestCase):
    def test_base_speed_must_be_positive(self):
        with self.assertRaises(ValueError):
            Fighter(1, 1, 1, 1, base_speed=-5)

        with self.assertRaises(ValueError):
            Fighter(1, 1, 1, 1, base_speed=0)

        with self.assertRaises(ValueError):
            f = Fighter(1, 1, 1, 1)
            f.base_speed = -1

        with self.assertRaises(ValueError):
            f = Fighter(1, 1, 1, 1)
            f.base_speed = 0
