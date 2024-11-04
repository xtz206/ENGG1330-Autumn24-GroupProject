import curses
import sys

import blocks
import sprites
import loaders
import display


def start(stdscr, displayer, menu_loader):
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
                return 0
            
            elif ord('1') <= key <= ord('9'):
                maze_index = int(chr(key))
                return maze_index

            # Display
            displayer.display_start(menu_loader.get_resource_info())

def game(stdscr, displayer, maze_loader, maze_index):
    # Sprites Initialization
    maze_loader.set_index(maze_index)
    maze_height, maze_width = maze_loader.get_basic_info()
    win = displayer.create_win(maze_height, maze_width, blocks.get_block_size())
    maze = sprites.Maze(win, maze_height, maze_width, **maze_loader.get_resource_info())
    player = sprites.Player(win, maze_height, maze_width, [blocks.get_block("player")], maze)
    chasers = []
    for name, route in maze_loader.get_route_info().items():
        if "auto" in name:
            chasers.append(sprites.AutoChaser(win, maze_height, maze_width, [blocks.get_block("chaser")], maze, route, player))
        else:
            chasers.append(sprites.FixedChaser(win, maze_height, maze_width, [blocks.get_block("chaser")], maze, route))
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
        elif key == ord('r'):
            return {
                "status": "retry",
            }
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
            return {
                "status": "win",
                "step": player.step,
                "score": player.score
            }
        
        elif player.check_lose():
            return {
                "status": "lose",
                "step": player.step,
                "score": player.score
            }

        # Display
        displayer.display_game(displaying_sprites)

def end(stdscr, displayer, menu_loader, results):
    # End Menu
    menu_loader.set_index(results["status"])
    win = displayer.create_win(*menu_loader.get_basic_info())
    displayer.erase_win(stdscr)
    displayer.erase_win(win)
    displayer.display_end(menu_loader.get_resource_info(), (results["step"], results["score"]))

    while True:
            
            # Keyboard Input
            key = stdscr.getch()

            # Exit Game
            if key == ord('q'):
                sys.exit()
            elif key == ord('r'):
                return {
                    "status": "retry",
                }
            elif key == ord('c'):
                if results["status"] == "win":
                    return {
                        "status": "continue"
                    }
            # Display
            displayer.display_end(menu_loader.get_resource_info(), (results["step"], results["score"]))

def main(stdscr):
    # Loaders Initialization
    color_loader = loaders.ColorLoader("assets/colors.json")
    block_loader = loaders.BlockLoader("assets/blocks.json")
    maze_loader = loaders.MazeLoader("assets/mazes.json")
    menu_loader = loaders.MenuLoader("assets/menu.json")

    # Assets Initialization
    color_loader.load()
    block_loader.load()
    maze_loader.load()
    menu_loader.load()

    # Displayer Initialization
    displayer = display.Displayer(stdscr)
    curses.curs_set(0)
    displayer.erase_win(stdscr)
    stdscr.refresh()

    maze_index = start(stdscr, displayer, menu_loader)
    
    while True:
        results = game(stdscr, displayer, maze_loader, maze_index)
        if results["status"] == "retry":
            continue
        
        results = end(stdscr, displayer, menu_loader, results)
        if results["status"] == "retry":
            continue
        elif results["status"] == "continue" and maze_index < maze_loader.get_maze_nums():
            maze_index += 1
            continue
        else:
            sys.exit()
        

curses.wrapper(main)


