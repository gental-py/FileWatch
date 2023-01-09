import display
import files
import json

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

    def __init__(self, config: dict) -> None:
        
        self.__config__ = config

        self.SKIP_TEMP = config["skip_temp"]
        self.SKIP_LOG = config["skip_log"]
        self.SKIP_CUSTOM = config["skip_custom"]
        self.SPECIALS = config["specials"]
        self.LOGS_SIZE_ALERT_GB = config["logs_size_alert_gb"]
        self.ONLY_SPECIALS = config["only_specials"]
        self.LOG_EDITS = config["log_edits"]


def createConfig() -> dict:
    
    # Define config as default.
    config = DEFAULT_CONFIG

    # Get values from json config.
    try:
        with open(files.CONFIG_FILE_PATH, "r", encoding="utf8") as file_obj:
            user_config = json.loads(file_obj.read())
    except Exception as Error:
        display.warning("Cannot load user configuration", f"Error while loading config: {Error}\nProgram is starting with default config.")
        return config

    # Check if config is dict.
    if not isinstance(user_config, dict):
        display.warning("Cannot laod user configuration", "Invalid file content format.")
        return config

    # Overwrite values from default config with user_config.
    for key, value in user_config.items():
        if key in config:
            config[key] = value

    return config
    
def changeConfig(key, value) -> None:
    """ Change value of key in config file. """

    current_config = createConfig()
    new_config = current_config[key] = value

    with open(files.CONFIG_FILE_PATH, 'w+', encoding="utf8") as file:
        json.dump(new_config, file, indent=4, separators=(',',': '))

def resetConfig() -> None:
    """ Reset all values of config to DEFAULT_CONFIG values. """
    
    with open(files.CONFIG_FILE_PATH, 'w+', encoding="utf8") as file:
        json.dump(DEFAULT_CONFIG, file, indent=4, separators=(',',': '))

