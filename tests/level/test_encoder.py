import unittest
import json

import hunting.level.parser as parser
import hunting.level.encoder as encoder
import hunting.resources.files as res_files
import hunting.utils as utils


class TestEncoder(unittest.TestCase):
    def test_encoder(self):
        level = parser.parse_level(res_files.test_hero_versus_zero_json)
        encoded = encoder.encode_level(level)
        decoded = utils.sort_dicts(json.loads(encoded))
        with open(res_files.test_results_hero_versus_zero_json) as f:
            loaded = json.load(f)
            loaded['log'] = []
            expected = utils.sort_dicts(loaded)
        self.assertEqual(expected, decoded)
