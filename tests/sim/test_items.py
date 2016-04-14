import unittest
from hunting.level.map import LevelMap, LevelTile
from hunting.sim.effects import PropertyEffect
from hunting.sim.entities import GameObject, Fighter
from hunting.sim.items import Equipment, ThrowingItem, Inventory
from hunting.constants import *
import unittest.mock as mock


class TestEquipment(unittest.TestCase):
    def setUp(self):
        self.level = LevelMap()

        self.test_id = '1'
        self.test_slot = 'test slot'
        self.effect = PropertyEffect(property_type=PROPERTY_POWER, value=10)
        self.sword = GameObject(self.test_id, self.level.log, None, None, 'sword',
                                item=Equipment(slot=self.test_slot, effects=[self.effect]))
        self.slot_object = GameObject('9', self.level.log, None, None, 'has slot',
                                      fighter=Fighter(10, 10, 10, 10, 0, equipment_slots=[self.test_slot]))
        self.no_slot_object = GameObject('8', self.level.log, None, None, 'does not have slot',
                                         fighter=Fighter(10, 10, 10, 10, 0, equipment_slots=[]))

    def test_can_equip_and_unequip(self):
        self.sword.item.use(self.slot_object, self.slot_object, self.level)
        self.assertTrue(self.sword.item.is_equipped)
        self.assertEqual({self.test_slot: self.sword}, self.slot_object.fighter.equipment_slots)

        self.sword.item.use(self.slot_object, self.slot_object, self.level)
        self.assertFalse(self.sword.item.is_equipped)
        self.assertEqual({self.test_slot: None}, self.slot_object.fighter.equipment_slots)

    def test_cannot_equip_if_slot_occupied(self):
        slot_holder = GameObject('x', self.level.log, None, None, 'take slot', item=Equipment(self.test_slot, []))
        slot_holder.item.use(self.slot_object, self.slot_object, self.level)
        self.assertFalse(self.sword.item.can_use(self.slot_object, self.slot_object, self.level))

    def test_cannot_equip_if_no_matching_slot(self):
        self.assertFalse(self.sword.item.can_use(self.no_slot_object, self.no_slot_object, self.level))

    def test_applies_effects(self):
        self.sword.item.use(self.slot_object, self.slot_object, self.level)
        self.assertEqual(self.slot_object.fighter.power, 20)
        self.assertEqual(len(self.slot_object.fighter.effect_list), 1)

        self.sword.item.use(self.slot_object, self.slot_object, self.level)
        self.assertEqual(self.slot_object.fighter.power, 10)
        self.assertEqual(len(self.slot_object.fighter.effect_list), 0)


class TestThrowingItem(unittest.TestCase):
    def setUp(self):
        self.level = LevelMap()
        self.level.add_faction('0', {})
        self.level.set_map([[LevelTile()] for _ in range(0, 5)])

        self.throwing_item = ThrowingItem(1000, 10)
        self.throwing = GameObject('1', self.level.log, None, None, 'item', item=self.throwing_item)
        self.inventory = Inventory(10, [self.throwing])

        self.target = GameObject('0', self.level.log, 0, 0, 'test', faction='0',
                                 fighter=Fighter(9999, 9999, defense=0, power=0, xp=0,
                                                 death_function=self.level.remove_object))
        self.level.add_object(self.target)

        self.user = GameObject('0', self.level.log, 4, 0, 'test', faction='1', inventory=self.inventory,
                               fighter=Fighter(9999, 9999, defense=0, power=0, xp=0,
                                               death_function=self.level.remove_object))

    def test_is_consumed_on_use(self):
        self.throwing.item.use(self.user, self.target, self.level)
        self.assertEqual(0, len(self.inventory))

    @mock.patch('random.randint', return_value=75)
    def test_does_damage(self, _):
        self.throwing.item.use(self.user, self.target, self.level)
        self.assertEqual(8999, self.target.fighter.hp)

    def test_respects_range(self):
        self.throwing_item.item_range = 1
        self.throwing.item.use(self.user, self.target, self.level)
        self.assertEqual(9999, self.target.fighter.hp)