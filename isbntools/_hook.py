# -*- coding: utf-8 -*-
# flake8: noqa
# pylint: skip-file

__all__ = ('pkg_version', 'pkg_path', 'pkg_options', 'reg_mod', 'conf_file',
           'reg_plugin', 'reg_apikey', 'mk_conf', 'print_conf', 'reg_myopt')


import os
import sys

from .__init__ import __version__
from ._initapp import conf
from .app import pkg_path, defaults_conf

pkg_version = __version__
pkg_options = conf.items('MODULES') if conf.has_section('MODULES') else []
conf_file = conf.files[-1] if conf.files else defaults_conf


def __write2conf(section, opts):
    if not conf.has_section(section):
        conf.add_section(section)
    for k, v in opts.items():
        conf.set(section, k, v)
    with open(conf_file, 'w') as f:
        conf.write(f)


def reg_mod(opts):
    __write2conf('MODULES', opts)


def reg_apikey(service, api_key):
    __write2conf('SERVICES', {service.upper()+'_API_KEY': api_key})


def reg_plugin(name, api_key=None, path=None):
    path = path if path else name + '.py'
    __write2conf('PLUGINS', {name: path})
    if api_key:
        reg_apikey(name, pi_key)


def __in_virtual():
    return True if hasattr(sys, 'real_prefix') else False


def __mkpath(path):
    directory = os.path.dirname(path)
    filename = os.path.basename(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    if filename:
        with open(path, 'w+') as f:
            f.close()


def __conf_file():
    if __in_virtual():
        installpath = ''
    else:
        homepath = os.path.expanduser('~') if os.name != 'nt' else os.getenv('APPDATA')
        confdir = '.isbntools' if os.name != 'nt' else 'isbntools'
        installpath = os.path.join(homepath, confdir)
    conffile = 'isbntools.conf'
    return os.path.join(installpath, conffile)


def mk_conf():
    global conf_file
    if conf_file == defaults_conf or not os.path.exists(__conf_file()):
        __mkpath(__conf_file())
        with open(__conf_file(), 'w') as f:
            conf.write(f)
            conf_file = f.name


def reg_myopt(opt, value):
    __write2conf('MISC', {opt.upper(): value})


def print_conf():
    if conf_file == defaults_conf:
        print("NO conf file! Using default builtins.")
        return
    print(("conf file at %s:" % conf_file))
    conf.write(sys.stdout)
