import hunting.level.parser as parser
from hunting.level.map import LevelMap, LevelTile


def gen_level_with_string(map_string: str):
    return LevelMap(parser.parse_map(map_string))


def set_level_to_string(level: LevelMap, map_string: str):
    level.set_map(parser.parse_map(map_string))
