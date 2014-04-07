# -*- coding: utf-8 -*-

import threading
from .. import config

results = {}


def _worker(name, task, arg):
    """
    Worker function for thread
    """
    try:
        results[name] = task(arg)
    except:
        pass


def parallel(named_tasks, arg):
    """
    Threaded calls
    """
    for name, task in named_tasks:
        t = threading.Thread(target=_worker, args=(name, task, arg))
        t.start()
        t.join(config.THREADS_TIMEOUT)

    return results


def serial(named_tasks, arg):
    """
    Serial calls
    """
    for name, task in named_tasks:
        results[name] = task(arg)

    return results
