import curses

class Text:
    def __init__(self, content, line, align=False, indent=0, variable=False, color=0):
        self.content = content
        self.line = line
        self.align = align
        self.indent = indent
        self.variable = variable
        self.color = color

    def fillin_variable(self, fillins):
        self.content = self.content % fillins

    def draw(self, win):
        height, width = win.getmaxyx()
        y = self.line
        x = ((width - len(self.content)) // 2 if self.align else 0) + self.indent
        win.addstr(y, x, self.content, curses.color_pair(self.color))


class Displayer:
    def __init__(self, screen):
        self.screen = screen
        self.win = None

    def create_win(self, height, width, size=(1,1)):
        window_height = height * size[0] + 2
        window_width = width * size[1] + 2
        screen_height, screen_width = self.screen.getmaxyx()
        window_origin_y = (screen_height - window_height) // 2
        window_origin_x = (screen_width - window_width) // 2
        self.win = curses.newwin(window_height, window_width, window_origin_y, window_origin_x)
        return self.win

    def display_game(self, displaying_sprites):
        self.win.erase()
        for displaying_sprite in displaying_sprites:
            displaying_sprite.draw()
        self.win.refresh()

    def display_start(self, texts):
        self.win.erase()
        for text in texts:
            text.draw(self.win)
        self.win.refresh()
    
    def display_end(self, texts, results):
        self.win.erase()
        results = iter(results)
        for text in texts:
            if text.variable:
                result = next(results)
                text.fillin_variable(result)
            text.draw(self.win)
        self.win.refresh()


