import uuid

import tdl

import hunting.sim.parser as parser
from hunting.display.render import Renderer

print(uuid.uuid4())

main_width = 80
main_height = 60
level_width = 80
level_height = 50

main_console = tdl.init(main_width, main_height, 'TDL Test')

(level, log) = parser.parse_level('resources/test_level.json')

for _ in range(100):
    for o in level._all_objects:
        o.ai.take_turn()

print(log.to_json_string())

# This is not very elegant, but the level used for doing the calculations is destructive, so we need to get a fresh
# from-json copy for rendering.
(scratch_level, _) = parser.parse_level('resources/test_level.json')

renderer = Renderer(main_console, level_width, level_height)
renderer.render_all(level=scratch_level)

for le in log._log:
    renderer.render_event(level=scratch_level, event=le)
