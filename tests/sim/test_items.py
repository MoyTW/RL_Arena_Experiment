import unittest
from hunting.level.map import LevelMap, LevelTile
from hunting.sim.entities import GameObject, Fighter
from hunting.sim.items import Inventory, ThrowingItem


class TestThrowingItem(unittest.TestCase):
    def setUp(self):
        self.level = LevelMap()
        self.level.set_map([[LevelTile()] for _ in range(0, 5)])

        self.throwing_item = ThrowingItem(1000, 10)
        self.throwing = GameObject('1', self.level.log, None, None, 'item', item=self.throwing_item)
        self.inventory = Inventory(10, [self.throwing])

        self.target = GameObject('0', self.level.log, 0, 0, 'test', faction='0',
                                 fighter=Fighter(hp=9999, defense=0, power=0, xp=0,
                                                 death_function=self.level.remove_object))
        self.level.add_object(self.target)

        self.user = GameObject('0', self.level.log, 4, 0, 'test', faction='1', inventory=self.inventory,
                               fighter=Fighter(hp=9999, defense=0, power=0, xp=0,
                                               death_function=self.level.remove_object))

    def test_is_consumed_on_use(self):
        self.throwing.item.use(self.user, self.target, self.level)
        self.assertEqual(0, len(self.inventory))

    def test_does_damage(self):
        self.throwing.item.use(self.user, self.target, self.level)
        self.assertEqual(8999, self.target.fighter.hp)

    def test_respects_range(self):
        self.throwing_item.item_range = 1
        self.throwing.item.use(self.user, self.target, self.level)
        self.assertEqual(9999, self.target.fighter.hp)