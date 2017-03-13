# -*- coding: utf-8 -*-
"""Performs an audit and reports on installed scripts and plugins."""

from pkg_resources import iter_entry_points

from ._columnize import columnize


def audit():
    """Report on installed scripts and plugins."""
    errcode = 1

    cmds = [
        entry.name for entry in iter_entry_points(group='console_scripts')
        if 'isbn' in entry.name
    ]
    if cmds:  # pragma: no cover
        print(' The following isbn commands are available in your system:')
        print('')
        columnize(sorted(cmds))
        errcode = 0

    plug = [
        entry.name for entry in iter_entry_points(group='isbntools.plugins')
    ]
    if plug:  # pragma: no cover
        print(' The following isbntools plugins are available in your system:')
        print('')
        columnize(sorted(plug))
        errcode = 1 if errcode == 1 else 0

    return errcode
