# -*- coding: utf-8 -*-
"""Edit conf file (mainly for programatic API)."""

from ._hook import (pkg_version, pkg_path, pkg_options, reg_mod,
                    reg_plugin, reg_apikey, mk_conf, print_conf,
                    reg_myopt, conf_file)

__all__ = ('pkg_version', 'pkg_path', 'pkg_options',
           'reg_mod', 'reg_plugin', 'reg_apikey', 'reg_myopt',
           'conf_file', 'mk_conf', 'print_conf')
