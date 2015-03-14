# -*- coding: utf-8 -*-
# flake8: noqa
# pylint: skip-file

import sys

from isbntools.contrib.modules.report import messages


"""
nose tests
"""


def test_messages():
    """Test the call to messages.csv and processing"""
    errcode = messages() or 0
    assert errcode == 0
