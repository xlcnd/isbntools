# -*- coding: utf-8 -*-

import os
import sys
from difflib import get_close_matches

from isbnlib.dev.helpers import ShelveCache

from ..app import CACHE_FILE, CONF_PATH, quiet_errors, uprint
from ..conf import mk_conf, print_conf, reg_apikey, reg_mod, reg_myopt

PREFIX = 'isbn_'


def delcache():
    try:
        os.remove(os.path.join(CONF_PATH, CACHE_FILE))
    except:
        pass


def cachepath():
    try:
        print(os.path.join(CONF_PATH, CACHE_FILE))
    except:
        pass


def dumpcache():
    try:
        path_cache = os.path.join(CONF_PATH, CACHE_FILE)
        sc = ShelveCache(path_cache)
        for k in list(sc.keys()):
            uprint(repr(sc[k]))
    except:
        pass


def purgecache():
    try:
        path_cache = os.path.join(CONF_PATH, CACHE_FILE)
        sc = ShelveCache(path_cache)
        if sc.purge():
            print('Cache: has %s records' % len(sc))
    except:
        pass


def range_date():
    try:
        from isbnlib import RDDATE
        print(RDDATE[0:8])
    except:
        pass


VERBS = {'show': print_conf,
         'make': mk_conf,
         'setkey': reg_apikey,
         'regmod': lambda x, y: reg_mod({x: y}),
         'setopt': reg_myopt,
         'delcache': delcache,
         'cachepath': cachepath,
         'dumpcache': dumpcache,
         'purgecache': purgecache,
         'rdate': range_date, }


def usage(prefix=PREFIX):
    sys.stderr.write('Usage: %sconf COMMAND OPTIONS\n' % prefix)
    sys.stderr.write(
        '\n'
        'COMMAND    OPTIONS               DESCRIPTION\n'
        '-------    --------------------  --------------------------------\n'
        'show                             show the conf file\n'
        'make                             make a conf file\n'
        'setkey     SERVICE  APIKEY       set an apikey\n'
        'regmod     OPTION   VALUE        set options for modules\n'
        'setopt     OPTION   VALUE        set options in MISC section\n'
        'delcache                         deletes the metadata cache\n'
        'cachepath                        show the path of the cache\n'
        'dumpcache                        write the cache to sys.stdout\n'
        'purgecache                       delete low yield keys from cache\n'
        'rdate                            show date of the isbn range db\n')
    return 1


def main(args=None, prefix=PREFIX):
    sys.excepthook = quiet_errors
    try:
        args = sys.argv if not args else args
        nargv = len(args)
        if nargv > 4 or nargv == 1:
            raise
        cmd = get_close_matches(args[1], list(VERBS.keys()))[0]
        if nargv == 2:
            VERBS[cmd]()
        elif nargv > 2:
            VERBS[cmd](*args[2:])
    except:
        usage(prefix)
