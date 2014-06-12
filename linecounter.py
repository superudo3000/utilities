#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Line Counter
~~~~~~~~~~~~

Count the lines in given files.

Multiple patterns with shell-style wildcards (``*`` for
everything, ``?`` for any single character) are accepted.

Example usage and output::

    $> python linecounter.py /some/path *.php *.html *.css

    *.css:      982 lines
    *.py:     4.739 lines
    *.xhtml:  2.218 lines
    ---------------------
    total:    7.939 lines

It returns the total for each pattern and an overall total.

Be aware that files will be included multiple times if you
specify overlapping patterns and so the result might not be
what you expected.

Python 2.5 is required.

:Copyright: 2005-2007 Jochen Kupperschmidt
:Date: 12-Jul-2007
:License: MIT
"""

from __future__ import with_statement
from glob import iglob
import locale
locale.setlocale(locale.LC_ALL, '')
from optparse import OptionParser
import os


def count_lines(filename):
    """Count lines in file."""
    with open(filename, 'rb') as f:
        return sum(1 for line in f)

def walk(top):
    """Walk file system tree and return directory names."""
    yield top
    for name in os.listdir(top):
        name = os.path.join(top, name)
        if os.path.isdir(name) and not os.path.islink(name):
            for dir in walk(name):
                yield dir

def match_filenames(path, patterns, callback):
    """Find files matching the pattern and count their lines."""
    for dir in walk(path):
        for pattern in patterns:
            for filename in iglob(os.path.join(dir, pattern)):
                line_count = count_lines(filename)
                callback(filename, line_count)
                yield pattern, line_count

def process_files(path, patterns, callback):
    """Collect line count statistics."""
    stats = dict.fromkeys(patterns, 0)
    for pattern, line_count in match_filenames(
            path, patterns, callback):
        stats[pattern] += line_count
    return stats

def format_thousands(number):
    """Format number with thousands separated."""
    return locale.format('%d', number, True)

def display_results(stats):
    total = format_thousands(sum(stats.values()))
    key_width = max(len(k) for k in stats.keys() + ['total'])
    value_width = len(total)
    format = '%%-%ds  %%%ds lines' % (key_width + 1, value_width)
    print
    for key in sorted(stats.iterkeys()):
        print format % (key + ':', format_thousands(stats[key]))
    total_line = format % ('total:', total)
    print '-' * len(total_line)
    print total_line

if __name__ == '__main__':
    parser = OptionParser(
        usage='%prog [options] <path> [patterns]')
    parser.add_option('-a', '--absolute', dest='absolute',
        action='store_true',
        help='show absolute paths in details (overrides `-r`)')
    parser.add_option('-d', '--details', dest='details',
        action='store_true',
        help='show details for each file')
    parser.add_option('-r', '--relative', dest='relative',
        action='store_true',
        help='show relative paths in details')

    opts, args = parser.parse_args()
    if not args:
        parser.print_help()
        parser.exit()
    path, patterns = args[0], args[1:]

    def callback(filename, line_count):
        if opts.details:
            path_len = len(path)
            if opts.absolute:
                filename = os.path.abspath(filename)
            elif opts.relative:
                filename = '.' + filename[path_len:]
            print '%5d %s' % (line_count, filename)

    stats = process_files(path, patterns, callback)
    display_results(stats)
