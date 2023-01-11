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
        self.log_path = files.SPECIAL_LOGS_FILE_PATH if is_special else files.make_path_for_disk(path) 
        self.initWatchdog()

    def initWatchdog(self):
        observer = Observer()
        observer.schedule(self, self.path, True)
        observer.start()

        try:
            while 1:
                pass
        finally:
            display.message_box_warning(f"{self.path}'s disk handler", "Main watchdog loop has been terminated.")
            observer.stop()
            observer.join()

    def logEvent(self, event):
        log = logs.format_log(event)

        # Check if src_path is in registered as special.
        if event.src_path in self.config.specials:
            logs.write_log(files.SPECIAL_LOGS_FILE_PATH, log)

        # Skip logs with temp phrase in it.
        if self.config.skip_temp:
            if logs.is_any_phrase_in_log(logs.TEMP_PHRASES, log):
                return
        
        # Skip logs with log phrase in it.
        if self.config.skip_log:
            if logs.is_any_phrase_in_log(logs.LOG_PHRASES, log):
                return   

        if logs.is_any_phrase_in_log(self.config.skip_custom, log):
            return

        # Save log to file.
        logs.write_log(self.log_path, log)


    # ---- LOG EVENTS ---- #
    def on_created(self, event):
        self.logEvent(event)

    def on_deleted(self, event):
        self.logEvent(event)

    def on_moved(self, event):
        self.logEvent(event)

    def on_modified(self, event): 
        if self.config.log_edits:
            self.logEvent(event)