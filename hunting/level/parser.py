import json

import hunting.sim.items as items
from hunting.constants import *
from hunting.level.map import LevelTile, LevelMap
from hunting.sim.ai.ais import TestMonster
from hunting.sim.effects import PropertyEffect
from hunting.sim.entities import GameObject, Fighter


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

        # Map info
        processed_map = [[LevelTile(bool(t[0]), bool(t[1])) for t in r] for r in parsed['map']]
        level.set_map(processed_map)

        # Faction info
        for faction, faction_info in parsed['factions'].items():
            faction_objects = faction_info.pop('objects')
            level.add_faction(faction, faction_info)
            for obj in faction_objects:
                level.add_object(obj)

        # Complete
        level.finalize()
        return level
