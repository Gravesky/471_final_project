import curses
import time

stdscr = curses.initscr()



while True:
    
    curses.cbreak()
    print("Type input: ")
    c = stdscr.getch()
    stdscr.addstr()
    stdscr.refresh()
    time.sleep(3)





#curses.endwin()