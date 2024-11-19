"""module for reading config"""
# piplib imports
from configparser import ConfigParser
# locallib imports
from .logger import Log, init_logger

def load_config(config_file:str) -> dict:
    """reads in the config file given and parses it into a dict object."""
    config = ConfigParser()
    config.read(config_file)
    init_logger(config["core"])
    Log.debug("read config")
    return dict(config["core"])
