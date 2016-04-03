import unittest
import unittest.mock as mock
from hunting.sim.entities import *
from hunting.level.log import LevelLog


class TestPropertyEffect(unittest.TestCase):
    def setUp(self):
        self.fighter = Fighter(100, 100, 100, 0, base_speed=100)
        self.obj = GameObject('1', LevelLog(), None, None, 'test', fighter=self.fighter)

    def test_add_remove_power(self):
        power_buff = PropertyEffect(PROPERTY_POWER, value=100)

        self.fighter.add_effect(power_buff)
        self.assertEqual(self.fighter.power, 200)

        self.fighter.remove_effect(power_buff)
        self.assertEqual(self.fighter.power, 100)

    def test_add_remove_speed(self):
        speed_buff = PropertyEffect(PROPERTY_SPEED, value=100)

        self.fighter.add_effect(speed_buff)
        self.assertEqual(self.fighter.speed, 200)

        self.fighter.remove_effect(speed_buff)
        self.assertEqual(self.fighter.speed, 100)

    def test_add_remove_defense(self):
        defense_buff = PropertyEffect(PROPERTY_DEFENSE, value=100)

        self.fighter.add_effect(defense_buff)
        self.assertEqual(self.fighter.defense, 200)

        self.fighter.remove_effect(defense_buff)
        self.assertEqual(self.fighter.defense, 100)


class TestFighter(unittest.TestCase):
    def setUp(self):
        self.dodger = Fighter(hp=100, defense=0, power=0, xp=0, dodge=0)
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
        self.dodger.hp = 100

        # Hits
        rand_fn.return_value = 57
        self.dodger.receive_attack('', 0, 11)
        self.assertEqual(self.dodger.hp, 89)
        self.dodger.hp = 100

        # Crits
        rand_fn.return_value = 130
        self.dodger.receive_attack('', 0, 10)
        self.assertEqual(self.dodger.hp, 85)
        self.dodger.hp = 100

    def test_minimum_speed_is_one(self):
        self.assertEqual(Fighter(1, 1, 1, 1, base_speed=-5).speed, 1)
        self.assertEqual(Fighter(1, 1, 1, 1, base_speed=0).speed, 1)
