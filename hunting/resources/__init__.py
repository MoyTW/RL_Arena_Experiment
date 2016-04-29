import os


_this_file = os.path.realpath(__file__)
_res_dir = os.path.split(_this_file)[0]


def get_full_path(path):
    full = os.path.join(_res_dir, path)
    if os.path.isfile(full):
        return full
    else:
        return None

# TODO: This kludged-together code generation is not a good substitute for a real method of managing resources.
# TODO: Also it gets built every time on eval. Silly!
file_tree = list(os.walk(_res_dir))
files_in_dirs = [[d[0] + '/' + f for f in d[2] if f.endswith('.json')] for d in file_tree]
files = [x for y in files_in_dirs for x in y]  # No 'flatten' huh?


def get_name_without_suffix(path):
    return path[len(_res_dir) + 1:].replace('/', '_').replace('.', '_')

file_listing = ''
for f in files:
    file_listing += get_name_without_suffix(path=f) + ' = "' + f + '"\n'

with open(os.path.join(_res_dir, 'files.py'), 'w') as listing_file:
    listing_file.write(file_listing)
