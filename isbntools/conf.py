# -*- coding: utf-8 -*-
"""Edit conf file."""

from .contrib._hook import (pkg_version, pkg_path, pkg_options, reg_mod,
                            reg_plugin, reg_apikey, mk_conf, print_conf,
                            reg_myopt)

__all__ = ('pkg_version', 'pkg_path', 'pkg_options', 'reg_mod',
           'reg_plugin', 'reg_apikey', 'mk_conf', 'print_conf', 'reg_myopt')
