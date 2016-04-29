import json
import unittest
import unittest.mock as mock

import hunting.level.parser as parser
import hunting.resources.files as res_files
from hunting.constants import *
from hunting.level.map import LevelMap, LevelTile
from hunting.sim.ai.ais import TestMonster, DummyAI
from hunting.sim.entities import GameObject, Fighter
from hunting.sim.runner import run_level, run_turn


class TestRunner(unittest.TestCase):
    def test_speed_system(self):
        level = LevelMap()
        level.add_faction(None, {})
        level.add_object(GameObject('1', level.log, 0, 0, 'slow', fighter=Fighter(1, 1, 1, 1, 1, speed=30),
                                    ai=DummyAI()))
        level.add_object(GameObject('2', level.log, 0, 0, 'fast', fighter=Fighter(1, 1, 1, 1, 1), ai=DummyAI()))
        for _ in range(4):
            run_turn(level)
        start_events = [e[OBJ_ID] for e in level.log.events if e[EVENT_TYPE] == BEGIN_TURN_EVENT]
        self.assertEqual(['1', '1', '1', '2'], start_events)

    def test_ends_if_one_faction(self):
        level = LevelMap()
        level.add_faction('1', {})
        level.add_object(GameObject('1', level.log, 0, 0, 'test', faction='1'))
        run_level(level)

        self.assertTrue(len(level.log.events) == 0)

    @mock.patch('random.randint', return_value=75)
    def test_runs_test_combat(self, _):
        level = LevelMap()
        level.set_map([[LevelTile()], [LevelTile()]])
        for x in [0, 1]:
            o = GameObject(x, level.log, x, 0, 'test', faction=x, ai=TestMonster(level),
                           fighter=Fighter(1, 1, defense=0, power=1, xp=0, death_function=level.remove_object))
            level.add_faction(x, {})
            level.add_object(o)
        run_level(level)
        event_types = [e[EVENT_TYPE] for e in level.log.events]

        self.assertEqual([BEGIN_TURN_EVENT, ATTACK_EVENT, TAKE_DAMAGE_EVENT, OBJECT_DESTRUCTION_EVENT, END_TURN_EVENT],
                         event_types)

    # This is not a unit test! However I'm not sure where to put it. So here it is.
    @mock.patch('random.randint', return_value=75)
    def test_level_json(self, _):
        level = parser.parse_level(res_files.test_test_level_json)
        run_level(level)

        with open(res_files.test_test_level_log_json, 'r') as f:
            self.assertEqual(level.log.events, json.load(f))
