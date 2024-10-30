import curses

class Text:
    def __init__(self, content, align, color):
        self.content = content
        self.align = align
        self.color = color

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
        height, width = self.win.getmaxyx()
        for index, text in enumerate(texts):
            content = text.content
            align = text.align
            color = curses.color_pair(text.color)

            if align == 0:
                y = index
                x = (width - len(content)) // 2
                self.win.addstr(y, x, content)

        self.win.refresh()


