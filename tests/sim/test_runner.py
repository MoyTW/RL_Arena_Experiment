import unittest
import hunting.resources as resources
from hunting.constants import *
from hunting.level.map import LevelMap, LevelTile
from hunting.sim.ais import TestMonster
from hunting.sim.entities import GameObject, Fighter
from hunting.sim.runner import run_level
import hunting.level.parser as parser
import json


class TestRunner(unittest.TestCase):
    def test_ends_if_one_faction(self):
        level = LevelMap()
        level.add_object(GameObject('1', level.log, 0, 0, 'test', faction='1'))
        log = run_level(level)

        self.assertTrue(len(log.events) == 0)

    def test_runs_test_combat(self):
        level = LevelMap()
        level.set_map([[LevelTile()], [LevelTile()]])
        for x in [0, 1]:
            o = GameObject(x, level.log, x, 0, 'test', faction=x, ai=TestMonster(level),
                           fighter=Fighter(hp=1, defense=0, power=1, xp=0, death_function=level.remove_object))
            level.add_object(o)
        log = run_level(level)
        event_types = [e[EVENT_TYPE] for e in log.events]

        self.assertEqual([BEGIN_TURN_EVENT, ATTACK_EVENT, TAKE_DAMAGE_EVENT, OBJECT_DESTRUCTION_EVENT, END_TURN_EVENT],
                         event_types)

    # This is not a unit test! However I'm not sure where to put it. So here it is.
    def test_level_json(self):
        level = parser.parse_level(resources.test_level_json)
        run_level(level)

        with open(resources.test_level_log_json, 'r') as f:
            self.assertEqual(level.log.events, json.load(f))
