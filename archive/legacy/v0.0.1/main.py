import curses
import blocks
from spirits import *
from mazes import *

def init_color(colors):
    for index, (name, color) in enumerate(colors.items()):
        curses.init_pair(index + 1, *color)
        blocks.Block.get_block(name).set_color(curses.color_pair(index + 1))

def render(win, objs):
    # win.clear()
    for obj in objs:
        obj.draw()
    win.refresh()

def main(stdscr):
    # Maze Initialization
    maze_loader = MazeLoader()
    maze_info = height, width, size = maze_loader.get_maze_info(0)
    maze_blocks = maze_loader.get_maze_blocks(0)

    # Display Initiliazation
    origin = (stdscr.getmaxyx()[0] - height * size[0]) // 2, (stdscr.getmaxyx()[1] - width * size[1]) // 2
    win = curses.newwin(height * size[0], width * size[1], *origin)

    # Spirits Initialization
    playground = Playground(win, *maze_info, maze_blocks)
    player = Player(win, *maze_info)
    spirits = [playground, player]
    init_color(blocks.colors)

    render(win, spirits)
    
    # Game Main Loop
    while True:

        # Keyboard Input
        key = stdscr.getch()
        if key == ord('q'):     # EXIT GAME
            break
        elif key == ord('w'):
            player.move(-1, 0)
        elif key == ord('a'):
            player.move(0, -1)
        elif key == ord('s'):
            player.move(1, 0)
        elif key == ord('d'):
            player.move(0, 1)
        
        # Display
        render(win, spirits)

curses.wrapper(main)
