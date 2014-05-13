# flake8: noqa
# pylint: skip file
import os
try:
    from ..__init__ import __version__, pkg_path, defaults_conf
    from ..setconf import conf

    pkg_version = __version__
    pkg_options = conf.items('MODULES') if conf.has_section('MODULES') else []
    conf_file = conf.files[-1] if conf.files else os.path.join(pkg_path, defaults_conf)

    __all__ = ['pkg_version', 'pkg_path', 'pkg_options', 'write_conf', 'reg_plugin']

except:
    pass


def __write2conf(section, opts):
    if not conf.has_section(section):
        conf.add_section(section)
    for k, v in opts.items():
        conf.set(section, k, v)
    with open(conf_file, 'wb') as f:
        conf.write(f)


def write_conf(opts):
    __write2conf('MODULES', opts)


def reg_plugin(name, api_key=None, path=None):
    path = path if path else name + '.py'
    __write2conf('PLUGINS', {name: path})
    if api_key:
        __write2conf('SERVICES', {name.upper()+'_API_KEY': api_key})



