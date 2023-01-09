import display
import getpass
import config
import json
import os
import re

ALL_DISKS = [ full_disk_name[0] for full_disk_name in re.findall( r"[A-Z]+:.*$", os.popen("mountvol /").read(), re.MULTILINE )]
MAIN_DIRECTORY = f"C:\\Users\\{getpass.getuser()}\\AppData\\Local\\FILES STRUCT LOGS\\"
SPECIAL_LOGS_FILE_PATH = MAIN_DIRECTORY + "sepcials.log"
CONFIG_FILE_PATH = MAIN_DIRECTORY + "config.json"


def bytesToGigabytes(bytes: int) -> float:
    """ Convert bytes to Gigabytes. """
    return bytes / 1073741824

def getAllLogsFilesPaths() -> list:
    """ Generate paths to all logs files. """

    paths = [SPECIAL_LOGS_FILE_PATH]

    # Add all disk's logs files.
    for disk in ALL_DISKS:
        paths.append(makePathForDisk(disk))

    return paths

def isExisting(file_path: str) -> bool:
    """ Check if file with given path exists. """
    return os.path.exists(file_path)

def createFile(file_path: str):
    """ Create file with given file_path. """
    open(file_path, "a+").close()

def createDirectory(dir_path: str):
    """ Create directory with given dir_path. """
    os.mkdir(dir_path)

def makePathForDisk(letter: str):
    """ Return path as a str for disk's log file. """
    return MAIN_DIRECTORY + letter + ".log"

def checkFiles() -> list[str]:
    """ Check all needed files existance and create missing ones.
        
        >return (list[str]): List of created files. Used to display information.
    """

    created_objects = []

    # Check main directory in appdata.
    if not isExisting(MAIN_DIRECTORY):
        createDirectory(MAIN_DIRECTORY)
        created_objects.append("Main directory")

    # Check file for all disks.
    for disk in ALL_DISKS :
        if not isExisting(MAIN_DIRECTORY + disk + ".log"):
            created_objects.append(f"Log file for: {disk}")
            createFile(MAIN_DIRECTORY + disk + ".log")

    # Check config file.
    if not isExisting(CONFIG_FILE_PATH):
        created_objects.append("User config file")
        createFile(CONFIG_FILE_PATH)

        with open(CONFIG_FILE_PATH, 'w+') as file:
            json.dump(config.DEFAULT_CONFIG, file, indent=4, separators=(',',': '))

    # Check special logs file.
    if not isExisting(SPECIAL_LOGS_FILE_PATH):
        created_objects.append("Special logs file")
        createFile(SPECIAL_LOGS_FILE_PATH)

    return created_objects

def controlFilesSize(alert_size_gb):
    """ Check if log files are bigger than max size and alert bigger files. 

        @alert_size_gb (numeric): Part of user config, represents size needed to achive to display alert.
    """
    paths = getAllLogsFilesPaths()

    for path in paths:
        size_gb = bytesToGigabytes(os.path.getsize(path))
        if size_gb >= alert_size_gb:
            display.warning(f"Logs file size alert", f"File: {os.path.basename(path)} got alert size: {size_gb} Gb!")
