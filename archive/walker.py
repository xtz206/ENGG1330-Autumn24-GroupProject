import curses
from random import randint

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
    
    def draw(self, window):
        window.addch(self.y, self.x, '@')

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def draw(self, window):
        window.border()
        window.addstr(0, 2, "Board")
        window.addstr(0, 10, f"Width: {self.width}, Height: {self.height}")

def main(stdscr):
    stdscr.clear()
    stdscr.refresh()

    height, width = stdscr.getmaxyx()
    board = Board(width, height)
    player = Player(randint(width // 3, width * 2 // 3), randint(height // 3, height * 2 // 3))

    while True:
        stdscr.clear()
        board.draw(stdscr)
        player.draw(stdscr)
        stdscr.refresh()

        key = stdscr.getch()
        if key == ord('q'):     # EXIT GAME
            break
        elif key == ord('w'):   # MOVE UP
            player.move(0, -1)
        elif key == ord('s'):   # MOVE DOWN
            player.move(0, 1)
        elif key == ord('a'):   # MOVE LEFT
            player.move(-1, 0)
        elif key == ord('d'):   # MOVE RIGHT
            player.move(1, 0)
curses.wrapper(main)
