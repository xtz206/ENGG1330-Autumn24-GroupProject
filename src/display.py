import curses

class Displayer:
    def __init__(self, screen):
        self.screen = screen
        self.wins = {}

    def create_win(self, name, height, width, size):
        window_height = height * size[0] + 2
        window_width = width * size[1] + 2
        screen_height, screen_width = self.screen.getmaxyx()
        window_origin_y = (screen_height - window_height) // 2
        window_origin_x = (screen_width - window_width) // 2
        self.wins[name] = curses.newwin(window_height, window_width, window_origin_y, window_origin_x)
        return self.wins[name]

    def display_game(self, displaying_sprites):
        self.wins["game"].erase()
        for displaying_sprite in displaying_sprites:
            displaying_sprite.draw()
        self.wins["game"].refresh()

    def display_start(self):
        # TODO: Complete the func
        width, height = self.win.getmaxyx()
        # self.win.border(*self.borders)
        
