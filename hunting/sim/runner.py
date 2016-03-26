from hunting.level.map import LevelMap


def run_turn(level: LevelMap):
    for o in level._all_objects:
            o.ai.take_turn()


def run_level(level: LevelMap):
    while len(level.get_factions()) > 1:
        run_turn(level)

    return level.log
