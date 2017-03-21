# -*- coding: utf-8 -*-
# flake8: noqa
# pylint: skip-file
"""Check available packages in pypi."""

import os
import sys
from subprocess import PIPE, Popen

from isbntools.contrib.modules.uxcolors import _colors as colors

PY2 = sys.version < '3'
PKGS = ('isbntools', 'isbnlib')
WINDOWS = os.name == 'nt'
EOL = '\r\n' if WINDOWS and not PY2 else '\n'
PY3 = not PY2
VIRTUAL = True if hasattr(sys, 'real_prefix') else False
VENV = True if hasattr(sys, 'sys.base_prefix') else False
if not VIRTUAL and VENV and PY3:  # pragma: no cover
    VIRTUAL = sys.prefix != sys.base_prefix  # inside pyvenv environement?
BOLD = colors.BOLD
RESET = colors.RESET


def shell(shcmd=None):
    """Run a shell command."""
    if not shcmd:  # pragma: no cover
        return
    sp = Popen(
        shcmd,
        shell=True,
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE,
        close_fds=not WINDOWS)
    (fo, fe) = (sp.stdout, sp.stderr)
    if PY2:  # pragma: no cover
        out = fo.read().strip(EOL)
        err = fe.read().strip(EOL)
    else:  # pragma: no cover
        out = fo.read().decode("utf-8")
        err = fe.read().decode("utf-8")
    if out:
        return out
    if err:  # pragma: no cover
        return 1


def check_pypi(pkgs=PKGS):
    """Check pypi for pkgs starting with pkgs."""
    if VIRTUAL or WINDOWS:  # pragma: no cover
        cmd = 'pip search '
    else:  # pragma: no cover
        cmd = 'sudo pip search '
    try:
        out = shell(cmd + ' '.join(pkgs))
        if out == '1':  # pragma: no cover
            return 1
        if out:  # pragma: no cover
            print('')
            print(' At %spypi%s, the following packages are available:' %
                  (BOLD, RESET))
            print('')
            print(out)
        return 0
    except:  # pragma: no cover
        return 1
