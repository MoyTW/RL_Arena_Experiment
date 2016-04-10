import random


def d100():
    return random.randint(1, 100)


def sort_dicts(obj):
    if isinstance(obj, dict):
        return sorted((k, sort_dicts(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return (sort_dicts(x) for x in obj)
    else:
        return obj
