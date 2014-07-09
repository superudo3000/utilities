#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""List the biggest files.

:Copyright: 2008-2014 Jochen Kupperschmidt
:Date: 09-Jul-2014 (original release: 20-Apr-2008)
:License: MIT
"""

from argparse import ArgumentParser
from glob import iglob
from heapq import heapify, heapreplace
from itertools import islice
import os


def get_files_info(path, pattern):
    """Yield the size and name of each file along the path."""
    for root, dirs, files in os.walk(path):
        for filename in iglob(os.path.join(root, pattern)):
            yield int(os.path.getsize(filename)), filename


def identify_biggest_files(files, limit):
    """Determine the biggest files.

    ``files``
        An iterable of ``(size, filename)`` tuples.
    ``limit``
        The maximum number of files to keep on the heap.  A lower value
        might result in slightly less memory usage.
    """
    # Create the initial heap.
    biggest = list(islice(files, limit))
    heapify(biggest)

    # Process remaining items.
    for file_tuple in files:
        if file_tuple > biggest[0]:
            heapreplace(biggest, file_tuple)

    # Sort and return the heap items.
    biggest.sort(reverse=True)
    return list(biggest)


def parse_args():
    parser = ArgumentParser(description='List the biggest files.')

    parser.add_argument(
        'path',
        metavar='PATH')

    parser.add_argument(
        '-m', '--max-files',
        dest='max_files',
        type=int,
        default=10,
        help='maximum number of files to show (default: 10)')

    parser.add_argument(
        '-p', '--pattern',
        dest='pattern',
        default='*',
        help='a pattern to narrow down the search, e.g. "*.txt"\n'
             ' NOTE: The pattern might need to be escaped, possibly '
             'using quotes or backslashes, depending on your shell.')

    return parser.parse_args()


def main():
    args = parse_args()
    files = get_files_info(args.path, args.pattern)
    biggest_files = identify_biggest_files(files, args.max_files)

    # Display biggest files.
    if biggest_files:
        tmpl = ' %%%dd  %%s' % len(str(biggest_files[0][0]))
        for file_tuple in biggest_files:
            print tmpl % file_tuple
    else:
        print 'No files were found.'


if __name__ == '__main__':
    main()
