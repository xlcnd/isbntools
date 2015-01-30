import cmd


class ISBNRepl(cmd.Cmd):
    """REPL for isbn."""

    prompt = 'isbn> '

    def do_meta(self, line):
        print("do meta %s" % line)

    def do_exit(self, line):
        return True

    def do_EOF(self, line):
        return True

if __name__ == '__main__':
    print("Welcome to the isbntools command line.")
    print("To exit enter 'exit'")
    ISBNRepl().cmdloop()
