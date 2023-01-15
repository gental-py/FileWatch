from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import structure
import display
import config
import stats
import logs


class DiskHandler(FileSystemEventHandler):
    """ Handle events for disk with given letter. """

    def __init__(self, path: str, configuration: config.Configuration, is_special: bool = False, cmd_line_settings: dict = {}) -> None:
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
        self.show_stats = cmd_line_settings['show_stats']
        self.no_warnings = cmd_line_settings['no_warnings']
        self.console_log_startup = cmd_line_settings['console_log_startup']
        self.log_path = structure.SPECIAL_LOGS_FILE_PATH if is_special else structure.make_path_for_disk(path) 
        self.init_watchdog()

    def init_watchdog(self):
        observer = Observer()
        observer.schedule(self, self.path, True)
        observer.start()

        if self.console_log_startup:
            display.terminal_info(f'Started watchdog for: [{self.path}]')

        try:
            while 1:
                pass

        finally:
            if not self.no_warnings:
                display.message_box_warning(f"{self.path}'s disk handler", "Main watchdog loop has been terminated.")
            observer.stop()
            observer.join()

    def log_event(self, event):
        log = logs.format_log(event)

        # Check if src_path is in registered as special.
        if event.src_path in self.config.specials:
            logs.write_log(structure.SPECIAL_LOGS_FILE_PATH, log)

        # Skip logs with temp phrase in it.
        if self.config.skip_temp:
            if logs.is_any_phrase_in_log(logs.TEMP_PHRASES, log):
                return
        
        # Skip logs with log phrase in it.
        if self.config.skip_log:
            if logs.is_any_phrase_in_log(logs.LOG_PHRASES, log):
                return   

        # Skip logs with custom phrases.
        if logs.is_any_phrase_in_log(self.config.skip_custom, log):
            return

        # Skip log with Filewatch directory.
        if structure.MAIN_DIRECTORY in event.src_path:
            return 

        # Save log to file.
        logs.write_log(self.log_path, log)

        # Move log to the stats viewer.
        if self.show_stats:
            stats.handle(self.path, event.event_type)


    # ---- LOG EVENTS ---- #
    def on_created(self, event):
        self.log_event(event)

    def on_deleted(self, event):
        self.log_event(event)

    def on_moved(self, event):
        self.log_event(event)

    def on_modified(self, event): 
        if self.config.log_edits:
            self.log_event(event)