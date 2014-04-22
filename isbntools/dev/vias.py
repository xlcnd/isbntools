# -*- coding: utf-8 -*-

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
    from threading import Thread
    for name, task in named_tasks:
        t = Thread(target=_worker, args=(name, task, arg))
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


def multi(named_tasks, arg):
    """
    Multiprocessing: using several cores (if available)
    TODO: alpha 
    """
    from multiprocessing import Process
    for name, task in named_tasks:
        p = Process(target=_worker, args=(name, task, arg))
        p.start()
        p.join(2*config.THREADS_TIMEOUT)
    return results
