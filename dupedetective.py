#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Dupe Detective
==============

Find duplicate files.

For the sake of speed, files are compared by size as the first step.  Only if
multiple files have the same size, MD5 hashes of their contents are calculated
to figure out if they are really identical.

Alternatives to MD5 include ``adler32()`` and ``crc32()`` from ``zlib``.  They
are much faster, although they have their own weaknesses, and especially
Adler-32 looks bad when little data is available.

:Copyright: 2008 Jochen Kupperschmidt
:Date: 16-May-2008
:License: MIT
"""

from __future__ import with_statement
from collections import defaultdict
import fnmatch
import hashlib
from itertools import ifilter
import os
import sys


def get_filenames(path, filemask):
    """Walk path recursively and yield filenames."""
    for root, dirs, files in os.walk(path):
        for filename in fnmatch.filter(files, filemask):
            yield os.path.join(root, filename)

def read_file(filename, block_size=8192):
    """Iterate block-wise over file contents."""
    with open(filename, 'rb') as f:
        for block in iter(lambda: f.read(block_size), ''):
            yield block

def calc_hash(iterable):
    """Calculate the MD5 hash for the iterable's data."""
    return reduce(lambda m, data: m.update(data) or m,
        iterable, hashlib.md5()).hexdigest()

def filter_groups(iterable, key_func):
    """Extract value sequences with more than one element."""
    d = defaultdict(set)
    for item in iterable:
        d[key_func(item)].add(item)
    return ifilter(lambda x: len(x[1]) > 1, d.iteritems())

def find_duplicates(iterable):
    """Compare file size and, if equal, hash sums."""
    def _get_size(filename):
        return int(os.path.getsize(filename))

    def _calc_hash(filename):
        return calc_hash(read_file(filename))

    for size, fnames in filter_groups(iterable, _get_size):
        for hash, fnames2 in filter_groups(fnames, _calc_hash):
            yield size, hash, fnames2

def main(path, mask='*'):
    """Retrieve and display results."""
    duplicates = list(find_duplicates(get_filenames(path, mask)))
    if not duplicates:
        return
    print 'The following files are duplicates:'
    for size, hash, filenames in duplicates:
        print '\n + %s, %d bytes' % (hash, size)
        for filename in filenames:
            print '   -', filename

if __name__ == '__main__':
    if len(sys.argv) not in (2, 3):
        print 'usage: %s <path> [mask pattern]' % os.path.basename(sys.argv[0])
        sys.exit(2)
    main(*sys.argv[1:])
