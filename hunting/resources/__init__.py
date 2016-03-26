import os

_this_file = os.path.realpath(__file__)
_res_dir = os.path.split(_this_file)[0]

# Ideally these could be auto-built so you won't have to add each new file manually!
test_level_json = os.path.join(_res_dir, 'test_level.json')
test_level_log_json = os.path.join(_res_dir, 'test_level_log.json')
