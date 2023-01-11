"""
Main: filewatch.py
Initialize program using modules.
"""

from typing import Iterable
import threading
import sys

from config import Configuration
import display
import handle
import config
import files


def start_handling_thread(source_path: str, is_special=False):
    """ Initialize DiskHandler's watchdog's loop. """
    handle.DiskHandler(source_path, configuration, is_special)

def create_threads_list(source_paths: Iterable, is_special=False) -> list[threading.Thread]:
    """ Create list containing pending threads pointed to DiskHandler object.

        @source_paths (Iterable): Paths to be watched.
        @is_special (bool=False): Defines if given path is special.

        >return (list[Thread]): Not ran threads.
    """
    threads_list = []

    for path in source_paths:
        thread = threading.Thread(target=start_handling_thread, args=[path, is_special])
        threads_list.append(thread)

    return threads_list


# Check files health.
files.check_program_files()

# Get configuration.
configuration = Configuration(config.create_config())

# Create thread that will check logs file sizes
# and alert files with bigger size than in user config.
if configuration.logs_size_alert_gb > 0:
    threading.Thread(
        target=files.control_files_size,
        args=[configuration.logs_size_alert_gb],
        daemon=True
    ).start()

# Check if ONLY_SPECIALS is enabled and SPECIALS list is not empty.
special_paths = configuration.specials
if configuration.only_specials:
    if not special_paths:
        display.message_box_error(
            "Specials list is empty.",
            "Cannot run.\nONLY_SPECIALS mode is enabled but SPECIALS list is empty"
        )
        sys.exit()

    # Create different watchdog event handler threads for all paths.
    threads = create_threads_list(special_paths, True)

    # Run all threads.
    [ thread.start() for thread in threads ]

else:
    # Split all disks into different threaded task and run them.
    disks_threads = create_threads_list(files.ALL_DISKS)

    # Add special threads to threads_list.
    special_threads = create_threads_list(special_paths, True)

    # Combine two lists of threads together.
    threads = disks_threads + special_threads

    # Run all threads.
    [ thread.start() for thread in threads ]
