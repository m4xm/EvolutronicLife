import curses
from Window import InfoWindow, MapWindow, OptionPane
from distutils.ccompiler import gen_lib_options
import globals as global_vars


#start and configure curses as needed
_main_win = curses.initscr()
curses.start_color()
curses.noecho()
curses.cbreak()
curses.curs_set(0)
_main_win.nodelay(1)
_main_win.keypad(1)
_main_win.refresh()

#declare colors
curses.init_pair(global_vars.WHITE_ON_BLUE, curses.COLOR_WHITE, curses.COLOR_BLUE)
curses.init_pair(global_vars.BLUE_ON_BLACK, curses.COLOR_BLUE, curses.COLOR_BLACK)
curses.init_pair(global_vars.RED_ON_BLACK, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(global_vars.GREEN_ON_BLACK, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(global_vars.YELLOW_ON_BLACK, curses.COLOR_YELLOW, curses.COLOR_BLACK)
curses.init_pair(global_vars.CYAN_ON_BLACK, curses.COLOR_CYAN, curses.COLOR_BLACK)
curses.init_pair(global_vars.MAGENTA_ON_BLACK, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
curses.init_pair(global_vars.WHITE_ON_CYAN, curses.COLOR_WHITE, curses.COLOR_CYAN)

def init():
    """
    init subwindows
    """
    global _info_win, _map_win, _option_pane
    _info_win = InfoWindow(1, 140, 0, 0)
    _map_win = MapWindow(35, 140, 1, 0)
    _option_pane = OptionPane(1, 140, 36, 0, "Pause", "Faster", "Slower", "Exit")


def update(the_map=None):
    """
    updates content of info window and also the map window, if a map is given
    :param the_map: the game map in the current state
    """
    _info_win.update()
    if(the_map):
        _map_win.update(the_map)

    curses.doupdate()


def replace_option(option_to_replace, new_option):
    """
    replaces option_to_replace with new_option in the_option pane
    :param option_to_replace: the option to replace
    :param new_option: the new option to take its place
    """
    _option_pane.replace_option(option_to_replace, new_option)


def key_pressed():
    """
    returns the current pressed key
    """
    return _main_win.getch()


def terminate():
    """
    unloads curses
    """
    curses.nocbreak()
    _main_win.keypad(0)
    curses.echo()
    curses.endwin()

def progress_info(end):
    _main_win.addstr(0, 0, "Generating step: %d/%d" % (global_vars.step, end))
    _main_win.noutrefresh()
