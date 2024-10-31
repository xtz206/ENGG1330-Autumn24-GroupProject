import curses

class Block:
    blocks = {}

    def __init__(self, name, size, char, color, is_solid, is_pushable):
        self.name = name
        self.size = size
        self.char = char
        self.color = color
        self.is_solid = is_solid
        self.is_pushable = is_pushable
        Block.blocks[self.name] = self
    
    def draw(self, win, y, x):
        for window_y, window_x in self.transform(y, x):
            win.addch(window_y, window_x, self.char, curses.color_pair(self.color))

    def transform(self, y, x):
        common_height, common_width = get_block_size()
        block_height, block_width = self.size
        return [
            (y * common_height + i + 1, x * common_width + j + 1) 
            for i in range(block_height) for j in range(block_width)
        ]


def get_block(name):
    return Block.blocks[name]

def get_block_size():
    max_size_y = max_size_x = 0
    for block in Block.blocks.values():
        max_size_y = max(max_size_y, block.size[0])
        max_size_x = max(max_size_x, block.size[1])
    return max_size_y, max_size_x


