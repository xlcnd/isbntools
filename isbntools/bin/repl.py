#!/usr/bin/env python
# encoding: utf-8

"""REPL for isbn."""

import cmd
import shlex

from . import conf, meta


class ISBNRepl(cmd.Cmd):

    """REPL main class."""

    prompt = 'isbn> '

    def do_meta(self, line):
        """meta command."""
        meta.main(self._parse('meta', line))

    def do_conf(self, line):
        """Configuration manager."""
        conf.main(self._parse('conf', line))

    def do_exit(self, line):
        """Soft exit from REPL."""
        return True

    def do_EOF(self, line):
        """Hard exit from REPL."""
        return True

    def _parse(self, comand, line):
        """Parse line as sys.argv."""
        args = []
        args.append(comand)
        args.extend(shlex.split(line))
        return args


def main():
    """Main entry point."""
    print("Welcome to the isbntools REPL (command line).")
    print("For help enter 'help'")
    print("To exit enter 'exit':)")
    print('')
    ISBNRepl().cmdloop()

if __name__ == '__main__':
    main()
