import uuid

import tdl

import hunting.level.parser as parser
import hunting.level.encoder as encoder
from hunting.display.render import Renderer
from hunting.sim.runner import run_level

print(uuid.uuid4())

main_width = 80
main_height = 60
level_width = 80
level_height = 50

main_console = tdl.init(main_width, main_height, 'TDL Test')

level = parser.parse_level('resources/test_level.json')

run_level(level)

print(level.log.to_json_string())

# This is not very elegant, but the level used for doing the calculations is destructive, so we need to get a fresh
# from-json copy for rendering.
scratch_level = parser.parse_level('resources/test_level.json')

renderer = Renderer(main_console, level_width, level_height)
renderer.render_all(level=scratch_level)

for event in level.log.events:
    renderer.render_event(level=scratch_level, event=event)

print(encoder.encode_level(level))
