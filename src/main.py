import curses

import blocks
import sprites
import loaders
import display

def main(stdscr):
    # Assets Loading
    color_loader = loaders.ColorLoader("assets/colors.json")
    color_loader.load()
    block_loader = loaders.BlockLoader("assets/blocks.json")
    block_loader.load()
    maze_loader = loaders.MazeLoader("assets/mazes.json")
    maze_loader.set_index(0)
    maze_height, maze_width = maze_loader.get_basic_info()

    # Window and Displayer Initiliazation
    displayer = display.Displayer(stdscr)
    curses.curs_set(0)
    game_win = displayer.create_win("game", maze_height, maze_width, blocks.get_block_size())


    # Sprites Initialization
    maze = sprites.Maze(game_win, maze_height, maze_width, **maze_loader.get_resource_info())
    player = sprites.Player(game_win, maze_height, maze_width, [blocks.get_block("player")], maze)
    displaying_sprites = [maze, player]
    
    # TODO: The start menu


    # Game Main Loop
    displayer.display_game(displaying_sprites)

    while True:

        # Keyboard Input
        key = stdscr.getch()
        
        # Exit Game
        if key == ord('q'):
            break

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
