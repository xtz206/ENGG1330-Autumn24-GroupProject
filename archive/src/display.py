import curses
from typing import Optional, Any

class Text:
    """
    A class to handle the display of texts.
    
    Attributes:
        content: str
            The content to be displayed.
        line: int
            The line number where the text should be displayed.
        align: bool, optional
            Whether the text should be centered (default is False).
        indent: int, optional
            The number of spaces to indent the text (default is 0).
        variable: bool, optional
            Whether the text contains variable to be filled in (default is False).
        color: int, optional
            The color pair number to be used for displaying the text (default is 0).
    
    Methods:
        fillin_variable(fillings):
            Replace variable in the content with the given fillings.
        draw(win):
            Draw the text on the given window.

    """

    def __init__(self, content: str, line: int, align: bool=False, indent: int=0, variable: bool=False, color: int=0):
        self.content: str = content
        self.line: int = line
        self.align: bool = align
        self.indent: int = indent
        self.variable: bool = variable
        self.color: int = color

    def fillin_variable(self, fillins: Any) -> None:
        """
        Replace variable in the content with the given fillings.
        
        Args:
            fillins:    Any
                The fillings which to be filled in the text.        
        """

        self.content = self.content % fillins

    def draw(self, win: curses.window) -> None:
        """
        Draws the text on the given window

        Args:
            win:    curses.window
                The curses window where the text will be drawn.
        """

        height, width = win.getmaxyx()
        y = self.line
        x = ((width - len(self.content)) // 2 if self.align else 0) + self.indent
        win.addstr(y, x, self.content, curses.color_pair(self.color))

class Displayer:
    """
    A class to handle the display operations for the game.

    Attributes:
        screen: curses.window
            The main screen window where the game is displayed.
        win: curses.window or None
            The window for playing the current game content, initialized as None.
    
    Methods:
        erase_win(win: curses.window):
            Erases the contents of a given window.
        create_win(height, width, size=(1, 1)):
            Creates a new window with the given height, width and size, then update self.win.
        display_game(displaying_sprites)
            Displays the game by drawing all the given sprites.
        display_menu(texts, variables=None):
            Displays the menu with the given texts and variables.    
    """

    def __init__(self, screen: curses.window):
        self.screen: curses.window = screen
        self.win: Optional[curses.window] = None

    @staticmethod
    def erase_win(win: curses.window) -> None:
        """
        Erases the contents of a given window.

        Args:
            win:    curses.window
                The window whose content will be erased
        
        Steps:
            1. Erase the content of the window.
            2. Get the height and width of the window.
            3. Add space to the window with the specific color.
            4. Refresh the window.
        """
        
        win.erase()
        h, w = win.getmaxyx()
        win.addstr(" " * (h * w - 1), curses.color_pair(6))
        win.insstr(h - 1, w - 1, " ", curses.color_pair(6))
        win.refresh()

    def create_win(self, height: int, width: int, size: tuple[int, int]=(1,1)) -> curses.window:
        """
        Creates a new window with the given height, width and size, then update self.win.

        Args:
            height: int
                The height of the window.
            width: int
                The width of the window.
            size: tuple[int, int], optional
                A tuple represents the size in terms of height and width.
        
        Returns:
            curses.window:
                The window to be displayed.
        """

        window_height = height * size[0] + 2
        window_width = width * size[1] + 2
        screen_height, screen_width = self.screen.getmaxyx()
        window_origin_y = (screen_height - window_height) // 2
        window_origin_x = (screen_width - window_width) // 2
        self.win = curses.newwin(window_height, window_width, window_origin_y, window_origin_x)
        self.erase_win(self.screen)
        return self.win

    def display_game(self, displaying_sprites: list["Sprite"]) -> None:
        """
        Displays the game by drawing all the given sprites.
        
        Args:
            displaying_sprites: list[Sprite]
                A list of the sprites to be drawn.
        """

        self.win.erase()
        for displaying_sprite in displaying_sprites:
            displaying_sprite.draw()
        self.win.refresh()

    def display_menu(self, texts: list["Text"], variables = None) -> None:
        """
        Displays the menu with the given texts and variables.
        
        Args:
            texts:  list[Text]
                A list of the texts to be displayed.
            variables: list[Any], optional
                A list of variables to be filled in (default is None).     
        """

        if variables is None:
            variables = iter([])
        else:
            variables = iter(variables)
        self.win.erase()
        for text in texts:
            if text.variable:
                variable = next(variables)
                text.fillin_variable(variable)
            text.draw(self.win)
        self.win.refresh()


class Recorder:
    """
    A class to handle the recording of the gameplay.

    Attributes:
        records: list[dict]
            A list of records, initialized as empty list.
    
    Methods:
        insert_record(record):
            Insert the record at the end of records.
        get_record():
            Get the latest record, return None if there is no record in records.
        summarize_recodes():
            Summarize the records and generate a summary. 
    """

    def __init__(self):
        self.records = []
    
    def insert_record(self, record: dict) -> None:
        """
        Insert the record at the end of records.

        Args:
            record: dict
                a single record to be inserted in the records.
        """

        self.records.append(record)
    
    def get_record(self) -> dict:
        """
        Get the latest record, return None if there is no record in records.

        Returns:
            dict[str, Any]
                The latest record in records.
        """

        if len(self.records) == 0:
            return None
        return self.records[-1]
    
    def summarize_recodes(self) -> dict[str, int]:
        """
        Summarize the records and generate a summary.

        Returns:
            dict[str, int]
                The summary generated for the whole game play.
        """

        summary = {
            "win": 0,
            "lose": 0,
            "step": 0,
            "score": 0
        }

        for record in self.records:
            status = record["status"]
            step = record["step"]
            score = record["score"]

            summary["win"] += int(status == "win")
            summary["lose"] += int(status == "lose")
            summary["step"] += step
            summary["score"] += score

        return summary

