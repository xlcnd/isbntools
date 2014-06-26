#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from difflib import get_close_matches
from isbntools import quiet_errors
from isbntools.config import CONF_PATH, CACHE_FILE
from isbntools.conf import (reg_plugin, reg_apikey, mk_conf,
                            print_conf, reg_mod, reg_myopt)


def delcache():
    try:
        os.remove(os.path.join(CONF_PATH, CACHE_FILE))
    except:
        pass


VERBS = {'show': print_conf, 'make': mk_conf,
         'setkey': reg_apikey, 'regplugin': reg_plugin,
         'regmod': lambda x, y: reg_mod({x: y}),
         'setopt': reg_myopt, 'delcache': delcache}


def usage():
    sys.stderr.write('Usage: isbn_conf COMMAND OPTIONS\n'
                     '\n'
                     'COMMAND    OPTIONS               DESCRIPTION\n'
                     '-------    --------------------  ----------------------------\n'
                     'show                             show the conf file\n'
                     'make                             make a conf file\n'
                     'setkey     SERVICE  APIKEY       sets an apikey\n'
                     'regplugin  SERVICE  [DIRECTORY]  registers a service\n'
                     'regmod     OPTION   VALUE        sets options for modules\n'
                     'setopt     OPTION   VALUE        sets options in MISC section\n'
                     'delcache                         deletes the metadata cache\n'
                     )
    sys.exit(1)


def main():
    sys.excepthook = quiet_errors
    try:
        nargv = len(sys.argv)
        if nargv > 4 or nargv == 1:
            raise
        cmd = get_close_matches(sys.argv[1], list(VERBS.keys()))[0]
        if nargv == 2:
            VERBS[cmd]()
        elif nargv > 2:
            VERBS[cmd](*sys.argv[2:])
    except:
        usage()
