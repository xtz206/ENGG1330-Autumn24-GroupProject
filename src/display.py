class Displayer:
    def __init__(self, win):
        self.win = win

    def display_game(self, displaying_sprites):
        self.win.clear()
        for displaying_sprite in displaying_sprites:
            displaying_sprite.draw()
        self.win.refresh()

    def display_start(self):
        # TODO: Complete the func
        width, height = self.win.getmaxyx()
        # self.win.border(*self.borders)
        
