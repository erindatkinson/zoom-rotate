"""module for downloading"""
# builtin imports
from os import makedirs
from os.path import join
# piplib imports
from contextlib import closing
# locallib imports
from .config import load_config
from .db import db_conn, create, Connection, find_picture, add_picture
from .logger import Log
from .pixabay import get_imageset, download_image

def download(config_file="./config.ini") -> None:
    """Download takes the config provided, and gets a random page of the search results 
    from pixabay based on your api query. It then downloads any images in that page that
    have not been previously downloaded."""
    config = load_config(config_file)
    makedirs(join(config["base_dir"], "images"), exist_ok=True)

    with closing(db_conn(config)) as conn:
        create(conn)
        imageset = get_imageset(config)
        process_images(conn, config, imageset)



def process_images(conn:Connection, config:dict, imageset:list)->None:
    """loop thru images to process images"""
    for image in imageset:
        if "ai generated" in image["tags"]:
            Log.debug("skipping as ai generated", image=image)
            continue
        if find_picture(conn, image["id"]) is not None:
            Log.debug("skipping as already processed", image=image)
            continue
        Log.debug("downloading image", image=image)
        download_image(config, image)
        add_picture(conn, image["id"])
