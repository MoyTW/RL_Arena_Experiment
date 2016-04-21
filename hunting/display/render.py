import tdl
import time
import hunting.constants as c


class Renderer:
    def __init__(self, main_console=None, level_display_width=c.SCREEN_WIDTH, level_display_height=c.SCREEN_HEIGHT):
        if main_console is None:
            self.main_console = tdl.init(level_display_width, level_display_height, 'From Renderer Default Constructor')
        else:
            self.main_console = main_console
        self.level_display_width = level_display_width
        self.level_display_height = level_display_height
        self._level_console = tdl.Console(level_display_width, level_display_height)

    def _render_level(self, con, level):
        for x in range(level.width):
            for y in range(level.height):
                if level[x][y].blocks is not False:
                    self._level_console.draw_rect(x, y, 1, 1, None, bg=[120, 0, 50])
                else:
                    self._level_console.draw_rect(x, y, 1, 1, None, bg=[30, 255, 30])

        # TODO: This is pretty hacky!
        i = 1
        for o in level._all_objects:
            if o.faction == '1':  # TODO: Better faction implementation!
                color = [255, 0, 0]
            else:
                color = [0, 0, 255]
            self._level_console.draw_char(o.x, o.y, i, color)
            i += 1

        con.blit(self._level_console)

    def render_all(self, level):
        self._render_level(self.main_console, level)
        tdl.flush()

    def clear(self, level):
        for o in level._all_objects:
            self._level_console.draw_char(o.x, o.y, ' ')

    def render_event(self, level, event):
        if event[c.EVENT_TYPE] == c.MOVEMENT_EVENT:
            # Clear previous location
            self._level_console.draw_char(event[c.MOVEMENT_PREV_X], event[c.MOVEMENT_PREV_Y], ' ', bg=[0, 15, 7])

            # Retrieve faction and color
            o = level.get_object_by_id(event[c.OBJ_ID])
            if o.faction == '1':  # TODO: Better faction implementation!
                color = [255, 0, 0]
            else:
                color = [0, 0, 255]

            self._level_console.draw_char(event[c.OBJ_X], event[c.OBJ_Y], o.faction, fg=color)

        elif event[c.EVENT_TYPE] == c.OBJECT_DESTRUCTION_EVENT:
            self._level_console.draw_char(event[c.OBJ_X], event[c.OBJ_Y], ' ', bg=[0, 15, 7])

        # Render
        self.main_console.blit(self._level_console)
        tdl.flush()


def visualize(level, show_time=1):
    Renderer().render_all(level)
    time.sleep(show_time)