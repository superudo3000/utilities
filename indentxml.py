#!/usr/bin/env python

"""Nicely indent XML read from STDIN or a file."""

from os.path import basename
from sys import argv, exit, stdin
from xml.dom.minidom import parseString


def read_data(fn):
    """Read data from STDIN or a file."""
    if fn == '-':
        f = stdin
    else:
        f = open(fn, 'rb')
    return f.read()

def indent_xml(xml, indent=' '*4):
    """Indent and return XML."""
    return parseString(xml).toprettyxml(indent)


if __name__ == '__main__':
    if len(argv) != 2:
        print 'Usage: %s <filename | - (stdin)>' \
            % basename(argv[0])
        exit(2)
    print indent_xml(read_data(argv[1]))
