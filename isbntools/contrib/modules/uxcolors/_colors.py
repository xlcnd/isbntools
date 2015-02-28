# -*- coding: utf-8 -*-
"""Define Some ASCII codes for colors on UNIX terminals."""


import os

RED = '\x1b[38;5;9m' if os.name != 'nt' else ''
BLUE = '\x1b[38;5;12m' if os.name != 'nt' else ''
GREEN = '\x1b[38;5;10m' if os.name != 'nt' else ''
BOLD = '\x1b[1m' if os.name != 'nt' else ''

RESET = '\x1b[0m' if os.name != 'nt' else ''
