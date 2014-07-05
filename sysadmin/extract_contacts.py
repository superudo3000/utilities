#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Extract contacts from a Jabberd14 xdb file.

xdb (XML database) files are flatfiles used by the jabberd14_ XMPP_ server to
store user data, including rosters.

Requires Python_ since version 2.5.

Note: If a contact is in multiple groups, only one (the first found by
ElementTree) will be perceived.

:Copyright: 2007-2008 Jochen Kupperschmidt
:Date: 16-Jul-2008
:License: MIT

.. _jabberd14:      http://jabberd.org/
.. _XMPP:           http://www.xmpp.org/
.. _Python:         http://www.python.org/
.. _ElementTree:    http://effbot.org/zone/element-index.htm
"""

from collections import defaultdict
from optparse import OptionParser
import xml.etree.ElementTree as ET


ROSTER_NAMESPACE = 'jabber:iq:roster'


def extract_contacts(filename):
    """Extract contacts in roster from xdb file."""
    doc = ET.parse(filename).getroot()
    for item in doc.findall('.//{%s}item' % ROSTER_NAMESPACE):
        yield {'jid': item.get('jid'),
               'name': item.get('name', u''),
               'group': item.findtext('{%s}group' % ROSTER_NAMESPACE)}


def group_contacts(contacts):
    """Group contacts by roster group name."""
    groups = defaultdict(list)
    for contact in contacts:
        groups[contact['group']].append(contact)
    return dict(groups)


def format_contacts(contacts):
    """Format contacts as JID and name."""
    for contact in contacts:
        yield u'%(jid)-30s  %(name)s' % contact


def format_contacts_grouped(contacts):
    """Separate contacts by roster groups."""
    groups = group_contacts(contacts)
    for group, contacts in groups.iteritems():
        yield u'\n--- ' + ((group or u'<no group>') + u' ').ljust(60, u'-')
        for contact in format_contacts(contacts):
            yield contact


def parse_args():
    parser = OptionParser(usage='usage: %prog [options] <filename>')

    parser.add_option(
        '-g', '--group',
        dest='group',
        action='store_true',
        help='list contacts by groups')

    parser.add_option(
        '-j', '--jids-only',
        dest='jids_only',
        action='store_true',
        help='only show JIDs (overrides `-g`)')

    opts, args = parser.parse_args()
    if not args:
        parser.print_help()
        parser.exit()

    return opts, args


if __name__ == '__main__':
    opts, args = parse_args()

    # Process xdb data and print result.
    contacts = extract_contacts(args[0])
    if opts.jids_only:
        output = (contact['jid'] for contact in contacts)
    elif opts.group:
        output = format_contacts_grouped(contacts)
    else:
        output = format_contacts(contacts)
    print u'\n'.join(output).encode('utf-8')
