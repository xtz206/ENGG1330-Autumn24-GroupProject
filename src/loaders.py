import curses
import json
from typing import Union, Any

import blocks
import display

class Loader:
    """
    A class to load data from a specific file path.
    
    Attributes:
        path:   str
            The path to the file to be loaded.
        data:   Union[dict, list]
            The raw data loaded from the file.
    
    Methods:
        load():
            Loads the raw data from the file by the given path attribute.

    """
    def __init__(self, path: str):
        self.path: str = path
        
    def load(self):
        """
        Loads the raw data from the file by the given path attribute.
        """
        with open(self.path, 'r') as f:
            self.data: Union[dict, list] = json.load(f)


class MultiLoader(Loader):
    """
    A subclass of Loader which provides an interface for setting index and get basic and resource information.
    This class should be extended by other classes which implement the details of the methods.

    Methods:
        set_index(index):
            Sets the index for the loader.
        get_basic_info():
            Abstract method to get basics.
        get_resource_info():
            Abstract method to get resources.
    """
    def set_index(self, index: Union[int, str]):
        """
        Sets the index for the loader.

        Args:
            index: Union[int, str]
        """
        self.index: Union[int, str] = index
    
    def get_basics(self):
        """
        Abstract method to get basics.
        """
        raise NotImplementedError
    
    def get_resources(self):
        """
        Abstract method to get resources.
        """
        raise NotImplementedError


class ColorLoader(Loader):
    """
    A subclass of Loader that loads color configuration from a JSON file.
    and initializes color pairs

    Methods:
        load():
            Loads the JSON file and parses the color configurations,
            and initializes color pairs using curses.init_pair.
    """
    def load(self):
        """
        Loads the JSON file and parses the color configurations,
        and initializes color pairs using curses.init_pair.

        Steps:
            1. Load the JSON file and store the data in self.data.
            2. Create color_names dict which maps color names to curses color constants.
            3. Iterate over the list of color pairs and initialize color pairs.
        """
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
    """
    A subclass of Loader that loads block configuration from a JSON file,
    and initializes blocks instances.

    Methods:
        load():
            Loads the JSON file and parses the block configurations,
            and initializes blocks and filled in missing values by the default section.
    """
    def load(self):
        """
        Loads the JSON file and parses the block configurations,
        and initializes blocks and filled in missing values by the default section.
        
        Steps:
            1. Load the JSON file and store the data in self.data.
            2. Create keys and default_data which can fill in the missing fields.
            3. Iterate over the list of block data and initialize blocks.
        """
        with open(self.path, 'r') as f:
            self.data = json.load(f)
        
        keys = self.data["default"].keys()
        default_data = self.data["default"]

        for block_data in self.data["blocks"]:
            block_info = {key: block_data.get(key, default_data.get(key)) for key in keys}
            blocks.Block(**block_info)


class MazeLoader(MultiLoader): 
    """
    A subclass of Loader that loads maze configurations from a JSON file,
    and provides various information about the mazes.

    Methods:
        get_baiscs():
            Get the basic information of the maze, including height and width.
        get_resources():
            Get the mainly part of the maze, 
            including the start and end points and the block table.
        get_routes():
            Get the routes of the chasers in the maze.
        get_maze_nums():
            Get the total number of the available mazes.
    """
    def get_basics(self) -> tuple[int, int]:
        """
        Get the basic information of the maze, including height and width.
        
        Returns:
            tuple[int, int]
                A tuple which contains the height and width of the maze.
        """
        maze_data = self.data[self.index]
        height = maze_data["height"]
        width = maze_data["width"]
        return height, width

    def get_resources(self) -> dict[str, Any]:
        """
        Get the mainly part of the maze, 
        including the start and end points and the block table.

        Returns:
            dict[str, Any]
                A dict which stores blocks list and start/end points information.
        """
        maze_data = self.data[self.index]
        start = tuple(maze_data["start"])
        end = tuple(maze_data["end"])
        block_names = maze_data["block_names"]
        return {
            "blocks": [blocks.get_block(block_name) for block_name in block_names], 
            "start": start,
            "end": end
        }
    
    def get_routes(self) -> dict[str, list[tuple[int, int]]]:
        """
        Get the routes of the chasers in the maze.

        Returns:
            dict[str, list[tuple[int, int]]
                A dict which stores the routes of the chasers.
        """
        maze_data = self.data[self.index]
        return maze_data.get("routes", {})
    
    def get_maze_nums(self) -> int:
        """
        Get the total number of the available mazes.

        Returns:
            int
                The number of the available mazes.
        """
        return len(self.data)


class MenuLoader(MultiLoader):
    """
    A subclass of Loader that loads menu configurations from a JSON file,
    and provides various information about the menus.

    Methods:
        get_baiscs():
            Get the basic information of the menu, including height and width.
        get_resources():
            Get the mainly part of the menu, including the texts.
    """
    def get_basics(self) -> tuple[int, int]:
        """
        Get the basic information of the menu, including height and width.

        Returns:
            tuple[int, int]
                A tuple which contains the height and width of the menu window.
        """
        menu_data = self.data[self.index]
        return menu_data["height"], menu_data["width"]

    def get_resources(self):
        """
        Get the mainly part of the menu, including the texts.

        Returns:
            list[Text]
                A list of Text which will be shown in the menu.
        """
        menu_data = self.data[self.index]
        return [display.Text(**text_data) for text_data in menu_data["texts"]]


