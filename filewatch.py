"""
Main: filewatch.py
Initialize program using modules.
"""

from typing import Iterable
import threading
import sys

from config import Configuration
import structure
import display
import handle
import config


def start_handling_thread(source_path: str, settings: dict, is_special=False):
    """ Initialize DiskHandler's watchdog's loop. """
    handle.DiskHandler(source_path, configuration, is_special, settings)

def create_threads_list(source_paths: Iterable, settings: dict, is_special=False) -> list[threading.Thread]:
    """ Create list containing pending threads pointed to DiskHandler object.

        @source_paths (Iterable): Paths to be watched.
        @is_special (bool=False): Defines if given path is special.

        >return (list[Thread]): Not ran threads.
    """
    threads_list = []

    for path in source_paths:
        thread = threading.Thread(target=start_handling_thread, args=[path, settings, is_special])
        threads_list.append(thread)

    return threads_list


# Check command line settings.
CMDLINE_SETTINGS = {
    'show_stats': False,
    'console_log_startup': False,
    'no_warnings': False
}

if '--display-stats' in sys.argv:
    CMDLINE_SETTINGS['show_stats'] = True

if '--console-log' in sys.argv:
    CMDLINE_SETTINGS['console_log_startup'] = True

if '--no-warns' in sys.argv:
    CMDLINE_SETTINGS['no_warnings'] = True


# Check if program is ran with --help param.
if '--help' in sys.argv:
    display.terminal_custom('FileWatch help', '''
    
    Program documentation can be found on it's GitHub page:
    https://github.com/gental-py/FileWatch

    Available params:
    --display-stats: displays logs amount for each path live time
    --console-log: show startup process
    --no-warns: don't display warnings
    ''')
    sys.exit()

# Check files health.
structure.check_program_files(CMDLINE_SETTINGS['console_log_startup'])

# Get configuration.
configuration = Configuration(config.create_config(
    CMDLINE_SETTINGS['console_log_startup'],
    CMDLINE_SETTINGS['no_warnings']
))

# Create thread that will check logs file sizes
# and alert files with bigger size than in user config.
if configuration.logs_size_alert_gb > 0:
    threading.Thread(
        target=structure.control_files_size,
        args=[configuration.logs_size_alert_gb],
        daemon=True
    ).start()

# Check if ONLY_SPECIALS is enabled and SPECIALS list is not empty.
special_paths = configuration.specials

# Check if any special path is same as disk path.
for special_path in special_paths:
    if special_path in structure.ALL_DISKS:
        special_paths.remove(special_path)

if configuration.only_specials:
    if not special_paths:
        if CMDLINE_SETTINGS['console_log_startup']:
            display.terminal_error("Specials list is empty but ONLY_SPECIALS mode is enabled.")

        else:
            display.message_box_error(
                "Specials list is empty.",
                "Cannot run.\nONLY_SPECIALS mode is enabled but SPECIALS list is empty"
            )
        sys.exit(1)

    # Create different watchdog event handler threads for all paths.
    threads = create_threads_list(special_paths, CMDLINE_SETTINGS, True)

    # Run all threads.
    [ thread.start() for thread in threads ]


else:
    # Split all disks into different threaded task and run them.
    disks_threads = create_threads_list(structure.ALL_DISKS, CMDLINE_SETTINGS)

    # Add special threads to threads_list.
    special_threads = create_threads_list(special_paths, CMDLINE_SETTINGS, True)

    # Combine two lists of threads together.
    threads = disks_threads + special_threads

    # Run all threads.
    [ thread.start() for thread in threads ]
