import json
from src.level_map import LevelTile, LevelMap
from src.ais import TestMonster
from src.entities import GameObject, Fighter


def parse_level(file):
    with open(file, 'r') as f:
        level = LevelMap()

        def decode_fn(d: dict):
            if d.get('class', None) == 'tile':
                return LevelTile(blocks=d['blocks'], blocks_sight=d['blocks_sight'])
            elif 'id' in d:
                # Generate the AI
                if 'ai' in d:
                    ai_component = TestMonster(level)
                else:
                    ai_component = None

                # Generate the Fighter
                if 'fighter' in d:
                    fighter = d['fighter']
                    fighter_component = Fighter(**fighter)
                    fighter_component.death_function = level.remove_object  # TODO: Allow setting of death fn
                else:
                    fighter_component = None

                game_object = GameObject(d['x'], d['y'], name=d['name'], faction=d['faction'], blocks=True,
                                         fighter=fighter_component, ai=ai_component)
                return game_object

            else:
                return d

        parsed = json.load(f, object_hook=decode_fn)
        level.width = parsed['width']
        level.height = parsed['height']
        level.set_map(parsed['map'])
        for obj in parsed['all_objects']:
            level.add_object(obj)
        level.finalize()
        return level
