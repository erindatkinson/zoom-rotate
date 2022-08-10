# Zoom Rotate

A helpful way to take the pressure off choosing what zoom background you have.

![photo taken from under an outcropping of a waterfall in a forest with light shining through the falling water](assets/3719233.jpg)



## Introduction

Have you ever spent 10 minutes a day every day for about 6 months manually curating which pretty background you wanted for that day in your zoom?

"There's gotta be a better way!"

## Installation

### Prerequisites

* Python
* Pipenv
* [A Pixabay API Key](#obtaining-a-pixabay-api-key)

### Install

Run `make install` to install the pip requisites.

You can run `pipenv run ./main.py --help` to verify that the install worked correctly.

### Configuration

To start, copy the `config.ini.example` file to `config.ini` in the directory and update the `API_QUERY` param to whatever search string you'd like. (I like autumn)

#### Obtaining a Pixabay API Key

The easiest way to get the pixabay API key is to sign up for Pixabay, and navigate to [this page](https://pixabay.com/api/docs/#api_search_images). You will either see `key (required) 	str 	Please login to see your API key here. Login | Signup` if you're not logged in, or  `Your API key: 12345678-abcdef0123456789abcdef012` (but with your key) if you are.

Once you've obtained your key, add the key to the `PIXABAY_API_KEY` in the `config.ini` file

#### Setting up Zoom

You will need to have added at least one image as a custom background to your zoom application that you're willing to have be erased as the "rotating" zoom image.

Once you've added your image (feel free to use the jpeg in the assets/ directory if you don't have one at hand), you'll need to navigate to where the custom images are stored.

* For macbooks, this is usually `/Users/USER_NAME/Library/Application Support/zoom.us/data/VirtualBkgnd_Custom`
* For windows, this is usually `C:\Users\USER_NAME\AppData\Roaming\Zoom\data\VirtualBkgnd_Custom`
* For linux, this is usually, `/home/USER_NAME/.zoom/data/VirtualBkgnd_Custom`

If you've added more than one custom image, you may want to open them each in either like Firefox or an image previewer that handles extensionless files to find the one you're looking for.
Once you have that, add the full path to your file in the style of `/path/to/VirtualBkgnd_Custom/BB74FD98-2E23-4E79-B01E-EDCB8D68253D` to the parameter `ZOOM_IMAGE`

#### Setting up the database

In your `config.ini` file update the `BASE_DIR` param with the full path to the current working directory (the root of the repo).

Additionally, update the `DB_LOCATION` param with the same path you used in the `BASE_DIR` but append the file `db.sqlite` to the path. (eg. if your base dir is `/home/USER_NAME/.local/zoom-rotate/` your db location would be `/home/USER_NAME/.local/zoom-rotate/db.sqlite`)

### Running the tool

#### Downloading images

You should be able to run `make get` and an `images` folder should appear in your repo and images should start to download that match your search query.

#### Approving/Rejecting images

If you want to just move good images over to an `approved` folder, you can, but if you go through the application, it'll store the ones you've approved in the db as well and not redownload them.

To approve:

* For each image `0123456.jpg`, `1234567.jpg` that you want to approve
  * Run `pipenv run ./main.py approve 0123456,1234567`
* If you only want to approve a single image
  * Run `pipenv run ./main.py approve 0123456,` (the ending comma is for being able to type it correctly from the Fire library.)

To reject:

* For each image `0123456.jpg`, `1234567.jpg` that you want to reject
  * Run `pipenv run ./main.py reject 0123456,1234567`
  * Similar caveats for single image rejections apply from the approvals.

Rejected images are deleted but retain a record in the db so if they get pulled in the search query they won't be downloaded.

#### Rotating Images

If you'd like to rotate using some other method, you can look at the [examples](examples/) directory, but otherwise you can run:

```shell
pipenv run ./main.py rotate
```

if you are going to make an alias for this to run from anywhere you'll want to run it in the style of:

```shell
pipenv run /path/to/repo/main.py rotate --config_file /path/to/repo/config.ini
```

