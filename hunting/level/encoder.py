import json
import hunting.sim.entities as entities


class GameObjectEncoder(json.JSONEncoder):
    def default(self, o):
        d = o.__dict__
        d.pop('owner', None)

        if isinstance(o, entities.GameObject):
            d.pop('log', None)
            d.pop('ai', None)
            return d
        elif isinstance(o, entities.Fighter):
            d.pop('death_function')
            return d
        elif isinstance(o, entities.ChangeableProperty):
            return {k: o.__dict__[k] for k in ['property_type', 'base']}
        else:
            return d


def encode_level(level):
    save_factions = [f for f in level.get_factions() if level.get_faction_info(f)['save'] is True]
    factions_to_objects = {f: level.get_objects_inside_faction(f) for f in save_factions}
    return json.dumps(factions_to_objects, cls=GameObjectEncoder, indent=2)
