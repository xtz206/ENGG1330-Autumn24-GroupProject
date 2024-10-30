import curses

class Block:
    blocks = {} # all kinds of blocks 

    def __init__(self, name, char=" "):
        self.name = name
        self.char = char
        self.color = None
        Block.blocks[self.name] = self

    def get_char(self):
        return self.char

    def set_color(self, color):
        self.color = color

    def get_color(self):
        if self.color is None:
            raise ValueError("Must Set Color First")
        return self.color

    @staticmethod
    def get_block(name):
        return Block.blocks[name]

colors = {
    "air": (curses.COLOR_BLACK, curses.COLOR_WHITE),
    "wall": (curses.COLOR_BLACK, curses.COLOR_YELLOW),
    "player" : (curses.COLOR_GREEN, curses.COLOR_WHITE)
}

air = Block("air")
wall = Block("wall")
player = Block("player", "@")
