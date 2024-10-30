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

    # Displayer Initiliazation
    displayer = display.Displayer(stdscr)
    curses.curs_set(0)


    # Start Menu
    win = displayer.create_win(7, 20)
    displayer.display_start()
    
    while True:
            
            # Keyboard Input
            key = stdscr.getch()

            # Exit Game
            if key == ord('q'):
                return
            
            # Start Game
            elif key == ord('1'):
                win.erase()
                win.refresh()
                break

            # Display
            displayer.display_start()

    # Sprites Initialization
    win = displayer.create_win(maze_height, maze_width, blocks.get_block_size())
    maze = sprites.Maze(win, maze_height, maze_width, **maze_loader.get_resource_info())
    player = sprites.Player(win, maze_height, maze_width, [blocks.get_block("player")], maze)
    displaying_sprites = [maze, player]
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
        
        # TODO: End Check
        # if player.check_win():
        #     # TODO: Display the winning pictures
        #     pass
        # elif player.check_lose():
        #     # TODO: Display the losing pictures
        #     pass


        # Display
        displayer.display_game(displaying_sprites)

curses.wrapper(main)

