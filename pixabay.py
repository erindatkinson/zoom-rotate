from random import randint
from requests import get
from os.path import splitext, join

def get_imageset(config: dict) -> list:
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
  download_dir = join(config["base_dir"], "images")
  filetype = splitext(image["largeImageURL"])
  resp = get(image["largeImageURL"], stream=True)

  with open(f"{download_dir}/{image['id']}{filetype[1]}", 'wb') as fp:
    for chunk in resp.iter_content(chunk_size=128):
      fp.write(chunk)
