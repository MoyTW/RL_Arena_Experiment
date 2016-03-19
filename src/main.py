import tdl
import time
from src.tdl_constants import *
from src.level_map import LevelMap
from src.render import Renderer

main_width = 80
main_height = 60
level_width = 80
level_height = 50

main_console = tdl.init(main_width, main_height, 'TDL Test')

level = LevelMap(80, 50)
renderer = Renderer(main_console, level_width, level_height)
renderer.render_all(level=level)

close_window = False
while not close_window:
    time.sleep(1)

    for e in tdl.event.get():
        if e.type == TDL_KEY_DOWN:
            close_window = True

    renderer.clear(level=level)

    for o in level._all_objects:
        o.ai.take_turn()

    renderer.render_all(level=level)
