#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa
# pylint: skip-file

"""REPL for isbn."""

import cmd
import shlex
import sys
import time

from difflib import get_close_matches
from subprocess import Popen, PIPE

from . import (conf, doi, doi2tex, EAN13, editions, from_words, goom,
               info, mask, meta, to_isbn10, to_isbn13, validate, version)
from .. import __version__
from ..app import registry
from ..contrib.modules.uxcolors import BOLD, RESET

from isbnlib.dev.helpers import fmts

CMDS = ['audit', 'BIBFORMATS', 'conf', 'doi', 'doi2tex', 'EAN13',
        'editions', 'goom', 'info', 'mask', 'meta', 'from_words',
        'PROVIDERS', 'shell', 'validate']
PREFIX = ''
PY2 = sys.version < '3'


class ISBNRepl(cmd.Cmd):

    """REPL main class."""

    # TODO refactor this boilerplate! Make a cli module.

    doc_header = 'Commands available (type ?<command> to get help):'
    intro = r'''
    Welcome to the %sisbntools %s%s REPL.
    ** For help type 'help' or '?'
    ** To exit type 'exit' :)
    ** To run a shell command, type '!<shellcmnd>'
    ''' % (BOLD, __version__, RESET)
    prompt = '%sisbn>%s ' % (BOLD, RESET)
    ruler = '-'


    # Base Classe Overrides:

    def default(self, s):
        """Override default method to allow fuzzy commands."""
        try:
            v = s.split(' ')[0]
            match = get_close_matches(v, CMDS)
            verb = None
            if match:
                match.sort(key=len)
                for m in match:
                    if m.startswith(v):
                        verb = m
                        break
                if not verb:
                    verb = match[0]
                s = s.replace(v, verb)
                return cmd.Cmd.onecmd(self, s)
            else:
                for c in sorted(CMDS):
                    if c.startswith(v):
                        return cmd.Cmd.onecmd(self, c)
                return cmd.Cmd.default(self, s)
        except:
            return cmd.Cmd.default(self, s)

    def emptyline(self):
        """Override emptyline method to output help."""
        return cmd.Cmd.do_help(self, '')

    # Helpers:

    def _formatters(self, text):
        if not text:
            completions = fmts
        else:
            completions = [p for p in fmts if p.startswith(text)]
        return completions

    def _parse(self, comand, line):
        """Parse line as sys.argv."""
        # TODO overwrite parseline instead?
        ops = ['<', '>', '>>', '|']
        redirect = any(x in line for x in ops)
        if redirect:
            if '<' in line:
                print('*** Input redirection is not supported!')
                return
            if comand == 'audit':
                comand = 'isbntools'
            elif comand.startswith('to_isbn'):
                pass
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

    # Commands:

    def do_audit(self, line):
        """audit"""
        wait=5
        version.main(wait)
        time.sleep(wait)

    def do_conf(self, line):
        """conf [COMMAND] [OPTIONS]"""
        if not line:
            conf.usage(prefix=PREFIX)
            return
        try:
            args = self._parse('conf', line)
            if args:
                conf.main(args, prefix=PREFIX)
        except:
            conf.usage(prefix=PREFIX)

    def complete_conf(self, text, line, begidx, endidx):
        """Autocomplete conf options."""
        opts = list(conf.VERBS.keys())
        if not text:
            completions = opts
        else:
            completions = [o for o in opts if o.startswith(text)]
        return completions

    def do_doi(self, line):
        """doi ISBN"""
        if not line:
            print(self.do_doi.__doc__)
            return
        args = self._parse('doi', line)
        if args:
            doi.main(args, prefix=PREFIX)

    def do_doi2tex(self, line):
        """doi2tex DOI\n=>doi2tex 10.3998/3336451.0004.203"""
        if not line:
            print(self.do_doi2tex.__doc__)
            return
        args = self._parse('doi2tex', line)
        if args:
            doi2tex.main(args, prefix=PREFIX)

    def do_EAN13(self, line):
        """EAN13 ISBN"""
        if not line:
            print(self.do_EAN13.__doc__)
            return
        args = self._parse('EAN13', line)
        if args:
            EAN13.main(args, prefix=PREFIX)

    def do_editions(self, line):
        """editions ISBN"""
        if not line:
            print(self.do_editions.__doc__)
            return
        args = self._parse('editions', line)
        if args:
            editions.main(args, prefix=PREFIX)

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
            from_words.main(args, prefix=PREFIX)

    def do_goom(self, line):
        """goom 'words' [BIBFORMAT]\n=>goom "eco name rose" refworks"""
        if not line:
            print(self.do_goom.__doc__)
            return
        args = self._parse('goom', line)
        if args:
            goom.main(args, prefix=PREFIX)

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
            info.main(args, prefix=PREFIX)

    def do_mask(self, line):
        """mask ISBN\n=>mask 9780156001311"""
        if not line:
            print(self.do_mask.__doc__)
            return
        args = self._parse('mask', line)
        if args:
            mask.main(args, prefix=PREFIX)

    def do_meta(self, line):
        """meta ISBN [PROVIDER] [BIBFORMAT] [apikey]"""
        if not line:
            self.help_meta()
            return
        args = self._parse('meta', line)
        if args:
            meta.main(args, prefix=PREFIX)

    def complete_meta(self, text, line, begidx, endidx):
        """Autocomplete providers."""
        return self._provandfmts(text)

    def help_meta(self):
        print('meta ISBN [PROVIDER] [BIBFORMAT] [apikey]\n'
              '=>meta 9780156001311 wcat endnote\n'
              '=>meta 9780156001311\n'
              '=>meta 9780156001311 tex'
              )

    def do_to_isbn10(self, line):
        """to_isbn10  ISBN13\n=>to_isbn10 9780156001311"""
        if not line:
            print(self.do_to_isbn10.__doc__)
            return
        args = self._parse('to_isbn10', line)
        if args:
            to_isbn10.main(args, prefix=PREFIX)

    def do_to_isbn13(self, line):
        """to_isbn13  ISBN10\n=>to_isbn13 1597499641"""
        if not line:
            print(self.do_to_isbn13.__doc__)
            return
        args = self._parse('to_isbn13', line)
        if args:
            to_isbn13.main(args, prefix=PREFIX)

    def do_validate(self, line):
        """validate ISBN\n=>validate 9780156001311"""
        if not line:
            print(self.do_validate.__doc__)
            return
        args = self._parse('validate', line)
        if args:
            validate.main(args, prefix=PREFIX)

    def do_BIBFORMATS(self, line):
        """Print the list of available bibliographic formats."""
        bibf = fmts[:]
        try:
            bibf.remove('labels')
        except:
            pass
        for f in sorted(bibf):
            print(f)

    def do_PROVIDERS(self, line):
        """Print the list of available providers."""
        providers = list(registry.services.keys())
        try:
            providers.remove('default')
        except:
            pass
        for p in sorted(providers):
            print(p)

    def do_shell(self, line):
        """Run a shell command."""
        if not line:
            return
        sp = Popen(line,
                   shell=True,
                   stdin=PIPE,
                   stdout=PIPE,
                   stderr=PIPE,
                   close_fds=True
                   )
        (fo, fe) = (sp.stdout, sp.stderr)
        if PY2:
            out = fo.read().strip(EOL)
            err = fe.read().strip(EOL)
        else:
            out = fo.read().decode("utf-8")
            err = fe.read().decode("utf-8")
        if out:
            print(out)
            return
        if err:
            print(err.replace('isbn_', ''))


def main():
    """Main entry point."""
    ISBNRepl().cmdloop()
