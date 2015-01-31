#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa
# pylint: skip-file

"""REPL for isbn."""

import cmd
import os
import shlex

from . import (conf, doi, doitotex, EAN13, editions, from_words, goom,
               info, mask, meta, to_isbn10, to_isbn13, validate, version)
from .. import __version__
from ..app import registry
from ..contrib.modules.uxcolors import BOLD, RESET

from isbnlib.dev.helpers import fmts


class ISBNRepl(cmd.Cmd):

    """REPL main class."""

    # TODO refactor the boilerplate!

    prompt = '%sisbn>%s ' % (BOLD, RESET)
    intro = r'''
    Welcome to the %sisbntools %s%s REPL.
    ** For help enter 'help' or '?'
    ** To exit enter 'exit' :)
    ** To run a shell command enter '!yourshellcmnd'
    ''' % (BOLD, __version__, RESET)

    def _formatters(self, text):
        if not text:
            completions = fmts
        else:
            completions = [p for p in fmts if p.startswith(text)]
        return completions

    def _parse(self, comand, line):
        """Parse line as sys.argv."""
        ops = ['<', '>', '>>', '|']
        redirect = any(x in line for x in ops)
        if redirect:
            if '<' in line:
                print('*** Redirection of input is not supported!')
                returns
            if comand == 'audit':
                comand = 'isbntools'
            else:
                comand = 'isbn_' + comand
            self.do_shell('%s %s' % (comand, line))
            return
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
        if not line:
            self.help_conf()
            return
        args = self._parse('conf', line)
        if args:
            conf.main(args)

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
        if not line:
            print(self.do_doi.__doc__)
            return
        args = self._parse('doi', line)
        if args:
            doi.main(args)

    def do_doitotex(self, line):
        """doi2tex DOI\n=>doi2tex 10.3998/3336451.0004.203"""
        if not line:
            print(self.do_doitotex.__doc__)
            return
        args = self._parse('doitotex', line)
        if args:
            doitotex.main(args)

    def do_EAN13(self, line):
        """EAN13 ISBN"""
        if not line:
            print(self.do_EAN13.__doc__)
            return
        args = self._parse('EAN13', line)
        if args:
            EAN13.main(args)

    def do_editions(self, line):
        """editions ISBN"""
        if not line:
            print(self.do_editions.__doc__)
            return
        args = self._parse('editions', line)
        if args:
            editions.main(args)

    def do_exit(self, line):
        """Soft exit from REPL."""
        print('bye')
        return True

    def do_EOF(self, line):
        """Hard exit from REPL."""
        return True

    def do_from_words(self, line):
        """from_words 'AUTHOR TITLE'\n=>from_words 'eco name rose'"""
        if not line:
            print(self.do_from_words.__doc__)
            return
        args = self._parse('from_words', line)
        if args:
            from_words.main(args)

    def do_goom(self, line):
        """goom 'words' [BIBFORMAT]\n=>goom "eco name rose" refworks"""
        if not line:
            print(self.do_goom.__doc__)
            return
        args = self._parse('goom', line)
        if args:
            goom.main(args)

    def complete_goom(self, text, line, begidx, endidx):
        """Autocomplete formatters."""
        return self._formatters(text)

    def do_info(self, line):
        """info ISBN\n=>info 9780156001311"""
        if not line:
            print(self.do_info.__doc__)
            return
        args = self._parse('info', line)
        if args:
            info.main(args)

    def do_mask(self, line):
        """mask ISBN\n=>mask 9780156001311"""
        if not line:
            print(self.do_mask.__doc__)
            return
        args = self._parse('mask', line)
        if args:
            mask.main(args)

    def do_meta(self, line):
        """meta ISBN [PROVIDER] [BIBFORMAT] [apikey]"""
        if not line:
            self.help_meta()
            return
        args = self._parse('meta', line)
        if args:
            meta.main(args)

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
        if not line:
            print(self.do_to_isbn10.__doc__)
            return
        args = self._parse('to_isbn10', line)
        if args:
            to_isbn10.main(args)

    def do_to_isbn13(self, line):
        """to_isbn13  ISBN10\n=>to_isbn13 1597499641"""
        if not line:
            print(self.do_to_isbn13.__doc__)
            return
        args = self._parse('to_isbn13', line)
        if args:
            to_isbn13.main(args)

    def do_validate(self, line):
        """validate ISBN\n=>validate 9780156001311"""
        if not line:
            print(self.do_validate.__doc__)
            return
        args = self._parse('validate', line)
        if args:
            validate.main(args)

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

    def do_shell(self, line):
        "Run a shell command"
        if not line:
            return
        output = os.popen(line).read().strip('\n')
        if output:
            print(output)


def main():
    """Main entry point."""
    ISBNRepl().cmdloop()
