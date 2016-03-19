import tdl


class Renderer:
    def __init__(self, main_console, level_display_width, level_display_height):
        self.main_console = main_console
        self.level_display_width = level_display_width
        self.level_display_height = level_display_height
        self._level_console = tdl.Console(level_display_width, level_display_height)

    def _render_level(self, con, level):
        for x in range(self.level_display_width):
            for y in range(self.level_display_height):
                if level[x][y].blocks is not False:
                    self._level_console.draw_rect(x, y, 1, 1, None, bg=[255, 255, 255])
                else:
                    self._level_console.draw_rect(x, y, 1, 1, None, bg=[0, 15, 7])

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