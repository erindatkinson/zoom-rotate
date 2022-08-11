from configparser import ConfigParser

def load_config(config_file:str) -> dict:
  """reads in the config file given and parses it into a dict object."""
  config = ConfigParser()
  config.read(config_file)
  return dict(config["core"])
