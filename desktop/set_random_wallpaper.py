#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Randomly select and set a wallpaper from the given directory.

Requires Python_ 3.4+ and feh_ to be installed.

.. _Python: https://www.python.org/
.. _feh:    http://feh.finalrewind.org/

:Copyright: 2012-2016 Jochen Kupperschmidt
:License: MIT
:Version: 19-Jan-2016
"""

from argparse import ArgumentParser
from pathlib import Path
from random import choice
import subprocess


EXTENSIONS = frozenset(['gif', 'jpg', 'jpeg', 'png'])


def parse_args():
    """Extract the images path from the command line arguments."""
    parser = ArgumentParser()
    parser.add_argument('images_path', type=Path)
    return parser.parse_args()


def collect_filenames(path):
    """Yield files in the path whose names match one of the extensions."""
    for extension in EXTENSIONS:
        pattern = '*.' + extension
        yield from path.glob(pattern)


def set_wallpaper(filename):
    """Set the wallpaper using feh."""
    print('Changing wallpaper to:', filename)
    subprocess.Popen(['feh', '--bg-fill', filename])


def main(path):
    if not path.exists():
        raise FileNotFoundError('Path does not exist: {}'.format(path))

    filenames = list(collect_filenames(path))
    if not filenames:
        raise FileNotFoundError(
                'Path does not contain matching images: {}'.format(path))

    random_filename = choice(filenames)
    set_wallpaper(str(random_filename))


if __name__ == '__main__':
    args = parse_args()
    main(args.images_path)
