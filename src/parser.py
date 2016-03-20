import json
from src.level_map import LevelTile, LevelMap
from src.ais import TestMonster
from src.entities import GameObject, Fighter
from src.level_log import LevelLog
from src.items import Inventory, TestItem, ThrowingItem

def parse_level(file):
    with open(file, 'r') as f:
        level = LevelMap()
        log = LevelLog()

        def decode_fn(d: dict):
            if d.get('class', None) == 'tile':
                return LevelTile(blocks=d['blocks'], blocks_sight=d['blocks_sight'])
            elif 'oid' in d:
                blocks = False

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
                    blocks = True
                else:
                    fighter_component = None

                # Fill the Inventory
                if 'inventory' in d:
                    inventory = d['inventory']
                    inventory_component = Inventory(**inventory)
                else:
                    inventory_component = None

                if 'item' in d:
                    item = d['item']  # type: dict
                    if item['class'] == 'TestItem':
                        item.pop('class')
                        item_component = TestItem(**item)
                    elif item['class'] == 'ThrowingItem':
                        item.pop('class')
                        item_component = ThrowingItem(**item)
                    else:
                        item_component = None
                else:
                    item_component = None

                game_object = GameObject(d['oid'], log, d.get('x'), d.get('y'), name=d['name'],
                                         faction=d.get('faction'), blocks=blocks, fighter=fighter_component,
                                         ai=ai_component, inventory=inventory_component, item=item_component)
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
        return level, log
