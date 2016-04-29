import os

_this_file = os.path.realpath(__file__)
_res_dir = os.path.split(_this_file)[0]


def get_full_path(path):
    full = os.path.join(_res_dir, path)
    if os.path.isfile(full):
        return full
    else:
        return None

test_level_json = get_full_path('test/test_level.json')
test_level_log_json = get_full_path('test/test_level_log.json')
