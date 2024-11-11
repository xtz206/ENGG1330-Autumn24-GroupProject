import curses

from blocks import get_block

class Sprite:
    """
    A base class for all sprite objects in the game.

    Attributes:
        win:    curses.window
            The window or screen where the sprite will be drawn.
        height: int
            The height of the maze.
        width:  int
            The width of the maze.
        blocks: list[Block]
            The blocks that make up the sprite.
    
    Methods:
        draw():
            An abstract interface for drawing the sprite on the window.
    """
    def __init__(self, win: curses.window, height: int, width: int, blocks: list["Block"]):
        self.win: curses.window = win
        self.height: int = height
        self.width: int = width
        self.blocks: list["Block"] = blocks
    
    def draw(self):
        """
        An abstract interface for drawing the sprite on the window.
        """
        raise NotImplementedError

class MovableSprite(Sprite):
    """
    A base class for all movable sprite objects in the game.

    Attributes:
        y: int
            The y-coordinate of the sprite.
        x: int
            The x-coordinate of the sprite.

    Methods:
        move(dy, dx):
            Moves the sprite by the given delta y and delta x.
    """
    def move(self, dy: int, dx: int):
        """
        Moves the sprite by the given delta y and delta x.

        Args:
            dy: int
                The change in the y-coordinate.
            dx: int
                The change in the x-coordinate.
        """
        self.y += dy
        self.x += dx

class Maze(Sprite):
    """
    A sprite representing a maze in the game.

    Attributes:
        start:  tuple[int, int]
            The starting point of the maze.
        end:    tuple[int, int]
            The ending point of the maze.
        player: Player
            The player object in the maze.
        chasers: list[Chaser]
            A list of chaser objects in the maze.
    
    Methods:
        set_player(player):
            Sets the player object in the maze.
        set_chasers(chaser):
            Sets the chaser objects in the maze.
        get_distance(y1, x1, y2, x2):
            Calculate the Manhattan distance between 2 points.
        get_neighbours(y, x):
            Returns a list of valid neighbouring points from a given coordinate.
        check_inrange(y, x):
            Check whether a position is within the maze boundaries.
        check_solid(y, x):
            Check whether a position is solid.
        check_route(y, x):
            Check whether a position is a valid route.
        check_player(y, x):
            Check whether a position is occupied by the player.
        check_chasers(y, x):
            Check whether a position is occupied by any chaser.
        check_box(y, x):
            Check whether a position contains a box.
        check_box_pushable(y, x, dy, dx):
            Check whether a box at the position can be pushed in the given direction.
        update_box(y, x, dy, dx, n):
            Updates the position of a box after pushing.
        check_bonus(y, x):
            Check whether a position contains a bonus.
        update_bonus(y, x):
            Updates the position of a bonus after being collected.
        draw():
            Draw the maze and its contents on the window.
    """
    def __init__(
        self, win: curses.window, height: int, width: int, 
        blocks: list["Block"], start: tuple[int, int], end: tuple[int, int]
    ):
        super().__init__(win, height, width, blocks)
        self.start: tuple[int, int] = start
        self.end: tuple[int, int] = end
    
    def set_player(self, player: "Player"):
        """
        Sets the player object in the maze.
        """
        self.player: "Player" = player

    def set_chasers(self, chasers: list["Chaser"]):
        """
        Sets the chaser objects in the maze.
        """
        self.chasers = chasers

    @staticmethod
    def get_distance(y1: int, x1: int, y2: int, x2: int):
        """
        Calculate the Manhattan distance between 2 points.
        """
        return abs(y1- y2) + abs(x1 - x2)

    def get_neighbours(self, y, x):
        """
        Returns a list of valid neighbouring points from a given coordinate.
        """
        neighbours = []
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for dy, dx in directions:
            ny, nx = y + dy, x + dx
            if self.check_route(ny, nx):
                neighbours.append((ny, nx))
        return neighbours

    def check_inrange(self, y, x):
        """
        Check whether a position is within the maze boundaries.
        """
        return 0 <= y < self.height and 0 <= x < self.width

    def check_solid(self, y, x):
        """
        Check whether a position is solid.
        """
        if not self.check_inrange(y, x):
            return False
        index = y * self.width + x
        return self.blocks[index].is_solid
    
    def check_route(self, y, x):
        """
        Check whether a position is a valid route.
        """
        return self.check_inrange(y, x) and not self.check_solid(y, x) and not self.check_chasers(y, x)

    def check_player(self, y, x):
        """
        Check whether a position is occupied by the player.
        """
        return (self.player.y, self.player.x) == (y, x)

    def check_chasers(self, y, x):
        """
        Check whether a position is occupied by any chaser.
        """
        for chaser in self.chasers:
            if (y, x) == (chaser.y, chaser.x):
                return True
        return False

    def check_box(self, y, x):
        """
        Check whether a position contains a box.
        """
        if not self.check_inrange(y, x):
            return False
        index = y * self.width + x
        return self.blocks[index] == get_block("box")

    def check_box_pushable(self, y, x, dy, dx):
        """
        Check whether a box at the position can be pushed in the given direction.
        """
        ny, nx = y + dy, x + dx
        return int(self.check_route(ny, nx)) # Only Push One Box
        if not self.check_inrange(ny, nx):
            return 0
        if self.check_route(ny, nx):
            return 1
        elif self.check_box(ny, nx):
            n = self.check_box_pushable(ny, nx, dy, dx)
            return n + 1 if n != 0 else 0
        else:
            return 0

    def update_box(self, y, x, dy, dx, n):
        """
        Updates the position of a box after pushing.
        """
        ny, nx = y + dy * n, x + dx * n
        index = y * self.width + x
        nindex = ny * self.width + nx
        self.blocks[index] = get_block("air")
        self.blocks[nindex] = get_block("box")

    def check_bonus(self, y, x):
        """
        Check whether a position contains a bonus.
        """
        index = y * self.width + x
        return self.blocks[index] == get_block("bonus")
    
    def update_bonus(self, y, x):
        """
        Updates the position of a bonus after being collected.
        """
        index = y * self.width + x
        if self.check_bonus(y, x):
            self.blocks[index] = get_block("air")

    def draw(self):
        """
        Draw the maze and its contents on the window.
        """
        for index, block in enumerate(self.blocks):
            y, x = divmod(index, self.width)
            block.draw(self.win, y, x)


class Player(MovableSprite):
    """
    A movable sprite representing a player in the game.

    Attributes:
        maze:   Maze
            The maze object that the player is on.
        score:  int
            The player's current score.
        step:   int
            The number of steps the player has taken.
    
    Methods:
        check_win()
            Checks if the player has reached the exit of the maze.
        check_lose()
            Checks if the player has been caught by any chaser.
        move(dy, dx):
            Moves the player in the given direction.
        draw():
            Draws the player at the coordinate on the window.
    """
    def __init__(
        self, win: curses.window, height: int, width: int, 
        blocks: list["Block"], maze: "Maze"
    ):
        super().__init__(win, height, width, blocks)
        self.y, self.x = maze.start
        self.maze: "Maze" = maze
        self.score: int = 1000 # BASIC SCORE
        self.step: int = 0

    def check_win(self):
        """
        Checks if the player has reached the exit of the maze.
        """
        return (self.y, self.x) == self.maze.end
    
    def check_lose(self):
        """
        Checks if the player has been caught by any chaser.
        """
        return self.maze.check_chasers(self.y, self.x)
    

    def move(self, dy, dx):
        """
        Moves the player in the given direction.

        Args:
            dy: int
                the change of y-coordinate.
            dx: int
                the change of x-coordinate.
        
        Returns:
            bool
                True if the move was successful, otherwise False.
        """
        ny, nx = self.y + dy, self.x + dx
        if dy == dx == 0:
            return False   
        elif self.maze.check_box(ny, nx):
            n = self.maze.check_box_pushable(ny, nx, dy, dx)
            if n == 0:
                return False
            else:
                self.maze.update_box(ny, nx, dy, dx, n)
        elif not self.maze.check_route(ny, nx):
            return False
        super().move(dy, dx)
        if self.maze.check_bonus(self.y, self.x):
            self.maze.update_bonus(self.y, self.x)
            self.score += 10000 # BONUS SCORE
        self.step += 1
        self.score -= 10 # STEP SCORE

        return True
        
    def draw(self):
        """
        Draws the player at the coordinate on the window.
        """
        block = self.blocks[0]
        block.draw(self.win, self.y, self.x)        


class Chaser(MovableSprite):
    """
    A movable sprite representing a chaser in the game.
    
    Attributes:
        maze:   Maze
            The maze object that the player is on.
        route:  list[tuple[int, int]]
            The route of the chaser.
    
    Methods:
        draw():
            Draws the chaser at the coordinate on the window.
    """
    def __init__(
        self, win: curses.window, height: int, width: int, 
        blocks: list["Blocks"], maze: "Maze", 
        route: list[tuple[int, int]]
    ):
        super().__init__(win, height, width, blocks)
        self.maze = maze
        self.route = route
        self.y, self.x = route[0]
    
    def draw(self):
        """
        Draws the chaser at the coordinate on the window.
        """
        block = self.blocks[0]
        block.draw(self.win, self.y, self.x)


class AutoChaser(Chaser):
    def __init__(
        self, win: curses.window, height: int, width: int, 
        blocks: list["Blocks"], maze: "Maze", 
        route: list[tuple[int, int]], player: "Player"
    ):
        """
        A subclass of Chaser representing Chasers which can search the shortest path to player by algorithm.

        Attributes:
            player:   Player
                The player which the chaser is chasing after.        
        
        Methods:
            search():
                Searches for the shortest path towards the player with the A* algorithm.
            move():
                Move the chaser along the path found by the search method,
                if the next route is valid route and not blocked by other chasers.
        """
        super().__init__(win, height, width, blocks, maze, route)
        self.player = player

    def search(self):
        """
        Searches for the shortest path towards the player with the A* algorithm.
        
        Returns:
            list[tuple[int, int]]
                A list of points which indicates the shortest path from the chaser to the player,
                if no path is found, returns empty list.
        """
        start = self.y, self.x
        end = self.player.y, self.player.x
        open_nodes = [start]
        closed_nodes = []
        prev_nodes = {start: None}
        costs = {start: 0}

        while open_nodes:
            open_nodes.sort(key=lambda node: costs[node] + self.maze.get_distance(*node, *end))
            open_node = open_nodes.pop(0)
            closed_nodes.append(open_node)

            # Path Found and Return
            if open_node == end:
                path = []
                curr = end
                while curr is not None:
                    path.append(curr)
                    curr = prev_nodes[curr]
                path.reverse()
                return path
            
            for neighbour_node in self.maze.get_neighbours(*open_node):
                if neighbour_node not in closed_nodes and neighbour_node not in open_nodes:
                    open_nodes.append(neighbour_node)
                    prev_nodes[neighbour_node] = open_node
                    cost = costs[open_node] + 1
                    if neighbour_node not in costs or cost < costs[neighbour_node]:
                        costs[neighbour_node] = cost
            
        # No Path Found
        return []

    def move(self):
        """
        Move the chaser along the path found by the search method,
        if the next route is valid route and not blocked by other chasers.
        """

        path = self.search()
        if len(path) < 2:
            return

        ny, nx = path[1]
        if not self.maze.check_route(ny, nx):
            return

        dy, dx = ny - self.y, nx - self.x
        super().move(dy, dx)


class FixedChaser(Chaser):
    """
    A subclass of Chaser representing Chasers which follows a fixed route.

    Attributes:
        step:   int
            The number of steps the chaser has taken.
    
    Methods:
        move():
            Move the chaser to the next route if it is valid.
        draw():
            Draws the chaser and the next step at the coordinate on the window.
    """
    def __init__(
        self, win: curses.window, height: int, width: int, 
        blocks: list["Blocks"], maze: "Maze", 
        route: list[tuple[int, int]]
    ):
        super().__init__(win, height, width, blocks, maze, route)
        self.step = 1

    def move(self):
        """
        Move the chaser to the next route if it is valid.
        """
        ny, nx = self.route[self.step % len(self.route)]
        if not self.maze.check_route(ny, nx):
            return
        
        dy, dx = ny - self.y, nx - self.x
        self.step += 1
        super().move(dy, dx)
    
    def draw(self):
        """
        Draws the chaser and the next step at the coordinate on the window.
        """
        ny, nx = self.route[self.step % len(self.route)]
        if self.maze.check_route(ny, nx) and not self.maze.check_player(ny, nx):
            block = self.blocks[1]
            block.draw(self.win, ny, nx)
        super().draw()

