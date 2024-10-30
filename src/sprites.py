class Sprite:
    def __init__(self, win, height, width, blocks):
        self.win = win
        self.height = height
        self.width = width
        self.blocks = blocks
    
    def draw(self):
        raise NotImplementedError


class Maze(Sprite):
    def __init__(self, win, height, width, blocks, start, end):
        super().__init__(win, height, width, blocks)
        self.start = start
        self.end = end

    def get_start(self):
        return self.start
    
    def get_end(self):
        return self.end

    def check_solid(self, y, x):
        index = y * self.width + x
        return self.blocks[index].is_solid
    
    def draw(self):
        for index, block in enumerate(self.blocks):
            y, x = divmod(index, self.width)
            block.draw(self.win, y, x)


class Player(Sprite):
    def __init__(self, win, height, width, blocks, maze):
        super().__init__(win, height, width, blocks)
        self.y, self.x = maze.get_start()
        self.maze = maze   

    def move(self, dy, dx):
        self.y += dy
        self.x += dx

        # border check
        if self.y < 0:
            self.y = 0
        elif self.y > self.height - 1:
            self.y = self.height - 1
        elif self.x < 0:
            self.x = 0
        elif self.x > self.width - 1:
            self.x = self.width - 1
        
        # solid block check
        elif self.maze.check_solid(self.y, self.x):
            self.y -= dy
            self.x -= dx
    
    def check_win(self):
        return self.y, self.x == self.maze.get_end()
    
    def check_lose(self):
        # TODO: Check Chaser
        return False

    def draw(self):
        block = self.blocks[0]
        block.draw(self.win, self.y, self.x)


class Chaser(Sprite):
    def __init__(self):
        pass
