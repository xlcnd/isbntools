#!/usr/bin/env python
# encoding: utf-8

"""REPL for isbn."""

import cmd
import shlex

from . import (conf, doi, doitotex, EAN13, editions, from_words, goom,
               info, mask, meta, to_isbn10, to_isbn13, validate, version)
from ..contrib.modules.uxcolors import BOLD, RESET


class ISBNRepl(cmd.Cmd):

    """REPL main class."""

    prompt = '%sisbn>%s ' % (BOLD, RESET)

    def do_audit(self, line):
        """audit."""
        version.main()

    def do_conf(self, line):
        """Configuration manager."""
        conf.main(self._parse('conf', line))

    def do_doi(self, line):
        """doi."""
        doi.main(self._parse('doi', line))

    def do_doitotex(self, line):
        """doitotex."""
        doitotex.main(self._parse('doitotex', line))

    def do_EAN13(self, line):
        """EAN13."""
        EAN13.main(self._parse('EAN13', line))

    def do_editions(self, line):
        """editions."""
        editions.main(self._parse('editions', line))

    def do_exit(self, line):
        """Soft exit from REPL."""
        return True

    def do_EOF(self, line):
        """Hard exit from REPL."""
        return True

    def do_from_words(self, line):
        """from_words."""
        from_words.main(self._parse('from_words', line))

    def do_goom(self, line):
        """goom."""
        goom.main(self._parse('goom', line))

    def do_info(self, line):
        """info."""
        info.main(self._parse('info', line))

    def do_mask(self, line):
        """mask."""
        mask.main(self._parse('mask', line))

    def do_meta(self, line):
        """meta command."""
        meta.main(self._parse('meta', line))

    def do_to_isbn10(self, line):
        """to_isbn10 command."""
        to_isbn10.main(self._parse('to_isbn10', line))

    def do_to_isbn13(self, line):
        """to_isbn13 command."""
        to_isbn13.main(self._parse('to_isbn13', line))

    def do_validate(self, line):
        """validate command."""
        validate.main(self._parse('validate', line))

    def _parse(self, comand, line):
        """Parse line as sys.argv."""
        args = []
        args.append(comand)
        args.extend(shlex.split(line))
        return args


def main():
    """Main entry point."""
    print("Welcome to the isbntools REPL (command line).")
    print("** For help enter 'help'")
    print("** To exit enter 'exit' :)")
    print('')
    ISBNRepl().cmdloop()
