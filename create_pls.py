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

from itertools import ifilter
import os.path
import re
from sys import argv, exit, stdout


PATTERN = re.compile('\.(mp3|ogg)$', re.I)


def find_files(path):
    """Return all matching files beneath the path."""
    for root, dirs, files in os.walk(os.path.abspath(path)):
        for fn in ifilter(PATTERN.search, files):
            yield os.path.join(root, fn)


def create_playlist(filenames):
    """Create a PLS playlist from filenames."""
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
        'NumberOfEntries=%d\n'
        'Version=2\n') % number


def create_track_entry(number, filename):
    """Create a track entry."""
    title = os.path.splitext(os.path.basename(filename))[0]

    return {
        'number': number,
        'file': filename,
        'title': title,
    }


if __name__ == '__main__':
    if len(argv) != 2:
        exit('Usage: %s <path to music files>' % os.path.basename(argv[0]))

    filenames = find_files(argv[1])
    map(stdout.write, create_playlist(filenames))
