import unittest
import tests.level.level_utils as utils
import hunting.sim.runner as runner
import hunting.sim.ai.ais as ais
from hunting.sim.entities import GameObject, Fighter

class TestOpenDistance(unittest.TestCase):
    def setUp(self):
        self.level = utils.generate_5x3_long_c()
        self.runner = GameObject('1', self.level.log, 3, 2, 'runner', faction='1', fighter=Fighter(100, 100, 5, 5, 100),
                                 ai=ais.RunnerMonster(self.level))
        self.level.add_faction('1', {})
        self.level.add_object(self.runner)
        self.scary = GameObject('2', self.level.log, 4, 2, 'scary', faction='2', fighter=Fighter(5, 100, 0, 1, 1),
                                ai=ais.TestMonster(self.level))
        self.level.add_faction('2', {})
        self.level.add_object(self.scary)

    def test_flees(self):
        for i in range(10):
            runner.run_turn(self.level)
        self.assertEqual(4, self.runner.x)
        self.assertEqual(0, self.runner.y)

