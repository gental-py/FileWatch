from datetime import datetime
from typing import Iterable

formatted_types = {
    "modified": "Modified ",
    "created":  "Created  ",
    "deleted":  "Deleted  ",
    "moved":    "Moved    ",
}

temp_phrases = ('tmp', 'temp', 'temporary')
log_phrases = ('log', 'logs')


def getDate() -> str:
    """ Return current date as a string in format: 15/04/2022 """
    return datetime.today().strftime("%d/%m/%Y")

def getTime() -> str: 
    """ Return current time as a string in format: 13:12:54 """
    return datetime.now().strftime("%H:%M:%S")

def isPhraseInLog(phrases: Iterable, log: str):
    """ Check if any value of iterable phrases is inside log. 

        @phrases (iterable[str]): iterable containing string values
        @log (str): 

        >return (bool): Any of phrases is in log?
    """
    return any([ phrase in log.lower() for phrase in phrases ])

def formatLog(event) -> str:
    """ Format given event into writable log with format:

        13/11/2022 23:12:54 | Created | path...        
    """

    log = "{} {} | {} | {} \n".format(
        getDate(),
        getTime(),
        formatted_types[event.event_type],
        event.src_path
    )

    return log

def writeLog(path: str, log: str):
    """ Write log into given path. """

    with open(path, "a") as file:
        file.write(log)
