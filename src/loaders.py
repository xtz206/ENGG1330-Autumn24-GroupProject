import curses
import json

import blocks
import display

class Loader:
    def __init__(self, path):
        self.path = path
        
    def load(self):
        with open(self.path, 'r') as f:
            self.data = json.load(f)


class MultiLoader(Loader):
    def set_index(self, index):
        self.index = index
    
    def get_basic_info(self):
        raise NotImplementedError
    
    def get_resource_info(self):
        raise NotImplementedError


class ColorLoader(Loader):
    def load(self):
        with open(self.path, 'r') as f:
            self.data = json.load(f)

        color_names = {
            "red": curses.COLOR_RED,
            "green": curses.COLOR_GREEN,
            "blue": curses.COLOR_BLUE,
            "yellow": curses.COLOR_YELLOW,
            "cyan": curses.COLOR_CYAN,
            "magenta": curses.COLOR_MAGENTA,
            "white": curses.COLOR_WHITE,
            "black": curses.COLOR_BLACK
        }

        for index, (fg, bg) in enumerate(self.data):
            curses.init_pair(index + 1, color_names[fg], color_names[bg])


class BlockLoader(Loader):
    def load(self):
        with open(self.path, 'r') as f:
            self.data = json.load(f)
        
        keys = self.data["default"].keys()
        default_data = self.data["default"]

        for block_data in self.data["blocks"]:
            block_info = {key: block_data.get(key, default_data.get(key)) for key in keys}
            blocks.Block(**block_info)


class MazeLoader(MultiLoader): 
    def get_basic_info(self):
        maze_data = self.data[self.index]
        height = maze_data["height"]
        width = maze_data["width"]
        return height, width

    def get_resource_info(self):
        maze_data = self.data[self.index]
        start = tuple(maze_data["start"])
        end = tuple(maze_data["end"])
        block_names = maze_data["block_names"]
        return {
            "blocks": [blocks.get_block(block_name) for block_name in block_names], 
            "start": start,
            "end": end
        }


class MenuLoader(MultiLoader):
    def get_basic_info(self):
        menu_data = self.data[self.index]
        return menu_data["height"], menu_data["width"]

    def get_resource_info(self):
        menu_data = self.data[self.index]
        return [display.Text(**text_data) for text_data in menu_data["texts"]]


