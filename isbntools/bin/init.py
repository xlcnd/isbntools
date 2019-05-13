# -*- coding: utf-8 -*-

import sys

from ..app import CONF_PATH, quiet_errors
from .._conf import mk_conf


def main():
    sys.excepthook = quiet_errors
    mk_conf()
    print("ISBNTOOLS is now initialized!")
    print("Check the configuration at {conf}".format(conf=CONF_PATH))
