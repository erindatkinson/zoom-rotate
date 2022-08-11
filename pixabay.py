from random import randint
from requests import get
from os.path import splitext, join

def get_imageset(config: dict) -> list:
  """pulls the api credentials/urls from the config dict given, calls the search endpoint, and returns a list of result
  objects. Raises Exception if API limit has been hit.
  """
  search_payload = {
      "q": config["api_query"],
      "per_page": 50,
      "order": "latest",
      "page": randint(1,10),
      "orientation": "horizontal",
      "category": "nature",
      "key": config["pixabay_api_key"]
    }

  resp = get(config["pixabay_prefix"], params=search_payload)
  if resp.status_code == 200:
    remaining = dict(resp.headers)["X-RateLimit-Remaining"]
    print(f"API Query Limit Remaining this Hour: {remaining}")
    return resp.json()["hits"]
  else:
    raise Exception(f"status code: {resp.status_code}\n{resp.text}")


def download_image(config: dict, image:dict):
  """pulls the base path from the given config, and the api object for an image in pixabay and downloads the
  high resolution image to the 'images' directory in the base path.
  """
  download_dir = join(config["base_dir"], "images")
  filetype = splitext(image["largeImageURL"])
  resp = get(image["largeImageURL"], stream=True)

  with open(f"{download_dir}/{image['id']}{filetype[1]}", 'wb') as fp:
    for chunk in resp.iter_content(chunk_size=128):
      fp.write(chunk)
