import json

import hunting.sim.items as items
from hunting.constants import *
from hunting.level.map import LevelTile, LevelMap
from hunting.sim.ai.ais import TestMonster
from hunting.sim.effects import PropertyEffect
from hunting.sim.entities import GameObject, Fighter


def parse_map(map_string):
    rows = map_string.splitlines()

    map_tiles = [[None for _ in rows] for _ in rows[0]]
    x = 0
    y = 0
    for line in rows:
        for i in line:
            if i == '.':
                map_tiles[x][y] = LevelTile(False, False)
            elif i == '#':
                map_tiles[x][y] = LevelTile(True, True)
            else:
                raise ValueError('Cannot parse character:', i)
            x += 1
        x = 0
        y += 1

    return map_tiles


def do_deploy(obj, deploy_state: dict):
    if deploy_state['strategy'] == 'eager':
        (x, y) = deploy_state['zones'].pop(0)
        obj.x = x
        obj.y = y


def parse_level(file):
    with open(file, 'r') as f:
        level = LevelMap()
        log = level.log

        def decode_fn(d: dict):
            if 'effect_type' in d:
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
                    if item['item_type'] == ITEM_THROWING:
                        item_component = items.ThrowingItem(**item)
                    elif item['item_type'] == ITEM_EQUIPMENT:
                        item_component = items.Equipment(**item)
                    else:
                        item_component = None
                else:
                    item_component = None

                game_object = GameObject(d['oid'], log, d.get('x'), d.get('y'), name=d['name'],  blocks=blocks,
                                         fighter=fighter_component, ai=ai_component, inventory=inventory_component,
                                         item=item_component)

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

        # Map info
        level.set_map(parse_map(parsed['map']))

        # Faction info
        for faction, faction_info in sorted(parsed['factions'].items()):
            faction_objects = faction_info.pop('objects')
            level.add_faction(faction, faction_info)

            deploy_info = parsed['deploy_info'][faction]

            for obj in faction_objects:
                obj.faction = faction
                level.add_object(obj)
                do_deploy(obj, deploy_info)

        # Complete
        level.finalize()
        return level
