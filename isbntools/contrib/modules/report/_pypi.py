#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa
# pylint: skip-file

"""REPL for isbn."""

import os
import sys

from subprocess import Popen, PIPE

from isbntools.contrib.modules.uxcolors import _colors as colors

PY2 = sys.version < '3'
PKGS = ('isbntools', 'isbnlib')
WINDOWS = os.name == 'nt'
EOL = '\r\n' if WINDOWS and not PY2 else '\n'
INVIRTUAL = True if hasattr(sys, 'real_prefix') else False
BOLD = colors.BOLD
RESET = colors.RESET


def shell(shcmd=None):
    """Run a shell command."""
    if not shcmd:  # pragma: no cover
        return
    sp = Popen(shcmd,
               shell=True,
               stdin=PIPE,
               stdout=PIPE,
               stderr=PIPE,
               close_fds=True
               )
    (fo, fe) = (sp.stdout, sp.stderr)
    if PY2:  # pragma: no cover
       out = fo.read().strip(EOL)
       err = fe.read().strip(EOL)
    else:  # pragma: no cover
       out = fo.read().decode("utf-8")
       err = fe.read().decode("utf-8")
    if out:
        print(out)
        return
    if err:  # pragma: no cover
        print(err)
        return 1


def check_pypi(pkgs=PKGS):
    """Check pypi for pkgs starting with pkgs."""
    if INVIRTUAL or WINDOWS:  # pragma: no cover
        cmd = 'pip search '
    else:  # pragma: no cover
        cmd = 'sudo pip search '
    try:
        print(' At %spypi%s, the following packages are available:' % (BOLD, RESET))
        print('')
        shell(cmd + ' '.join(pkgs))
        return 0
    except:  # pragma: no cover
        return 1
