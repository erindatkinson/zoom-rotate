"""module to interface with the pixabay search api"""
# builtin imports
from os.path import splitext, join
from random import randint
# piplib imports
from requests import get
# locallib imports
from .logger import Log

class DownloadException(Exception):
    """exception for downloads"""

def get_imageset(config: dict) -> list:
    """pulls the api credentials/urls from the config dict given, calls the search endpoint,
    and returns a list of result objects. Raises Exception if API limit has been hit.
    """
    search_payload = {
        "q": config["api_query"],
        "per_page": 50,
        "order": "latest",
        "page": randint(1,10),
        "orientation": "horizontal",
        "category": "nature",
        "image_type": "photo",
        "key": config["pixabay_api_key"]
      }

    resp = get(
        config["pixabay_prefix"],
        params=search_payload,
        timeout=int(config['pixabay_timeout']))
    if resp.status_code == 200:
        remaining = dict(resp.headers)["X-RateLimit-Remaining"]
        Log.info(f"API Query Limit Remaining this Hour: {remaining}")
        hits = resp.json()["hits"]
        Log.debug("query response", hits=hits)
        return hits

    raise DownloadException(f"status code: {resp.status_code}\n{resp.text}")


def download_image(config: dict, image:dict):
    """pulls the base path from the given config, and the api object for an image in
    pixabay and downloads the high resolution image to the 'images' directory in the base path.
    """
    download_dir = join(config["base_dir"], "images")
    filetype = splitext(image["largeImageURL"])
    filename = f"{image['id']}{filetype[1]}"
    resp = get(image["largeImageURL"], stream=True, timeout=int(config["pixabay_timeout"]))
    Log.debug("downloaded file", file=filename)
    if resp.status_code != 200:
        Log.error("error on downloading", file=filename, status_code=resp.status_code)
    with open(f"{download_dir}/{filename}", 'wb') as fp:
        for chunk in resp.iter_content(chunk_size=128):
            fp.write(chunk)
