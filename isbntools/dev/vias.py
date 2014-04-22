# -*- coding: utf-8 -*-

from .. import config

RESULTS = {}


def _worker(name, task, arg):
    """
    Worker function for thread
    """
    try:
        RESULTS[name] = task(arg)
    except:
        pass


def parallel(named_tasks, arg):
    """
    Threaded calls
    """
    from threading import Thread
    for name, task in named_tasks:
        t = Thread(target=_worker, args=(name, task, arg))
        t.start()
        t.join(config.THREADS_TIMEOUT)
    return RESULTS


def serial(named_tasks, arg):
    """
    Serial calls
    """
    for name, task in named_tasks:
        RESULTS[name] = task(arg)
    return RESULTS


def multi(named_tasks, arg):
    """
    Multiprocessing: using several cores (if available)
    FIXME!
    """
    from multiprocessing import Process
    for name, task in named_tasks:
        p = Process(target=_worker, args=(name, task, arg))
        p.start()
        p.join(config.THREADS_TIMEOUT)
    return RESULTS
