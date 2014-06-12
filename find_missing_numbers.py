#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Find missing numbers in a range derived from file names.

This comes in handy to find the missing pieces in an enumerated list of files
named according to a pattern, e.g. documents with an identifier prefix,
music/podcast files, photos from a digital camera, segments of packed archives
etc.

It requires the path to the files and a `regular expression`_ pattern for
those to be given by the user.

.. _regular expression: http://en.wikipedia.org/wiki/Regular_expression
"""

import os
import re


def find_matches(pattern, iterable):
    """Apply regular expression to each item and yield matches.

    If the item doesn't match, nothing is yielded.

    Only the first match group is considered and expected to represent an
    integer.

    The yielded items are not necessarily sorted.
    """
    cp = re.compile(pattern)
    for item in iterable:
        match = cp.match(item)
        if match is not None:
            yield int(match.group(1))

def find_missing(iterable, start=1, stop=9999):
    """Find missing numbers in a range of integers."""
    # Keep only results within the given limits.
    iterable = frozenset(item for item in iterable if start <= item <= stop)

    # Build a range to compare the iterable's content to.
    comparison_range = xrange(start, max(iterable) + 1)

    # Return the difference.
    return frozenset(comparison_range).difference(iterable)

def main(path, pattern, **kwargs):
    filenames = os.listdir(path)
    matches = find_matches(pattern, filenames)
    missing = find_missing(matches, **kwargs)
    print 'Missing: ' + ', '.join(map(str, sorted(missing)))

# Example usage:
if __name__ == '__main__':
    # Scan audio tracks (e.g. ``04 - Some Song.mp3``).
    main(u'/my/music/album1', u'(\d{2}) - .+\.mp3')

    # Scan images (e.g. ``image0217.jpg``).
    main(u'/my/photos', u'image(\d{4})\.jpg')
