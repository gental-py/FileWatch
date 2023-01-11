"""
Module: config.py
Contains default config, manages user config file.
"""

import json

import display
import files


DEFAULT_CONFIG = {
    "skip_temp": True,
    "skip_log": True,
    "skip_custom": [],
    "specials": [],
    "logs_size_alert_gb": 2,
    "only_specials": False,
    "log_edits": True
}

class Configuration:
    """ Represents configuration.
        All settings are stored as class attributes
        and as dictionary with __config__ attribute.
    """

    def __init__(self, config: dict) -> None:

        self.__config__ = config

        self.skip_temp = config["skip_temp"]
        self.skip_log = config["skip_log"]
        self.skip_custom = config["skip_custom"]
        self.specials = config["specials"]
        self.logs_size_alert_gb = config["logs_size_alert_gb"]
        self.only_specials = config["only_specials"]
        self.log_edits = config["log_edits"]


def create_config() -> dict:
    """ Creates configuration dictionary by overwriting
        default config with user configuration.
        Displays warning when some error with reading config occurs.
    """

    # Define config as default.
    config = DEFAULT_CONFIG

    # Get values from json config.
    try:
        with open(files.CONFIG_FILE_PATH, "r", encoding="utf8") as file_obj:
            user_config = json.loads(file_obj.read())

    except Exception as error:
        display.message_box_warning(
            "Cannot load user configuration",
            f"Config cannot be loaded: {error}\n(running with default)"
        )
        return config

    # Check if config is dict.
    if not isinstance(user_config, dict):
        display.message_box_warning("Cannot load user configuration", "Invalid file content format.")
        return config

    # Overwrite values from default config with user_config.
    for key, value in user_config.items():
        if key in config:
            config[key] = value

    return config

def change_config(key, value) -> None:
    """ Change value of key in config file. """

    current_config = create_config()
    new_config = current_config[key] = value

    with open(files.CONFIG_FILE_PATH, 'w+', encoding="utf8") as file:
        json.dump(new_config, file, indent=4, separators=(',',': '))

def reset_config() -> None:
    """ Reset all values of config to DEFAULT_CONFIG values. """

    with open(files.CONFIG_FILE_PATH, 'w+', encoding="utf8") as file:
        json.dump(DEFAULT_CONFIG, file, indent=4, separators=(',',': '))
