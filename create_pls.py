#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Create ``.pls`` playlists from music filenames.

Specify a path to be recursively searched for music files.

According to an `unofficial PLS format specification`__, the attribute
``NumberOfEntries`` can be placed *after* all entries.  This allows to iterate
through filenames without keeping details for each entry in memory.

__ http://forums.winamp.com/showthread.php?threadid=65772

:Copyright: 2007 Jochen Kupperschmidt
:Date: 09-Feb-2007
:License: MIT
"""

from argparse import ArgumentParser
try:
    from itertools import ifilter as filter  # Python 2
except ImportError:
    pass
import os.path
import re
from sys import stdout


PATTERN = re.compile('\.(mp3|ogg)$', re.I)


def parse_args():
    """Parse command line arguments."""
    parser = ArgumentParser()
    parser.add_argument('path')

    return parser.parse_args()


def find_files(path):
    """Return all matching files beneath the path."""
    for root, dirs, files in os.walk(os.path.abspath(path)):
        for fn in filter(PATTERN.search, files):
            yield os.path.join(root, fn)


def generate_playlist(filenames):
    """Generate a PLS playlist from filenames."""
    yield '[playlist]\n\n'

    number = 0

    entry = (
        'File{number:d}={file}\n'
        'Title{number:d}={title}\n'
        'Length{number:d}=-1\n\n')
    for filename in filenames:
        number += 1
        track_entry = create_track_entry(number, filename)

        yield entry.format(**track_entry)

    yield (
        'NumberOfEntries={:d}\n'
        'Version=2\n').format(number)


def create_track_entry(number, filename):
    """Create a track entry."""
    title = os.path.splitext(os.path.basename(filename))[0]

    return {
        'number': number,
        'file': filename,
        'title': title,
    }


if __name__ == '__main__':
    args = parse_args()
    filenames = find_files(args.path)
    stdout.writelines(generate_playlist(filenames))
