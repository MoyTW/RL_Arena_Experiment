import unittest
import json

import hunting.level.parser as parser
import hunting.level.encoder as encoder
import hunting.resources as resources
import hunting.utils as utils


class TestEncoder(unittest.TestCase):
    def test_encoder(self):
        level = parser.parse_level(resources.get_full_path('test/hero_versus_zero.json'))
        encoded = encoder.encode_level(level)
        decoded = utils.sort_dicts(json.loads(encoded))
        with open(resources.get_full_path('test/results/hero_versus_zero.json')) as f:
            expected = utils.sort_dicts(json.load(f))
        self.assertEqual(expected, decoded)