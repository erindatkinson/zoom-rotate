from configparser import ConfigParser

def load_config(config_file:str) -> dict:
  config = ConfigParser()
  config.read(config_file)
  return dict(config["core"])