import json
import hunting.sim.entities as entities


def remove_unused_keys(d: dict):
    """ Mutates a dictionary to remove keys which map to None """
    empties = [k for k in d if d[k] is None or d[k] == []]
    for e in empties:
        d.pop(e)


class GameObjectEncoder(json.JSONEncoder):
    def default(self, o):
        d = o.__dict__  # type: dict
        d.pop('owner', None)

        if isinstance(o, entities.GameObject):
            d.pop('x', None)
            d.pop('y', None)
            d.pop('log', None)
            d.pop('faction', None)
            # TODO: Clunky and awkard; don't really want to rely on *class names* of all things. Should be a mapping!
            if d.get('ai', None) is not None:
                d['ai'] = o.ai.__class__.__name__
            d.pop('blocks', None)
            remove_unused_keys(d)

            return d
        elif isinstance(o, entities.Fighter):
            d.pop('death_function')
            d.pop('_time_until_turn')
            d.pop('destroyed')

            if len(d['equipment_slots']) == 0:
                d.pop('equipment_slots')
            if len(d['effect_list']) == 0:
                d.pop('effect_list')

            changeables = [[k, v.__dict__] for k, v in d.items() if isinstance(v, entities.ChangeableProperty)]
            for dict_key, changable_dict in changeables:
                d.pop(dict_key)
                d[changable_dict['property_type']] = changable_dict['base']

            hp = d.pop('_hp')
            d['hp'] = hp
            stamina = d.pop('_stamina')
            d['stamina'] = stamina

            remove_unused_keys(d)

            return d
        elif isinstance(o, entities.ChangeableProperty):
            return {k: o.__dict__[k] for k in ['property_type', 'base']}
        else:
            return d


def encode_level(level):
    save_factions = {f: level.get_faction_info(f) for f in level.get_factions()
                     if level.get_faction_info(f)['save'] is True}

    for f in save_factions:
        save_factions[f]['objects'] = level.get_objects_inside_faction(f)

    output = {'log': level.log.events,
              'factions': save_factions}

    return json.dumps(output, cls=GameObjectEncoder, indent=2)
