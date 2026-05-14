"""get singleton"""
from pprint import pprint
from .pixabay import get_image
from .config import load_config
def get(img_id:str, verify:bool=False, config_file="./config.ini")->None:
    """get info on file"""
    config = load_config(config_file)
    pprint(get_image(img_id, config, verify))
