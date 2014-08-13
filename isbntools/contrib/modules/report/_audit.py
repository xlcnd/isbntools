# -*- coding: utf-8 -*-

"""Performs an audit and reports on installed scripts and plugins."""

from pkg_resources import iter_entry_points



def audit():
    """Perform an audit and report on installed scripts and plugins."""
    cmds = [entry.name for entry in iter_entry_points(group='console_scripts')
            if 'isbn' in entry.name]

    if cmds:
        print('The following isbn commands are available on your system:')
        print('')
        for c in sorted(cmds):
            print("   {cmd}".format(cmd=c))
        print('')

    plug = [entry.name for entry in
            iter_entry_points(group='isbntools.plugins')]

    if plug:
        print('The following isbntools plugins are available on your system:')
        print('')
        for p in sorted(plug):
            print("   {plugin}".format(plugin=p))
        print('')        
    
