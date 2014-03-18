#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
from .. import config

results = {}


def worker(name, task, arg):
    """
    Worker function for thread
    """
    try:
        results[name] = task(arg)
    except:
        pass


def vias(named_tasks, arg):
    """
    Threaded calls
    """
    for name, task in named_tasks:
        t = threading.Thread(target=worker, args=(name, task, arg))
        t.start()
        t.join(config.THREADS_TIMEOUT)

    return results
