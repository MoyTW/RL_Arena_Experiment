import unittest
from hunting.sim.effects import PropertyEffect
from hunting.sim.entities import *


class TestPropertyEffect(unittest.TestCase):
    def setUp(self):
        self.fighter = Fighter(100, 100, 100, 0, base_speed=100)
        self.obj = GameObject('1', LevelLog(), None, None, 'test', fighter=self.fighter)

    def test_add_remove_power(self):
        power_buff = PropertyEffect(c.PROPERTY_POWER, value=100)

        self.fighter.add_effect(power_buff)
        self.assertEqual(self.fighter.power, 200)

        self.fighter.remove_effect(power_buff)
        self.assertEqual(self.fighter.power, 100)

    def test_add_remove_speed(self):
        speed_buff = PropertyEffect(c.PROPERTY_SPEED, value=100)

        self.fighter.add_effect(speed_buff)
        self.assertEqual(self.fighter.speed, 200)

        self.fighter.remove_effect(speed_buff)
        self.assertEqual(self.fighter.speed, 100)

    def test_add_remove_defense(self):
        defense_buff = PropertyEffect(c.PROPERTY_DEFENSE, value=100)

        self.fighter.add_effect(defense_buff)
        self.assertEqual(self.fighter.defense, 200)

        self.fighter.remove_effect(defense_buff)
        self.assertEqual(self.fighter.defense, 100)
