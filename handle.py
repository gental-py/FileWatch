from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import display
import config
import files
import logs


class DiskHandler(FileSystemEventHandler):
    """ Handle events for disk with given letter. """

    def __init__(self, path: str, configuration: config.Configuration, is_special: bool = False) -> None:
        if is_special:
            if path.endswith("\\"):
                self.path = path
            else:
                self.path = path + "\\"
        else:
            if ":" in path:
                self.path = path
            else:
                self.path = path + ":\\"
        self.config = configuration
        self.is_special = is_special
        self.log_path = files.SPECIAL_LOGS_FILE_PATH if is_special else files.makePathForDisk(path) 
        self.initWatchdog()

    def initWatchdog(self):
        observer = Observer()
        observer.schedule(self, self.path, True)
        observer.start()

        try:
            while 1:
                pass
        finally:
            display.warning(f"{self.path}'s disk handler", "Main watchdog loop has been terminated.")
            observer.stop()
            observer.join()

    def logEvent(self, event):
        log = logs.formatLog(event)

        # Check if src_path is in registered as special.
        if event.src_path in self.config.SPECIALS:
            logs.writeLog(files.SPECIAL_LOGS_FILE_PATH, log)

        # Skip logs with temp phrase in it.
        if self.config.SKIP_TEMP:
            if logs.isPhraseInLog(logs.temp_phrases, log):
                return
        
        # Skip logs with log phrase in it.
        if self.config.SKIP_LOG:
            if logs.isPhraseInLog(logs.log_phrases, log):
                return   

        if logs.isPhraseInLog(self.config.SKIP_CUSTOM, log):
            return

        # Save log to file.
        logs.writeLog(self.log_path, log)


    # ---- LOG EVENTS ---- #
    def on_created(self, event):
        self.logEvent(event)

    def on_deleted(self, event):
        self.logEvent(event)

    def on_moved(self, event):
        self.logEvent(event)

    def on_modified(self, event): 
        if self.config.LOG_EDITS:
            self.logEvent(event)