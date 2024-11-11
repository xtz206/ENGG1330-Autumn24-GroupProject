import curses
import sys

import blocks
import sprites
import loaders
import display


def start(stdscr, displayer, menu_loader, maze_loader):
    menu_loader.set_index("start")
    win = displayer.create_win(*menu_loader.get_basic_info())
    displayer.erase_win(stdscr)
    displayer.erase_win(win)
    displayer.display_start(menu_loader.get_resource_info())
    
    while True:
            
            # Keyboard Input
            key = stdscr.getch()
            # Exit Game
            if key == ord('q'):
                sys.exit()
            
            # Start Game
            elif key == ord('t'):
                maze_loader.set_index(0)
                tutorial(stdscr, displayer, menu_loader)
                return "start"

            elif ord('1') <= key <= ord('9'):
                maze_index = int(chr(key))
                maze_loader.set_index(maze_index)
                return "start"

            # Display
            displayer.display_start(menu_loader.get_resource_info())

def tutorial(stdscr, displayer, menu_loader):
    menu_loader.set_index("tutorial")
    win = displayer.create_win(*menu_loader.get_basic_info())
    displayer.erase_win(stdscr)
    displayer.erase_win(win)
    displayer.display_start(menu_loader.get_resource_info())

    while True:

        # Keyboard Input
        key = stdscr.getch()

        # Exit Game
        if key == ord('q'):
            sys.exit()
        
        elif key == ord('c'):
            return "continue"
        
        # Display
        displayer.display_start(menu_loader.get_resource_info())

def game(stdscr, displayer, recorder, maze_loader):
    # Sprites Initialization
    maze_height, maze_width = maze_loader.get_basic_info()
    win = displayer.create_win(maze_height, maze_width, blocks.get_block_size())
    maze = sprites.Maze(win, maze_height, maze_width, **maze_loader.get_resource_info())
    player = sprites.Player(win, maze_height, maze_width, [blocks.get_block("player")], maze)
    chasers = []
    for name, route in maze_loader.get_route_info().items():
        if "auto" in name:
            chasers.append(sprites.AutoChaser(win, maze_height, maze_width, [blocks.get_block("chaser")], maze, route, player))
        else:
            chasers.append(sprites.FixedChaser(win, maze_height, maze_width, [blocks.get_block("chaser"), blocks.get_block("warning")], maze, route))
    maze.set_player(player)
    maze.set_chasers(chasers)
    displaying_sprites = [maze, player] + chasers
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
    # End Menu
    record = recorder.get_record()
    menu_loader.set_index(record["status"])
    win = displayer.create_win(*menu_loader.get_basic_info())
    displayer.erase_win(stdscr)
    displayer.erase_win(win)
    displayer.display_end(menu_loader.get_resource_info(), (record["step"], record["score"]))

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
            displayer.display_end(menu_loader.get_resource_info(), (record["step"], record["score"]))

def final(stdscr, displayer, recorder, menu_loader):
    # Final Menu
    summary = recorder.summarize_recodes()
    menu_loader.set_index("final")
    win = displayer.create_win(*menu_loader.get_basic_info())
    displayer.erase_win(stdscr)
    displayer.erase_win(win)
    displayer.display_end(menu_loader.get_resource_info(), summary.values())

    while True:
            
            # Keyboard Input
            key = stdscr.getch()

            # Exit Game
            if key == ord('q'):
                sys.exit()
            elif key == ord('m'):
                return "back"

            # Display
            displayer.display_end(menu_loader.get_resource_info(), summary.values())


def main(stdscr):
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


