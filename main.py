#!/usr/bin/env python3
# pip/global imports
from contextlib import closing
from fire import Fire
from os import listdir, makedirs
from os.path import join
from random import choice
from shutil import copyfile, move

# local module imports
from db import db_conn, create, find_picture, add_picture, mark_pictures
from pixabay import get_imageset, download_image
from config import load_config

def Download(config_file="./config.ini") -> None:
  """Download takes the config provided, and gets a random page of the search results from pixabay based on your api
  query. It then downloads any images in that page that have not been previously downloaded."""
  config = load_config(config_file)
  makedirs(join(config["base_dir"], "images"), exist_ok=True)
  with closing(db_conn(config)) as conn:
    create(conn)
    imageset = get_imageset(config)

    for image in imageset:
      if find_picture(conn, image["id"]) is not None:
        continue
      download_image(config, image)
      add_picture(conn, image["id"])

def Rotate(config_file="./config.ini") -> None:
  """Rotate takes the config provided, and chooses a random image within the approved set of images and copies it to the
  zoom image location specified, rotating the background. Zoom must either have video turned off/on (within a meeting) or
  a new meeting started to refresh the image."""
  config = load_config(config_file)
  approved_dir = join(config["base_dir"], "approved")
  try:
    downloads = listdir(approved_dir)
    image = choice(downloads)
  except FileNotFoundError as fnfe:
    print("No images to rotate.")
  print(f"copying {join(approved_dir, image)} to {config['zoom_image']}")
  copyfile(join(approved_dir, image), config["zoom_image"])

def Approve(selection:tuple, config_file="./config.ini") -> None:
  """Approve takes the comma separated ids given and moves the corresponding files in the images directory into the approved directory and
  marks it as 'approved' in the local database. (Usage: `main.py approve 11234,` or `main.py approve 11234,23455`)
  """
  mark_pictures(selection, "approve", load_config(config_file))

def Reject(selection:tuple, config_file="./config.ini") -> None:
  """Reject takes the comma separated ids given and deletes the corresponding files in the images directory and
  marks it as 'rejected' in the local database. (Usage: `main.py reject 12345`, or `main.py reject 23456,34567`"""
  mark_pictures(selection, "reject", load_config(config_file))


if __name__ == '__main__':
  Fire({
    "download": Download,
    "rotate": Rotate,
    "approve": Approve,
    "reject": Reject
  })
