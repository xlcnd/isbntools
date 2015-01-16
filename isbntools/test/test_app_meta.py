#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa
# pylint: skip-file

import os

from nose.tools import assert_equals, assert_raises

from isbnlib.dev.helpers import File, cwdfiles
from isbnlib.dev.bouth23 import u

from isbntools.app.meta import main as meta_app

"""
nose tests
"""



def test_meta_app():
    sys.argv[1] = '9780321534965'
    assert_equals(len(meta_app()) > 150, True)

