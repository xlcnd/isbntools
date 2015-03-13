# -*- coding: utf-8 -*-
"""isbntools console & uprint file.

This is a 'just good enough' fix for UTF-8 printing and redirection.
On Windows, some characters (cyrillic, chinese, ...) are missing
in console (even if you have the right font), only on non-cyrillic's
systems. However, if you redirect to a file, they will shown!
On modern Linux and OSX it works well.

Usage:
Call 'set_msconsole()' at the begin of your program and then use
'uprint(content, filep=None, mode='w')' for printing unicode

Remarks:
'content' should be something like u'...' not 'bytes unicode'!
'filep='myfile.txt' will print to file 'myfile.txt'
'mode' has the same options as file's 'open(fp, mode)'
"""
# flake8: noqa


import os
import sys


WINDOWS = os.name == 'nt'
PY2 = sys.version < '3'
PY3 = not PY2
EOL = '\r\n' if WINDOWS and PY3 else '\n'
try:
    DEFAULT_CODEPAGE = sys.stdout.encoding if WINDOWS else None
except:
    sys.stdout = sys.__stdout__


def set_consolefont(fontname="Lucida Console"):
    """See stackoverflow question 3592673."""
    import ctypes

    LF_FACESIZE = 32
    STD_OUTPUT_HANDLE = -11

    class COORD(ctypes.Structure):
        _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

    class CONSOLE_FONT_INFOEX(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_ulong),
                    ("nFont", ctypes.c_ulong),
                    ("dwFontSize", COORD),
                    ("FontFamily", ctypes.c_uint),
                    ("FontWeight", ctypes.c_uint),
                    ("FaceName", ctypes.c_wchar * LF_FACESIZE)]

    font = CONSOLE_FONT_INFOEX()
    font.cbSize = ctypes.sizeof(CONSOLE_FONT_INFOEX)
    font.nFont = 12
    font.dwFontSize.X = 11
    font.dwFontSize.Y = 18
    font.FontFamily = 54
    font.FontWeight = 400
    font.FaceName = fontname

    handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    ctypes.windll.kernel32.SetCurrentConsoleFontEx(
        handle, ctypes.c_long(False), ctypes.pointer(font))


def register_cp65001():
    import codecs
    try:
        codecs.lookup('cp65001')
        return False
    except LookupError:
        codecs.register(
            lambda name: name == 'cp65001' and codecs.lookup('utf-8') or None)
        return True


def set_codepage(cp):
    """Set msconsole's codepage"""
    # This is THE trick to 'convince' PY2 and PY3 to accept 'cp65001'
    from ctypes import windll
    KERNEL32 = windll.kernel32
    KERNEL32.SetConsoleCP("cp%i" % cp)
    KERNEL32.SetConsoleOutputCP("cp%i" % cp)
    import subprocess
    subprocess.call("chcp %i " % cp + " > %TMP%\\xxx", shell = True)


def reset_codepage():
    """Reset codepage."""
    return set_codepage(int(DEFAULT_CODEPAGE[2:])) if DEFAULT_CODEPAGE else None


def set_msconsole():
    """Setup msconsole (with actions that don't need to be reset)."""
    # check if sys.stdout is attached to a terminal
    if not sys.stdout.isatty():
        return
    register_cp65001()
    for font in ('DejaVu LGC Sans Mono', 'Lucida Console', 'Consolas'):
        try:
            set_consolefont(font)
            break
        except:
            continue


def uprint(content, filep=None, mode='w'):
    """Unicode print function."""
    if filep:
        stdout = sys.stdout
        sys.stdout = open(filep, mode)
    s = content + EOL
    buf = s.encode("utf-8")
    if WINDOWS and sys.stdout.isatty():
        set_codepage(65001)
    try:
        if PY3:
            sys.stdout.buffer.write(buf)
        if PY2:
            sys.stdout.write(buf)
    except Exception as e:
        if type(e) == IOError:
            pass
        else:
            raise e
    if WINDOWS and sys.stdout.isatty():
        reset_codepage()
    if filep:
        sys.stdout = stdout