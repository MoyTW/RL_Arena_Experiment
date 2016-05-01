import unittest

import hunting.constants as c
from hunting.sim.effects import PropertyEffect
from hunting.level.map import LevelMap
from hunting.sim.entities import GameObject, Fighter
import hunting.sim.items.equipment as equipment


class TestEquipment(unittest.TestCase):
    def setUp(self):
        self.level = LevelMap()

        self.test_id = '1'
        self.test_slot = 'test slot'
        self.effect = PropertyEffect(property_type=c.PROPERTY_POWER, value=10)
        self.sword = GameObject(self.test_id, self.level.log, None, None, 'sword',
                                item=equipment.Equipment(slot=self.test_slot, effects=[self.effect]))
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
        slot_holder = GameObject('x', self.level.log, None, None, 'take slot',
                                 item=equipment.Equipment(self.test_slot, []))
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