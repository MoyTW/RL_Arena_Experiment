import json

from hunting.constants import *
from hunting.level.map import LevelTile, LevelMap
from hunting.sim.ais import TestMonster
from hunting.sim.entities import GameObject, Fighter
from hunting.sim.effects import PropertyEffect
import hunting.sim.items as items


def parse_level(file):
    with open(file, 'r') as f:
        level = LevelMap()
        log = level.log

        def decode_fn(d: dict):
            if d.get('class', None) == 'tile':
                return LevelTile(blocks=d['blocks'], blocks_sight=d['blocks_sight'])
            elif 'effect_type' in d:
                if d['effect_type'] == EFFECT_TYPE_PROPERTY:
                    return PropertyEffect(**d)
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
                    inventory_component = items.Inventory(**inventory)
                else:
                    inventory_component = None

                if 'item' in d:
                    item = d['item']  # type: dict
                    if item['item_type'] == ITEM_TEST:
                        item_component = items.TestItem(**item)
                    elif item['item_type'] == ITEM_THROWING:
                        item_component = items.ThrowingItem(**item)
                    elif item['item_type'] == ITEM_EQUIPMENT:
                        item_component = items.Equipment(**item)
                    else:
                        item_component = None
                else:
                    item_component = None

                game_object = GameObject(d['oid'], log, d.get('x'), d.get('y'), name=d['name'],
                                         faction=d.get('faction'), blocks=blocks, fighter=fighter_component,
                                         ai=ai_component, inventory=inventory_component, item=item_component)

                # If it has an inventory and equipped items, equip the items
                if game_object.inventory is not None:  # TODO: This is frankly silly, especially the boolean flipping!
                    for i in game_object.inventory.get_equipment_items():
                        if i.item.is_equipped is True:
                            i.item.is_equipped = False
                            i.item.use(game_object, game_object, level)

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
