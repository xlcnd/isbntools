# -*- coding: utf-8 -*-
# flake8: noqa
# pylint: skip-file
"""Crude Timer for 'import speed'."""

import time


print("Test 'import speed' of:")


def speed_initapp():
    """Test import speed of '_initapp'."""
    t = time.process_time()
    import isbntools._initapp
    elapsed_time = time.process_time() - t
    millis = int(elapsed_time * 1000)
    print('(_initapp)  {} milliseconds < 200 milliseconds'.format(millis))
    assert millis < 200
    isbntools._initapp.CONF_PATH


def speed_app():
    """Test import speed of 'app'."""
    t = time.process_time()
    import isbntools.app
    elapsed_time = time.process_time() - t
    millis = int(elapsed_time * 1000)
    print('(app)         {} milliseconds <  10 milliseconds'.format(millis))
    assert millis < 10
    isbntools.app.defaults_conf


speed_initapp()
speed_app()
