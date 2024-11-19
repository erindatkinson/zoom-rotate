#!/usr/bin/env python3
"""zoom-rotate: a program to download/rotate zoom backgrounds"""
# piplib imports
from fire import Fire
# locallib imports
from lib.download import download
from lib.rotate import rotate

if __name__ == '__main__':
    Fire({
        "download": download,
        "rotate": rotate
    })
