import unittest
import unittest.mock as mock

from hunting.level.map import LevelMap, LevelTile
from hunting.sim.entities import GameObject, Fighter
from hunting.sim.skills import PowerStrike


class TestPowerStrike(unittest.TestCase):
    def setUp(self):
        level = LevelMap()
        level.set_map([[LevelTile()], [LevelTile()]])

        self.power_strike = PowerStrike(-25, 50, 25)
        self.attacker = GameObject('0', level.log, 0, 0, 'attacker', faction='0',
                                   fighter=Fighter(100, 100, 0, 0, 0, speed=1, skills=[self.power_strike]))
        level.add_faction('0', {})
        level.add_object(self.attacker)

        self.defender = GameObject('1', level.log, 1, 0, 'defender', faction='1',
                                   fighter=Fighter(100, 100, defense=0, power=10, xp=0, speed=100))
        level.add_faction('1', {})
        level.add_object(self.defender)

    @mock.patch('random.randint', return_value=40)
    def test_reduces_accuracy(self, _):
        self.power_strike.use(self.attacker, self.defender)
        self.assertEqual(self.defender.fighter.hp, 100)

    @mock.patch('random.randint', return_value=85)
    def test_increases_power(self, _):
        self.power_strike.use(self.attacker, self.defender)
        self.assertEqual(self.defender.fighter.hp, 50)

    def test_effect_is_removed(self):
        self.power_strike.use(self.attacker, self.defender)
        self.assertEqual(len(self.attacker.fighter.effect_list), 2)
        self.attacker.fighter.pass_time(1)
        self.assertEqual(len(self.attacker.fighter.effect_list), 0)
