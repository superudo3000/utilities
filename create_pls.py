#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Create a ``.pls`` playlist from music filenames.

Specify a path to be recursively searched for music files.

Requires Python 3.3 and the `pathlib` module, or Python 3.4+.

According to an `unofficial PLS format specification`__, the attribute
``NumberOfEntries`` can be placed *after* all entries.  This allows to
iterate through filenames without keeping details for each entry in
memory.

__ http://forums.winamp.com/showthread.php?threadid=65772

:Copyright: 2007-2016 Jochen Kupperschmidt
:Date: 2016-03-28 (original release: 09-Feb-2007)
:License: MIT
:Website: http://homework.nwsnet.de/releases/1a02/#create-pls-playlists
"""

from argparse import ArgumentParser
from itertools import count
import os.path
from pathlib import Path
import re
from sys import stdout


PATTERN = re.compile('\.(mp3|ogg)$', re.I)


def parse_args():
    """Parse command line arguments."""
    parser = ArgumentParser()
    parser.add_argument('path', type=Path)

    return parser.parse_args()


def find_files(path):
    """Return all matching files beneath the path."""
    for root, dirs, files in os.walk(str(path)):
        for fn in filter(PATTERN.search, files):
            filename = os.path.join(root, fn)
            yield Path(filename)


def generate_playlist(filenames):
    """Generate a PLS playlist from filenames."""
    yield '[playlist]\n\n'

    total = 0

    entry_template = (
        'File{number:d}={file}\n'
        'Title{number:d}={title}\n'
        'Length{number:d}=-1\n\n')

    for track_entry in generate_track_entries(filenames):
        total += 1
        yield entry_template.format(**track_entry)

    yield (
        'NumberOfEntries={:d}\n'
        'Version=2\n').format(total)


def generate_track_entries(filenames, start_number=1):
    """Generate track entries."""
    numbers = count(start_number)
    for number, filename in zip(numbers, filenames):
        yield create_track_entry(number, filename)


def create_track_entry(number, path):
    """Create a track entry."""
    title = path.stem

    return {
        'number': number,
        'file': path,
        'title': title,
    }


if __name__ == '__main__':
    args = parse_args()
    paths = find_files(args.path)
    stdout.writelines(generate_playlist(paths))
