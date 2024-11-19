"""module for rotating images"""
# builtin imports
from os import listdir
from os.path import join
from random import choice
from shutil import copyfile
# locallib imports
from .config import load_config
from .logger import Log

def rotate(config_file="./config.ini") -> None:
    """Rotate takes the config provided, and chooses a random image within the approved
    set of images and copies it to the zoom image location specified, rotating the
    background. Zoom must either have video turned off/on (within a meeting) or
    a new meeting started to refresh the image."""
    config = load_config(config_file)
    approved_dir = join(config["base_dir"], "approved")

    try:
        downloads = listdir(approved_dir)
        image = choice(downloads)
    except FileNotFoundError:
        Log.error("No images to rotate.")

    Log.info(f"copying {join(approved_dir, image)} to {config['zoom_image']}")
    copyfile(join(approved_dir, image), config["zoom_image"])
