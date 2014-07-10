#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Repository Sorter
=================

Recursively search files in a directory for ``$Id ... $`` identifier strings
and show a list of matching files, ordered by the date of their latest change
(according to the identifier).

Supports Subversion (SVN), CVS, and RCS.

:Copyright: 2006 Jochen Kupperschmidt
:Date: 12-May-2006
:License: MIT
"""

from __future__ import with_statement
from itertools import islice
from optparse import OptionParser
import os
import re


# Configuration
BINARY_SUFFIXES = set((
    'gif', 'jpg', 'jpeg', 'png', 'tga', 'tif',
    'class', 'pyc',
    'bz2', 'gz', 'rar', 'tar', 'zip'))  # ...


RE_SVN_ID = re.compile('''
    .*
    \$Id:                           # Id string prefix
    \ (?P<filename>.+)              # filename
    \ (?P<version>\d+)              # file revision
    \ (?P<date>\d{4}-\d{2}-\d{2})   # last change's date
    \ (?P<time>\d{2}:\d{2}:\d{2})Z  # last change's time
    \ (?P<author>.+)                # last change's author's name
    \ \$                            # Id string suffix
    .*
    ''', re.VERBOSE)

RE_RCS_ID = re.compile('''
    .*
    \$Id:                           # Id string prefix
    \ (?P<filename>.+),v            # filename
    \ (?P<version>\d+.\d+)          # file version
    \ (?P<date>\d{4}/\d{2}/\d{2})   # last change's date
    \ (?P<time>\d{2}:\d{2}:\d{2})   # last change's time
    \ (?P<author>.+)                # last change's author's name
    \ Exp\ \$                       # Id string suffix
    .*
    ''', re.VERBOSE)

TYPES = {
    'svn': ('.svn', RE_SVN_ID),
    'cvs': ('CVS', RE_RCS_ID),
    'rcs': ('RCS', RE_RCS_ID),
}


def autodetect_type(directory):
    """Try to autodetect the repository type by folder names."""
    entries = os.listdir(directory)
    for type_ in TYPES:
        if TYPES[type_][0] in entries:
            return type_


def find_id_line(f, max_lines):
    """Try to find a line containing the id keyword ``$Id$``."""
    for line in islice(f, max_lines):
        if '$Id' in line:
            return line


class Id(object):
    """An identifier."""

    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def __cmp__(self, other):
        """Specify the sort order of ``Id`` objects."""
        for attr in ['date', 'time', 'filename', 'version']:
            result = cmp(getattr(self, attr), getattr(other, attr))
            if result != 0:
                return result
        return 0

    @classmethod
    def parse_id(cls, line, type_):
        """Parse id string with compiled pattern."""
        m = TYPES[type_][1].match(line)
        if m is not None:
            return cls(**m.groupdict())


def scan_files(path, opts):
    """Scan through files, trying to find an id signature."""
    for root, dirs, files in os.walk(path):
        # Skip version control specific directories.
        for type_ in TYPES:
            vc_dir = TYPES[type_][0]
            if vc_dir in dirs:
                dirs.remove(vc_dir)

        for fname in files:
            # Skip defined binary file suffixes.
            if fname.split('.')[-1] in BINARY_SUFFIXES:
                continue

            # Open file and look for ident line.
            with open(os.path.join(root, fname), 'rb') as f:
                id_line = find_id_line(f, opts.num_lines)
            if id_line:
                id_ = Id.parse_id(id_line, opts.type)
                if id_ is not None:
                    yield id_


def parse_args():
    parser = OptionParser(
        usage='%prog [options] <directory>',
        version='Repository Sorter',
        description='Search files in a repository for ident strings'
                    ' and order the files by the date of their last change.'
        )

    parser.add_option(
        '-t', '--type',
        choices=TYPES.keys() + ['auto'],
        dest='type',
        default='auto',
        help='repository type: %s or auto (default)' % ', '.join(TYPES.keys())
        )

    parser.add_option(
        '-a', '--authors',
        action='store_true',
        dest='authors',
        default=False,
        help='display last authors')

    parser.add_option(
        '-n', '--num-lines',
        dest='num_lines',
        type='int',
        default=10,
        help='maximum number of lines to scan')

    # Process options and arguments.
    opts, args = parser.parse_args()
    if len(args) != 1:
        parser.print_help()
        parser.exit()

    # Autodetect repository type.
    if opts.type == 'auto':
        opts.type = autodetect_type(args[0])
        if opts.type is None:
            parser.exit(msg='Auto-detection of repository type failed.'
                            ' Please specify a type.\n')
        print('Auto-detection assumes this is a %s repository.\n'
              % opts.type.upper())

    return opts, args


def main():
    opts, args = parse_args()

    # Scan.
    ids = list(scan_files(args[0], opts))

    # Print sorted results.
    ids.sort()
    format = '%(date)s %(time)s %(filename)s'
    if opts.authors:
        format += ' [%(author)s]'
    for id_ in ids:
        print format % id_.__dict__

if __name__ == '__main__':
    main()
