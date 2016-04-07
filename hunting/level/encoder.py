import json
from hunting.sim.entities import *
from hunting.sim.items import Inventory


class GameObjectEncoder(json.JSONEncoder):
    def default(self, o):
        d = o.__dict__
        d.pop('owner', None)

        if isinstance(o, GameObject):
            d.pop('log', None)
            d.pop('ai', None)
            return d
        elif isinstance(o, Fighter):
            d.pop('death_function')
            return d
        elif isinstance(o, ChangeableProperty):
            return {k: o.__dict__[k] for k in ['property_type', 'base']}
        else:
            return d