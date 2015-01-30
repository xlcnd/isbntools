#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa
# pylint: skip-file

"""REPL for isbn."""

import cmd
import shlex

from . import (conf, doi, doitotex, EAN13, editions, from_words, goom,
               info, mask, meta, to_isbn10, to_isbn13, validate, version)
from .. import __version__
from ..app import registry
from ..contrib.modules.uxcolors import BOLD, RESET

from isbnlib.dev.helpers import fmts


class ISBNRepl(cmd.Cmd):

    """REPL main class."""

    prompt = '%sisbn>%s ' % (BOLD, RESET)
    intro = r'''
    Welcome to the %sisbntools %s%s REPL.
    ** For help enter 'help'
    ** To exit enter 'exit' :)
    ''' % (BOLD, __version__, RESET)

    def _formatters(self, text):
        if not text:
            completions = fmts
        else:
            completions = [p for p in fmts if p.startswith(text)]
        return completions

    def _parse(self, comand, line):
        """Parse line as sys.argv."""
        args = []
        args.append(comand)
        args.extend(shlex.split(line))
        return args

    def _provandfmts(self, text):
        providers = list(registry.services.keys())
        cmds = []
        cmds.extend(providers)
        cmds.extend(fmts)
        if not text:
            completions = cmds
        else:
            completions = [p for p in cmds if p.startswith(text)]
        return completions

    def _providers(self, text):
        providers = list(registry.services.keys())
        if not text:
            completions = providers
        else:
            completions = [p for p in providers if p.startswith(text)]
        return completions

    def do_audit(self, line):
        """audit"""
        version.main()

    def do_conf(self, line):
        """conf [COMMAND] [OPTIONS]"""
        conf.main(self._parse('conf', line))

    def help_conf(self):
        print('conf COMMAND [OPTIONS]\n'
              '\n'
              'COMMAND    OPTIONS               DESCRIPTION\n'
              '-------    --------------------  ----------------------------\n'
              'show                             show the conf file\n'
              'make                             make a conf file\n'
              'setkey     SERVICE  APIKEY       sets an apikey\n'
              'regplugin  SERVICE  [DIRECTORY]  registers a service\n'
              'regmod     OPTION   VALUE        sets options for modules\n'
              'setopt     OPTION   VALUE        sets options in MISC section\n'
              'delcache                         deletes the metadata cache\n'
              'cachepath                        show the path of the cache\n'
              )

    def do_doi(self, line):
        """doi ISBN"""
        doi.main(self._parse('doi', line))

    def do_doitotex(self, line):
        """doi2tex DOI\n=>doi2tex 10.3998/3336451.0004.203"""
        doitotex.main(self._parse('doitotex', line))

    def do_EAN13(self, line):
        """EAN13 ISBN"""
        EAN13.main(self._parse('EAN13', line))

    def do_editions(self, line):
        """editions ISBN"""
        editions.main(self._parse('editions', line))

    def do_exit(self, line):
        """Soft exit from REPL."""
        print('bye')
        return True

    def do_EOF(self, line):
        """Hard exit from REPL."""
        return True

    def do_from_words(self, line):
        """from_words 'AUTHOR TITLE'"""
        from_words.main(self._parse('from_words', line))

    def do_goom(self, line):
        """goom 'words' [BIBFORMAT]\n=>goom "eco name rose" refworks"""
        goom.main(self._parse('goom', line))

    def complete_goom(self, text, line, begidx, endidx):
        """Autocomplete formatters."""
        return self._formatters(text)

    def do_info(self, line):
        """info ISBN\n=>info 9780156001311"""
        info.main(self._parse('info', line))

    def do_mask(self, line):
        """mask ISBN\n=>mask 9780156001311"""
        mask.main(self._parse('mask', line))

    def do_meta(self, line):
        """meta ISBN [PROVIDER] [BIBFORMAT] [apikey]"""
        meta.main(self._parse('meta', line))

    def complete_meta(self, text, line, begidx, endidx):
        """Autocomplete providers."""
        return self._provandfmts(text)

    def help_meta(self):
        print('meta ISBN [PROVIDER] [BIBFORMAT] [apikey]\n'
              '=>meta 9780156001311 wcat endnote\n'
              '=>meta 9780156001311\n'
              '=>meta 9780156001311 tex\n'
              )

    def do_to_isbn10(self, line):
        """to_isbn10  ISBN13\n=>to_isbn10 9780156001311"""
        to_isbn10.main(self._parse('to_isbn10', line))

    def do_to_isbn13(self, line):
        """to_isbn13  ISBN10\n=>to_isbn13 1597499641"""
        to_isbn13.main(self._parse('to_isbn13', line))

    def do_validate(self, line):
        """validate ISBN\n=>validate 9780156001311"""
        validate.main(self._parse('validate', line))

    def do_BIBFORMATS(self, line):
        """Print the list of available bibliographic formats."""
        fmts.remove('labels')
        for f in sorted(fmts):
            print(f)

    def do_PROVIDERS(self, line):
        """Print the list of available providers."""
        providers = list(registry.services.keys())
        providers.remove('default')
        for p in sorted(providers):
            print(p)

def main():
    """Main entry point."""
    ISBNRepl().cmdloop()
