"""placeholder for updated acception"""
# locallib imports
from .config import load_config
from .db import mark_pictures

def approve(selection=tuple(), yes_all=False, config_file="./config.ini") -> None:
    """Approve takes the comma separated ids given and moves the corresponding files in
    the images directory into the approved directory and marks it as 'approved' in the
    local database. (Usage: `main.py approve 11234,` or `main.py approve 11234,23455`)
    """
    mark_pictures(selection, "approve", load_config(config_file), yes_all)

def reject(selection=tuple(), no_all=False, config_file="./config.ini") -> None:
    """Reject takes the comma separated ids given and deletes the corresponding files in
    the images directory and marks it as 'rejected' in the local database.
    (Usage: `main.py reject 12345`, or `main.py reject 23456,34567`"""
    mark_pictures(selection, "reject", load_config(config_file), no_all)
