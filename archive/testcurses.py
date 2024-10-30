import curses

def main(stdscr):
    stdscr.clear()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_MAGENTA)


    for i in range(3):
        stdscr.addstr(f"This is line {i}\n", curses.color_pair(i))

    stdscr.addstr(f"The windows has width {curses.COLS} and height {curses.LINES}")

    stdscr.refresh()
    stdscr.getch()

curses.wrapper(main)

