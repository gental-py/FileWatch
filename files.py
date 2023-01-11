"""
Module: files.py
Manages program files like logs and config.
"""

import getpass
import json
import os
import re

import display
import config

ALL_DISKS = [ 
            full_disk_name[0] for full_disk_name in
            re.findall(
                r"[A-Z]+:.*$", os.popen("mountvol /").read(),
                re.MULTILINE
            ) 
            ]

MAIN_DIRECTORY = f"C:\\Users\\{getpass.getuser()}\\AppData\\Local\\FILES STRUCT LOGS\\"
SPECIAL_LOGS_FILE_PATH = MAIN_DIRECTORY + "specials.log"
CONFIG_FILE_PATH = MAIN_DIRECTORY + "config.json"


def bytes_to_gigabytes(bytes_value: int) -> float:
    """ Convert bytes to Gigabytes. """
    return bytes_value / 1073741824

def get_all_logs_files_paths() -> list:
    """ Generate paths to all logs files. """

    paths = [SPECIAL_LOGS_FILE_PATH]

    # Add all disk's logs files.
    for disk in ALL_DISKS:
        paths.append(make_path_for_disk(disk))

    return paths

def is_existing(file_path: str) -> bool:
    """ Check if file with given path exists. """
    return os.path.exists(file_path)

def create_file(file_path: str):
    """ Create file with given file_path. """
    open(file_path, "a+", encoding="utf-8").close()

def create_directory(dir_path: str):
    """ Create directory with given dir_path. """
    os.mkdir(dir_path)

def make_path_for_disk(letter: str):
    """ Return path as a str for disk's log file. """
    return MAIN_DIRECTORY + letter + ".log"

def check_program_files():
    """ Check all needed files existence and create missing ones. """

    # Check main directory in appdata.
    if not is_existing(MAIN_DIRECTORY):
        create_directory(MAIN_DIRECTORY)

    # Check file for all disks.
    for disk in ALL_DISKS :
        if not is_existing(make_path_for_disk(disk)):
            create_file(make_path_for_disk(disk))

    # Check config file.
    if not is_existing(CONFIG_FILE_PATH):
        create_file(CONFIG_FILE_PATH)

        with open(CONFIG_FILE_PATH, 'w+', encoding="utf-8") as file:
            json.dump(config.DEFAULT_CONFIG, file, indent=4, separators=(',',': '))

    # Check special logs file.
    if not is_existing(SPECIAL_LOGS_FILE_PATH):
        create_file(SPECIAL_LOGS_FILE_PATH)

def control_files_size(alert_size_gb):
    """ Check if log files are bigger than max size and alert bigger files.

        @alert_size_gb (numeric): Part of user config,
         represents size needed to achieve to display alert.
    """
    paths = get_all_logs_files_paths()

    for path in paths:
        size_gb = bytes_to_gigabytes(os.path.getsize(path))

        if size_gb >= alert_size_gb:
            display.message_box_warning(
                "Logs file size alert",
                f"File: {os.path.basename(path)} got alert size: {size_gb} Gb!"
            )
