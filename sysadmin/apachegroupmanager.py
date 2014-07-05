#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Apache Auth Group Manager

A grid of checkboxes represents group memberships for Apache access control.
They are read from the group file, which has to be specified on the command
line, and can be saved back to the very same file.

The file format is as follows::

    group1: user1 user2
    group2: user1 user3 user4

Optionally, a users file (usually called ``.passwd`` or ``.digest_pw``) can be
specfied to include users in the grid that are not yet members of one of the
groups.

This utility is only meant for adding or removing users to or from groups.
Add users using the standard tools (``htpasswd`` or ``htdigest``).  To remove
users, add or remove groups, edit the according file manually.

.. note:: Groups without users assigned won't be saved.

:Copyright: (c) 2008 Jochen Kupperschmidt
:Date: 25-Nov-2008
:License: MIT
"""

from __future__ import with_statement
from collections import defaultdict
from itertools import chain
import os.path
import sys
import Tkinter as tk


# Load, handle and store users and groups.


def load_groups(filename):
    """Load groups and their members from file."""
    with open(filename, 'rb') as f:
        for line in f:
            group, users = line.split(':', 1)
            yield group, frozenset(users.split())


def load_users(filename):
    """Load users from file."""
    with open(filename, 'rb') as f:
        for line in f:
            yield line.split(':', 1)[0]


def get_groups_users(groups):
    """Return the set of users that are group members."""
    return set(chain(*(members for group, members in groups)))


def save_groups(filename, groups):
    """Write groups and their member associations to file."""
    with open(filename, 'wb') as f:
        for group, members in groups.iteritems():
            f.write('%s: %s\n' % (group, ' '.join(members)))


# Tkinter GUI


class GUI(tk.Tk):
    """Graphical frontend."""

    def __init__(self, users, groups, filename):
        tk.Tk.__init__(self)
        self.title('Group Membership Manager')

        # Build labeled grid of checkbuttons.
        self.items = []
        for column, (group, members) in enumerate(sorted(groups)):
            tk.Label(self, text=group).grid(row=0, column=column + 1)
        for row, user in enumerate(sorted(users)):
            tk.Label(self, text=user).grid(row=row + 1, column=0, sticky=tk.W)
            for column, (group, members) in enumerate(groups):
                var = tk.BooleanVar()
                var.set(user in members)
                tk.Checkbutton(self, variable=var) \
                    .grid(row=row + 1, column=column + 1)
                self.items.append((group, user, var))

        # Add a button to save the current selection.
        self.filename = filename
        tk.Button(self, text='Save', command=self.save) \
            .grid(row=len(users) + 2, column=0, columnspan=len(groups) + 1)

    def save(self):
        """Re-assemble and save groups and memberships."""
        groups = defaultdict(list)
        for group, user, var in self.items:
            if var.get():
                groups[group].append(user)

        save_groups(self.filename, groups)


def main(groups_filename, users_filename=None):
    groups = list(load_groups(groups_filename))
    users = get_groups_users(groups)
    if users_filename:
        users.update(load_users(users_filename))
    GUI(users, groups, groups_filename).mainloop()


if __name__ == '__main__':
    if len(sys.argv) not in (2, 3):
        print('usage: %s <groups file> [users file]'
              % os.path.basename(sys.argv[0]))

    main(*sys.argv[1:])
