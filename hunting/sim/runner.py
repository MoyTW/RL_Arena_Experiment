from hunting.level.map import LevelMap


def run_turn(level: LevelMap):
    level.pass_time_to_next_event()
    objects_moving = level.get_objects_moving_now()
    for o in [o for o in objects_moving if o.ai is not None]:  # TODO: Don't keep just because you think it's hilarious
        if not o.fighter.destroyed:
            o.ai.take_turn()


def continue_run(level: LevelMap):
    counts = [len(level.get_objects_inside_faction(f)) for f in level.get_factions()]
    return len(counts) > 1 and all(c > 0 for c in counts)


def run_level(level: LevelMap):
    while continue_run(level):
        run_turn(level)
