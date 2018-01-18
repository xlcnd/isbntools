# -*- coding: utf-8 -*-
"""isbntools console & uprint file.

This is a 'just good enough' fix for UTF-8 printing and redirection.
On Windows, some characters (cyrillic, chinese, ...) are missing
in console (only on latin's systems), even if you have the
right font. However, if you redirect to a file, they will shown!
On modern Linux and OSX it works well.

Usage:
Call 'set_msconsole()' at the begin of your program and then use
'uprint(content, filep=None, mode='w')' for printing unicode

Remarks:
 . 'content' should be something like u'...' not 'bytes unicode'!
 . 'filep="myfile.txt"' will print to file 'myfile.txt'
 . 'mode' has the same options as file's 'open(fp, mode)'
 . for PY2, codepage is changed automatically, but for PY3
   the user MUST change it manually (by enter 'chcp 65001')!
"""
# flake8: noqa

import logging
import os
import sys

LOGGER = logging.getLogger(__name__)
WINDOWS = os.name == 'nt'
PY2 = sys.version < '3'
PY3 = not PY2
EOL = '\r\n' if WINDOWS and PY3 else '\n'
try:
    DEFAULT_CODEPAGE = sys.stdout.encoding if WINDOWS else None
except:
    LOGGER.critical('sys.stdout not properly reset.')
    sys.stdout = sys.__stdout__


def set_consolefont(fontname="Lucida Console"):
    """See stackoverflow question 3592673."""
    import ctypes

    LF_FACESIZE = 32
    STD_OUTPUT_HANDLE = -11

    class COORD(ctypes.Structure):
        _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

    class CONSOLE_FONT_INFOEX(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_ulong), ("nFont", ctypes.c_ulong),
                    ("dwFontSize", COORD), ("FontFamily", ctypes.c_uint),
                    ("FontWeight",
                     ctypes.c_uint), ("FaceName",
                                      ctypes.c_wchar * LF_FACESIZE)]

    font = CONSOLE_FONT_INFOEX()
    font.cbSize = ctypes.sizeof(CONSOLE_FONT_INFOEX)
    font.nFont = 12
    font.dwFontSize.X = 11
    font.dwFontSize.Y = 18
    font.FontFamily = 54
    font.FontWeight = 400
    font.FaceName = fontname

    handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    ctypes.windll.kernel32.SetCurrentConsoleFontEx(handle,
                                                   ctypes.c_long(False),
                                                   ctypes.pointer(font))


def register_cp65001():
    """Register cp65001 so that PY2 knowns about it."""
    import codecs
    try:
        codecs.lookup('cp65001')
        return False
    except LookupError:
        codecs.register(
            lambda name: codecs.lookup('utf-8') if name == 'cp65001' else None)
        return True


def set_codepage(cp):
    """Set msconsole's codepage."""
    # for PY2 this method always works
    # (only change if needed, to avoid echo messages)
    if sys.stdout.encoding == 'cp%i' % cp:
        return
    import subprocess
    subprocess.call("chcp %i" % cp + " > %TMP%\\xxx", shell=True)


def reset_codepage():
    """Reset codepage."""
    return set_codepage(int(DEFAULT_CODEPAGE[2:]))\
       if DEFAULT_CODEPAGE else None


def set_msconsole():
    """Setup msconsole (with actions that don't need to be reset)."""
    # check if sys.stdout is attached to a terminal
    if not sys.stdout.isatty():
        return
    register_cp65001()
    for font in ('Lucida Console', 'Consolas'):
        try:
            set_consolefont(font)
            break
        except:
            continue

    if WINDOWS and PY3 and sys.stdout.encoding not in ('cp65001', 'cp1252'):
        LOGGER.debug('sys.stdout.encoding is %s', sys.stdout.encoding)
        print('')
        print("    WARNING: your system is not prepared for Unicode.")
        print("    Enter 'chcp 65001' in a 'cmd' prompt before 'isbntools'.")
        print("    ** You are using codepage " + sys.stdout.encoding)
        print('')


def uprint(content, filep=None, mode='w'):
    """Unicode print function."""
    if filep:
        stdout = sys.stdout
        sys.stdout = open(filep, mode)
    s = content + EOL
    buf = s.encode("utf-8")
    if WINDOWS and PY2 and sys.stdout.isatty():
        set_codepage(65001)
    try:
        if PY3:
            sys.stdout.buffer.write(buf)
        if PY2:
            sys.stdout.write(buf)
    except IOError:
        pass
    if WINDOWS and PY2 and sys.stdout.isatty():
        reset_codepage()
    if filep:
        sys.stdout = stdout
