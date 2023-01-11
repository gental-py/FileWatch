"""
Module: logs.py
Create logs with given context.
"""

from datetime import datetime
from typing import Iterable

formatted_types = {
    "modified": "Modified ",
    "created":  "Created  ",
    "deleted":  "Deleted  ",
    "moved":    "Moved    ",
}

TEMP_PHRASES = ('tmp', 'temp')
LOG_PHRASES = ('log')


def get_date() -> str:
    """ Return current date as a string in format: 15/04/2022 """
    return datetime.today().strftime("%d/%m/%Y")

def get_time() -> str:
    """ Return current time as a string in format: 13:12:54 """
    return datetime.now().strftime("%H:%M:%S")

def is_any_phrase_in_log(phrases: Iterable, log: str):
    """ Check if any value of iterable phrases is inside log.

        @phrases (iterable[str]): iterable containing string values
        @log (str):

        >return (bool): Any of phrases is in log?
    """
    return any([ phrase in log.lower() for phrase in phrases ])

def format_log(event) -> str:
    """ Format given event into writable log with format:

        13/11/2022 23:12:54 | Created | path...
    """

    log = "{} {} | {} | {} \n".format(
        get_date(),
        get_time(),
        formatted_types[event.event_type],
        event.src_path
    )

    return log

def write_log(path: str, log: str):
    """ Write log into given path. """

    with open(path, "a", encoding="utf-8") as file:
        file.write(log)
