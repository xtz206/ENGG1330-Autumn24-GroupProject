import curses

class Block:
    """
    A class to represent a block in the maze.

    Attributes:
        blocks: dict[str, Block]
            A class attribute which stores all block instances by their name.
        name:   str
            The name of the block.
        size:   tuple[int, int]
            The size of the block in terms of height and width.
        char:   str
            The character which represents the block.
        color:  int
            The color of the block, which is an index of the color pair.
        is_solid:   bool
            A boolean value which shows whether the block is solid or not.
        
    Methods:
        draw(win, y, x)
            Draws the block on the given window at the given coordinates.
        transform(y, x)
            Transforms the block coordinate to window coordinates.
    """


    blocks: dict[str, "Block"] = {}

    def __init__(self, name: str, size: tuple[int, int], char: str, color: int, is_solid: bool):
        self.name: str = name
        self.size: tuple[int, int] = size
        self.char: str = char
        self.color: int = color
        self.is_solid: bool = is_solid
        Block.blocks[self.name] = self
    
    def draw(self, win: curses.window, y: int, x: int) -> None:
        """
        Draws the block on the given window at the given coordinates.

        Args:
            win:    curses.window
                The curses window where the block will be drawn.
            y:      int
                The y-coordinate where the block will be drawn.
            x:      int
                The x-coordinate where the block will be drawn.
        """
        for window_y, window_x in self.transform(y, x):
            win.addch(window_y, window_x, self.char, curses.color_pair(self.color))

    def transform(self, y: int, x: int) -> list[tuple[int, int]]:
        """
        Transforms the block coordinate to window coordinates.

        Args:
            y:  int
                The y-coordinate of the block
            x:  int
                The x-coordinate of the block
        
        Returns:
            list[tuple[int, int]]: A list of tuple representing the window coordinates.
        """
        common_height, common_width = get_block_size()
        block_height, block_width = self.size
        return [
            (y * common_height + i + 1, x * common_width + j + 1) 
            for i in range(block_height) for j in range(block_width)
        ]


def get_block(name: str) -> "Block":
    """
    Get the block instance by its name.

    Args: 
        name:   str
            The name of the block
    
    Returns:
        Block:  The Block instance 
    """
    return Block.blocks[name]

def get_block_size() -> tuple[int, int]:
    """
    Get the maximum block size

    Returns:
        tuple[int, int]: The maximum size in terms of height and width
    
    """
    max_size_y = max_size_x = 0
    for block in Block.blocks.values():
        max_size_y = max(max_size_y, block.size[0])
        max_size_x = max(max_size_x, block.size[1])
    return max_size_y, max_size_x

