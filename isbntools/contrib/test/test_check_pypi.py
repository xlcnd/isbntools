# -*- coding: utf-8 -*-
# flake8: noqa
# pylint: skip-file

"""nose tests for 'check pypi'."""

from isbntools.contrib.modules.report import check_pypi


def test_check_pypi():
    """Test the call to pypi"""
    errcode = check_pypi() or 0
    assert errcode == 0
