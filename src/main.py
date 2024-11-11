import curses
import sys

import blocks
import sprites
import loaders
import display


def start(stdscr, displayer, menu_loader, maze_loader):
    """
    Initializes and starts the main menu.
    
    Args:
        stdscr:         curses.window
            The main window object from curses.
        displayer:      Displayer
            An object for handling the display operations.
        menu_loader:    MenuLoader
            An object for loading and initializing the menu assets.
        maze_loader:    MazeLoader
            An object for loading and initializing the maze assets.
    
    Returns:
        str
            The status of the game,
            returns "start" for starting the game.
    """

    # Initialization
    menu_loader.set_index("start")
    win = displayer.create_win(*menu_loader.get_basics())
    displayer.erase_win(stdscr)
    displayer.erase_win(win)
    displayer.display_menu(menu_loader.get_resources())
    
    while True:
            
            # Keyboard Input
            key = stdscr.getch()
            # Exit Game
            if key == ord('q'):
                sys.exit()
            
            # Start Game
            elif key == ord('t'):
                maze_loader.set_index(0)
                tutorial(stdscr, displayer, menu_loader) # Goto the tutorial menu
                return "start"

            elif ord('1') <= key <= ord('9'):
                maze_index = int(chr(key))
                maze_loader.set_index(maze_index)
                return "start"

            # Display
            displayer.display_menu(menu_loader.get_resources())

def tutorial(stdscr, displayer, menu_loader):
    """
    Displays the tutorial menu.
    
    Args:
        stdscr:         curses.window
            The main window object from curses.
        displayer:      Displayer
            An object for handling the display operations.
        menu_loader:    MenuLoader
            An object for loading and initializing the menu assets.
    
    Returns:
        str
            The status of the game,
            returns "continue" to stop displaying tutorial.
    """

    # Initialization
    menu_loader.set_index("tutorial")
    win = displayer.create_win(*menu_loader.get_basics())
    displayer.erase_win(stdscr)
    displayer.erase_win(win)
    displayer.display_menu(menu_loader.get_resources())

    while True:

        # Keyboard Input
        key = stdscr.getch()

        # Exit Game
        if key == ord('q'):
            sys.exit()
        
        elif key == ord('c'):
            return "continue"
        
        # Display
        displayer.display_menu(menu_loader.get_resources())

def game(stdscr, displayer, recorder, maze_loader):
    """
    Initializes and runs the tutorial menu.
    
    Args:
        stdscr:         curses.window
            The main window object from curses.
        displayer:      Displayer
            An object for handling the display operations.
        recorder:       Recorder
            An object for recording the scores and steps in the game play.
        maze_loader:    MazeLoader
            An object for loading and initializing the maze assets.
    
    Returns:
        str
            The status of the game,
            returns "retry" for retrying the previous level,
            returns "back" for going back to the start menu,
            returns "win" if the level is cleared,
            returns "lose" if the player is caught by the chasers.
    """
    
    # Sprites Initialization
    maze_height, maze_width = maze_loader.get_basics()
    win = displayer.create_win(maze_height, maze_width, blocks.get_block_size())
    maze = sprites.Maze(win, maze_height, maze_width, **maze_loader.get_resources())
    player = sprites.Player(win, maze_height, maze_width, [blocks.get_block("player")], maze)
    chasers = []
    for name, route in maze_loader.get_routes().items():
        if "auto" in name: # Auto Chasers
            chasers.append(sprites.AutoChaser(win, maze_height, maze_width, [blocks.get_block("chaser")], maze, route, player))
        else: # Fixed Chasers
            chasers.append(sprites.FixedChaser(win, maze_height, maze_width, [blocks.get_block("chaser"), blocks.get_block("warning")], maze, route))
    maze.set_player(player)
    maze.set_chasers(chasers)
    displaying_sprites = [maze, player] + chasers

    # Displayer Initialization
    displayer.erase_win(stdscr)
    displayer.erase_win(win)
    displayer.display_game(displaying_sprites)

    # Game Loop
    while True:

        # Keyboard Input
        key = stdscr.getch()
        if key == ord('q'):
            sys.exit()
        elif key == ord('m'):
            return "back"
        elif key == ord('r'):
            return "retry"
        elif key == ord('w'):
            player_dy, player_dx = -1, 0
        elif key == ord('s'):
            player_dy, player_dx = 1, 0
        elif key == ord('a'):
            player_dy, player_dx = 0, -1
        elif key == ord('d'):
            player_dy, player_dx = 0, 1
        else:
            player_dy, player_dx = 0, 0
        
        # Move
        if player.move(player_dy, player_dx):          
            for chaser in chasers:
                chaser.move()
        
        # Check
        if player.check_win():
            record = {
                "status": "win",
                "step": player.step,
                "score": player.score
            }
            recorder.insert_record(record)
            return "win"
        
        elif player.check_lose():
            record = {
                "status": "lose",
                "step": player.step,
                "score": 0
            }
            recorder.insert_record(record)
            return "lose"

        # Display
        displayer.display_game(displaying_sprites)

def end(stdscr, displayer, recorder, menu_loader, maze_loader):
    """
    Handle and display the end menu which will display when a level is cleared or lost.

    Args:
        stdscr:         curses.window
            The main window object from curses.
        displayer:      Displayer
            An object for handling the display operations.
        recorder:       Recorder
            An object for recording the scores and steps in the game play.
        menu_loader:    MenuLoader
            An object for loading and initializing the menu assets.
        maze_loader:    MazeLoader
            An object for loading and initializing the maze assets.
    
    Returns:
        str
            The status of the game,
            returns "retry" for retrying the previous level,
            returns "back" for going back to the start menu,
            returns "continue" for going forward to the next level,
            returns "clear" for going forward to the final menu.
    """

    # End Menu
    record = recorder.get_record()
    menu_loader.set_index(record["status"])
    win = displayer.create_win(*menu_loader.get_basics())
    displayer.erase_win(stdscr)
    displayer.erase_win(win)
    displayer.display_menu(menu_loader.get_resources(), (record["step"], record["score"]))

    while True:
            
            # Keyboard Input
            key = stdscr.getch()

            # Exit Game
            if key == ord('q'):
                sys.exit()
            elif key == ord('r'):
                return "retry"
            elif key == ord('m'):
                return "back"

            elif key == ord('c') and record["status"] == "win":
                    if maze_loader.index + 1 < maze_loader.get_maze_nums():
                        maze_loader.set_index(maze_loader.index + 1)
                        return "continue"
                    else:
                        return "clear"

            # Display
            displayer.display_menu(menu_loader.get_resources(), (record["step"], record["score"]))

def final(stdscr, displayer, recorder, menu_loader):
    """
    Handle and display the final menu which will display when all levels are cleared.

    Args:
        stdscr:         curses.window
            The main window object from curses.
        displayer:      Displayer
            An object for handling the display operations.
        recorder:       Recorder
            An object for recording the scores and steps in the game play.
        menu_loader:    MenuLoader
            An object for loading and initializing the menu assets.
    
    Returns:
        str
            The status of the game,
            returns "back" for going back to the start menu,
    """

    # Final Menu
    summary = recorder.summarize_recodes()
    menu_loader.set_index("final")
    win = displayer.create_win(*menu_loader.get_basics())
    displayer.erase_win(stdscr)
    displayer.erase_win(win)
    displayer.display_menu(menu_loader.get_resources(), summary.values())

    while True:
            
            # Keyboard Input
            key = stdscr.getch()

            # Exit Game
            if key == ord('q'):
                sys.exit()
            elif key == ord('m'):
                return "back"

            # Display
            displayer.display_menu(menu_loader.get_resources(), summary.values())


def main(stdscr):
    """
    The main function for the whole application,
    which initializes loaders and loads the assets,
    while it also controls the game progress from menu to game play.
    
    Args:
        stdscr: curses.window
            The standard screen object from curses.
    """

    # Loaders Initialization
    color_loader = loaders.ColorLoader("assets/colors.json")
    block_loader = loaders.BlockLoader("assets/blocks.json")
    maze_loader = loaders.MazeLoader("assets/mazes.json")
    menu_loader = loaders.MenuLoader("assets/menu.json")

    # Assets Load
    color_loader.load()
    block_loader.load()
    maze_loader.load()
    menu_loader.load()

    # Displayer and Recorder Initialization
    displayer = display.Displayer(stdscr)
    recorder = display.Recorder()
    curses.curs_set(0)
    displayer.erase_win(stdscr)
    stdscr.refresh()

    status = "start"
    while status == "start" or status == "back":
        status = start(stdscr, displayer, menu_loader, maze_loader)

        while status == "retry" or status == "continue" or status == "start":
            status = game(stdscr, displayer, recorder, maze_loader)
        
            if status == "win" or status == "lose":
                status = end(stdscr, displayer, recorder, menu_loader, maze_loader)
            
        if status == "clear":
            status = final(stdscr, displayer, recorder, menu_loader)
      

curses.wrapper(main)


