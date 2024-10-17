import curses


def main(stdscr):
    # Clear screen and hide the cursor
    stdscr.clear()
    curses.curs_set(0)

    # Instructions
    stdscr.addstr(0, 0, "Use arrow keys to move 'X'. Press 'q' to quit.")
    stdscr.refresh()

    # Initial position of 'X'
    y, x = 1, 0

    while True:
        key = stdscr.getch()

        if key == ord('q'):
            break
        elif key == curses.KEY_UP:
            y = max(1, y - 1)
        elif key == curses.KEY_DOWN:
            y = min(curses.LINES - 1, y + 1)
        elif key == curses.KEY_LEFT:
            x = max(0, x - 1)
        elif key == curses.KEY_RIGHT:
            x = min(curses.COLS - 1, x + 1)

        stdscr.clear()
        stdscr.addstr(0, 0, "Use arrow keys to move 'X'. Press 'q' to quit.")
        stdscr.addstr(y, x, 'X')
        stdscr.refresh()



if __name__ == "__main__":
    # Run the main function within curses.wrapper to handle initialization and cleanup
    curses.wrapper(main)

