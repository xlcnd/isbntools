# -*- coding: utf-8 -*-
"""isbntools console & uprint file.

This is a 'just good enough' fix for UTF-8 printing and redirection.
On Windows, some characters (cyrillic, chinese, ...) are missing
in console, however if you redirect to a file they will shown!
Its OK on Linux and OSX.
"""
# flake8: noqa



import os
import sys


WINDOWS = os.name == 'nt'
PY2 = sys.version < '3'
PY3 = not PY2
EOL = '\r\n' if WINDOWS and PY3 else '\n'
DEFAULT_CODEPAGE = sys.stdout.encoding if WINDOWS else None


def set_codepage(cp):
    try:
        if sys.stdout.encoding == 'cp65001':
            return
    except:
        pass
    # (1) pywin32
    # import win32console
    # win32console.SetConsoleOutputCP(65001)
    # win32console.SetConsoleCP(65001)

    # (2) command line
    # import subprocess
    # subprocess.call("chcp " + cp[2:] + " > %TMP%\\xxx", shell = True)

    # (3) ctypes
    from ctypes import windll

    KERNEL32 = windll.kernel32

    # default_cp = KERNEL32.GetConsoleCP()
    # default_output_cp = KERNEL32.GetConsoleOutputCP()

    rc1 = KERNEL32.SetConsoleCP(cp)
    rc2 = KERNEL32.SetConsoleOutputCP(cp)
    return rc1 + rc2 == 0


def register_cp65001():
    import codecs
    try:
        codecs.lookup('cp65001')
        return False
    except LookupError:
        codecs.register(
            lambda cp: cp == 'cp65001' and codecs.lookup('utf-8') or None)
        return True

def set_consolefont(fontname="Lucida Console"):
    """stackoverflow.com/questions/3592673/change-console-font-in-windows"""
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


def set_msconsole():
    register_cp65001()
    if sys.stdout.encoding != 'cp65001':
        set_codepage('cp65001')
    set_consolefont('Lucida Console')


def reset_msconsole():
    set_codepage(DEFAULT_CODEPAGE)


def uprint(content, filep=None, mode='w'):
    """Unicode print function."""
    if WINDOWS:
        set_codepage('cp65001')
    s = content + EOL
    buf = s.encode("utf-8")
    if filep:
        stdout = sys.stdout
        sys.stdout = open(filep, mode)
    if PY3:
        sys.stdout.buffer.write(buf)
    if PY2:
        sys.stdout.write(buf)
    if filep:
        sys.stdout = stdout
    if WINDOWS:
        reset_msconsole()
    return True
