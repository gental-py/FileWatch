from config import Configuration
import threading
import display
import handle
import config
import files


# Check files health.
created_files = files.checkFiles()

# Display information if any files were created.
if created_files:
    display.info("Missing files created.", "List of created files: \n\n"+"\n".join(created_files))

# Get configuration.
configuration = Configuration(config.createConfig())

# Create thread that will check logs file sizes
# and alert files with bigger size than in user config.
if configuration.LOGS_SIZE_ALERT_GB > 0:
    threading.Thread(target=files.controlFilesSize, args=[configuration.LOGS_SIZE_ALERT_GB], daemon=True).start()

# Start handle thread.
def startHandlingThread(path, is_special=False):
    handle.DiskHandler(path, configuration, is_special)

# Check if ONLY_SPECIALS is enabled and SPECIALS list is not empty.
specials = configuration.SPECIALS
if configuration.ONLY_SPECIALS:
    if not len(specials):
        display.error("Specials list is empty.", "Cannot run.\nONLY_SPECIALS mode is enabled but SPECIALS list is empty")
        exit()

    # Create different watchdog event handler threads for all paths.
    threads_list = []
    for path in specials:
        thread = threading.Thread(target=startHandlingThread, args=[path, True])
        threads_list.append(thread)

    # Run all threads.
    [ thread.start() for thread in threads_list ]

else:
    # Split all disks into different threaded task and run them.   
    threads_list = []
    for disk in files.ALL_DISKS:
        thread = threading.Thread(target=startHandlingThread, args=[disk])
        threads_list.append(thread)
    
    # Add special threads to threads_list.
    for path in specials:
        thread = threading.Thread(target=startHandlingThread, args=[path, True])
        threads_list.append(thread)

    # Run all threads.
    [ thread.start() for thread in threads_list ]
