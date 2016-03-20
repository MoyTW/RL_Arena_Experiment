import tdl
import time
from src.tdl_constants import *
from src.render import Renderer
import src.parser as parser

main_width = 80
main_height = 60
level_width = 80
level_height = 50

main_console = tdl.init(main_width, main_height, 'TDL Test')

(level, log) = parser.parse_level('../resources/test_level.json')
for _ in range(100):
    for o in level._all_objects:
        o.ai.take_turn()

print(log.to_json_string())

# This is not very elegant, but the level used for doing the calculations is destructive, so we need to get a fresh
# from-json copy for rendering.
(scratch_level, _) = parser.parse_level('../resources/test_level.json')

renderer = Renderer(main_console, level_width, level_height)
renderer.render_all(level=scratch_level)

close_window = False
while not close_window:
    for le in log._log:
        renderer.render_event(level=scratch_level, event=le)

    for e in tdl.event.get():
            if e.type == TDL_KEY_DOWN:
                close_window = True
