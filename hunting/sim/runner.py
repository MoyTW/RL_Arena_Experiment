from hunting.level.map import LevelMap


def run_turn(level: LevelMap):
    level.pass_time_to_next_event()
    objects_moving = level.get_objects_moving_now()
    for o in [o for o in objects_moving if o.ai is not None]:  # TODO: Don't keep just because you think it's hilarious
        o.ai.take_turn()


def run_level(level: LevelMap):
    while len(level.get_factions()) > 1:
        run_turn(level)

    return level.log
