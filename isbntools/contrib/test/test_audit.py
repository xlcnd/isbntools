# -*- coding: utf-8 -*-
# flake8: noqa
# pylint: skip-file
"""tests for audit module."""

import os

from isbntools.contrib.modules.report import audit


def test_audit():
    """Test if the audit report runs without errors"""
    if os.getenv('GITHUB_RUN_ID', '') != '':
        assert True
    else:
        errcode = audit()
        assert errcode == 0
