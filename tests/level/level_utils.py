from hunting.level.map import LevelMap, LevelTile

def generate_5x3_long_c():
    level_map = LevelMap([[LevelTile() for _ in range(0, 3)] for _ in range(0, 5)])

    for x in range(1, 5):
        level_map[x][1].blocks = True

    return level_map