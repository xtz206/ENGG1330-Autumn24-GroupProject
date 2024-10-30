from blocks import player

class Spirit:
    def __init__(self, win, height, width, size):
        self.win = win
        self.height = height
        self.width = width
        self.size = size
        self.blocks = []
    
    def draw(self):
        raise NotImplementedError
    
    @staticmethod
    def resize(y, x, m, n):
        # resize the block to m * n
        return [(y * m + i, x * n + j) for i in range(m) for j in range(n)]
    
class Playground(Spirit):
    def __init__(self, win, height, width, size, blocks):
        super().__init__(win, height, width, size)
        self.blocks = blocks

    def draw(self):
        for index, block in enumerate(self.blocks):
            for y, x in self.resize(index // self.width, index % self.width, *self.size):
                self.win.insch(y, x, block.get_char(), block.get_color())

class Player(Spirit):
    def __init__(self, win, height, width, size):
        super().__init__(win, height, width, size)
        self.blocks = [player]
        self.y, self.x = self.height // 2, self.width // 2
    
    def move(self, dy, dx):
        self.y += dy
        self.x += dx
        
        # Exceeding the border
        if self.y < 0:
            self.y = 0
        elif self.y > self.height - 1:
            self.y = self.height - 1
        if self.x < 0:
            self.x = 0
        elif self.x > self.width - 1:
            self.x = self.width - 1

    def draw(self):
        block = self.blocks[0]
        for y, x in self.resize(self.y, self.x, *self.size):
            self.win.insch(y, x, block.get_char(), block.get_color())



