import unittest
from hunting.sim.effects import PropertyEffect
from hunting.sim.entities import *


class TestPropertyEffect(unittest.TestCase):
    def setUp(self):
        self.fighter = Fighter(100, 100, 100, 100, 0, speed=100)
        self.obj = GameObject('1', LevelLog(), None, None, 'test', fighter=self.fighter)

    def test_effect_timer(self):
        temp_buff = PropertyEffect(c.PROPERTY_MAX_HP, value=100, timer=50)
        self.fighter.add_effect(temp_buff)
        self.fighter.pass_time(50)
        self.assertEqual(self.fighter.max_hp, 200)

        self.fighter.pass_time(1)
        self.assertEqual(self.fighter.max_hp, 100)

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
