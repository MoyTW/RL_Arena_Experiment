from hunting.level.map import LevelMap


def run_level(level: LevelMap):

    while len(level.get_factions()) > 1:
        for o in level._all_objects:
            o.ai.take_turn()

    return level.log