import tdl
from src.tdl_constants import *

close_window = False

main_console = tdl.init(80, 60, 'Hello World!')

text_console = tdl.Console(80, 60)
text_console.move(35, 30)
text_console.set_colors([0, 255, 0])
text_console.print_str('Hello World!')

text_console.move(30, 32)
text_console.set_colors([255, 0, 0])
text_console.print_str('Press any key to exit.')

main_console.blit(text_console, 0, 0)
tdl.flush()

while not close_window:
    for e in tdl.event.get():
        if e.type == TDL_KEY_DOWN:
            close_window = True
