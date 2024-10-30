import json

from blocks import Block

class MazeLoader:
    def __init__(self):
        self.path = "./assets/mazes.json"
        with open(self.path, 'r') as f:
            self.mazes = json.load(f)
    
    def get_maze_info(self, index):
        maze = self.mazes[index]
        return maze["height"], maze["width"], tuple(maze["size"])
    
    def get_maze_blocks(self, index):
        maze = self.mazes[index]
        return [Block.get_block(block_name) for block_name in maze["blocks"]]
