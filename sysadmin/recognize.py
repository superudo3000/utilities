#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File Recognizer
===============

This tool tries to aid in recognizing files after they were recovered (e.g.
after a hard drive failure) with some software that left them uniformly named.

It grabs the output of the UNIX ``file`` utility (a Windows binary is
available from ``http://gnuwin32.sourceforge.net/``) and moves files with a
specified type into accordant subdirectories.

Run it in the directory where the files are in.  Make backups before doing so!

:Copyright: 2006-2014 Jochen Kupperschmidt
:Date: 05-Jul-2014 (original release: 30-May-2006)
:License: MIT
"""

import os


# Define a file types to move to subfolders (which will be created if not yet
# existing) if `file`'s output starts with one of these strings.
TYPES = frozenset(['JPEG', 'TIFF', 'PNG'])


def create_folders():
    for folder in TYPES:
        if not os.path.isdir(folder):
            os.mkdir(folder)


if __name__ == '__main__':
    create_folders()

    for entry in os.listdir('.'):
        if not os.path.isfile(entry):
            continue

        detected = os.popen('file -b -n -p %s' % entry).read()
        for type in TYPES:
            if detected.startswith(type):
                os.rename(entry, os.path.join(type, entry))
                break
