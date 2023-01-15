"""
Module: stats.py
Display live time stats for each path.
"""

import curses

CURSES_INITIALIZED = False
screen_length = -1

def init_curses():
    global screen_length, CURSES_INITIALIZED

    main_screen = curses.initscr()
    _, screen_length = main_screen.getmaxyx()
    curses.curs_set(0)
    Colors.setup_colors()

    CURSES_INITIALIZED = True



class Colors:
    """ Colors used by curses. """

    def setup_colors():
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_WHITE)

        Colors.RED = curses.color_pair(1) # delete
        Colors.BLUE = curses.color_pair(2) # move
        Colors.GREEN = curses.color_pair(3) # create
        Colors.WHITE = curses.color_pair(4) # modify
        Colors.MAGENTA = curses.color_pair(5)
        Colors.BLACK_ON_WHITE = curses.color_pair(6)


    def get_coresponding(type):
        colors = {
            "deleted":  Colors.RED, 
            "moved":    Colors.BLUE,
            "created":  Colors.GREEN,
            "modified": Colors.WHITE, 
        }

        return colors[type]


class Events:
    """ Events names. """

    class Full:
        CREATED = "created"
        DELETED = "deleted"
        MOVED = "moved"
        MODIFIED = "modified"

    class Short:
        CREATED = "new"
        DELETED = "del"
        MOVED = "mov"
        MODIFIED = "mod"


class Item:
    items = {}

    @staticmethod
    def find(item_name: str):
        """ Find Item object coresponding to given letter. """
        return Item.items[item_name] if item_name in Item.items else None

    @staticmethod
    def create_window():
        """ Create curses window object. """
        window = curses.newwin(1, screen_length-1, len(Item.items), 0)
        return window
    

    def __init__(self, name):
        self.name = name
        self.counter = {
            'all': 0,
            Events.Full.CREATED: 0,
            Events.Full.DELETED: 0,
            Events.Full.MOVED: 0,
            Events.Full.MODIFIED: 0
        }
        self.window = Item.create_window()
        self.last_type = None

        Item.items.update({name: self})

    def handle_event(self, event_type):
        """ Increase counter and call screen updater. """
        self.counter['all'] += 1
        self.counter[event_type] += 1
        self.last_type = event_type
        self.update()

    def update(self):
        """ Update counter on screen. """

        self.window.clear()
        self.window.erase()

        self.window.addstr("[", Colors.MAGENTA)
        self.window.addstr(f" {self.name} ", Colors.get_coresponding(self.last_type) + curses.A_REVERSE)
        self.window.addstr("] ", Colors.MAGENTA)
        self.window.addstr(f"{self.counter['all']}", Colors.get_coresponding(self.last_type))
        self.window.addstr(" ")

        self.window.refresh()

def handle(name, event_type):
    """ Handle event from Handler object. """

    if not CURSES_INITIALIZED:
        init_curses()

    if not name in Item.items:
        Item(name)

    item_object = Item.find(name)
    item_object.handle_event(event_type)
