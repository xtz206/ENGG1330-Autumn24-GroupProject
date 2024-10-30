import curses

import blocks
import sprites
import loaders
import display

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

    # Start Menu
    menu_loader.set_index("start")
    win = displayer.create_win(*menu_loader.get_basic_info())
    displayer.display_start(menu_loader.get_resource_info())

    while True:
            
            # Keyboard Input
            key = stdscr.getch()

            # Exit Game
            if key == ord('q'):
                return
            
            # Start Game
            elif key == ord('t'):
                win.erase()
                win.refresh()
                maze_index = 0
                break
            
            elif key == ord('1'):
                win.erase()
                win.refresh()
                maze_index = 1
                break

            # Display
            displayer.display_start(menu_loader.get_resource_info())

    # Sprites Initialization
    maze_loader.set_index(maze_index)
    maze_height, maze_width = maze_loader.get_basic_info()
    win = displayer.create_win(maze_height, maze_width, blocks.get_block_size())
    maze = sprites.Maze(win, maze_height, maze_width, **maze_loader.get_resource_info())
    player = sprites.Player(win, maze_height, maze_width, [blocks.get_block("player")], maze)
    chaser = sprites.Chaser(win, maze_height, maze_width, [blocks.get_block("chaser")], maze)
    displaying_sprites = [maze, player, chaser]
    displayer.display_game(displaying_sprites)

    # Game Loop
    while True:

        # Keyboard Input
        key = stdscr.getch()
        
        # Exit Game
        if key == ord('q'):
            return

        # Moving
        elif key == ord('w'):
            player.move(-1, 0)
        elif key == ord('s'):
            player.move(1, 0)
        elif key == ord('a'):
            player.move(0, -1)
        elif key == ord('d'):
            player.move(0, 1)
        
        # End Check
        if player.check_win():
            player_status = "win"
            break

        # Display
        displayer.display_game(displaying_sprites)


    # End Menu
    menu_loader.set_index(player_status)
    win = displayer.create_win(*menu_loader.get_basic_info())
    displayer.display_start(menu_loader.get_resource_info())

    while True:
            
            # Keyboard Input
            key = stdscr.getch()

            # Exit Game
            if key == ord('q'):
                return

            # Display
            displayer.display_start(menu_loader.get_resource_info())

curses.wrapper(main)


