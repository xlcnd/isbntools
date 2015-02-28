# -*- coding: utf-8 -*-
# flake8: noqa
# pylint: skip-file


from isbntools.contrib.modules.report import check_pypi


"""
nose tests
"""


def test_check_pypi():
    errcode = check_pypi() or 0
    assert errcode == 0
