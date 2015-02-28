# -*- coding: utf-8 -*-
# flake8: noqa
# pylint: skip-file

import sys

from isbntools.contrib.modules.report import messages


"""
nose tests
"""


def test_messages():
    errcode = messages() or 0
    assert errcode == 0
