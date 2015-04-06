"""Borrowed from Standard Library (cmd.py)."""

import sys


def columnize(list, displaywidth=80):
    """Display a list of strings as a compact set of columns.

    Each column is only as wide as necessary.
    Columns are separated by two spaces (one was not legible enough).
    """
    if not list:
        sys.stdout.write("<empty>\n")
        return
    nonstrings = [i for i in range(len(list))
                  if not isinstance(list[i], str)]
    if nonstrings:
        raise TypeError("list[i] not a string for i in %s" %
                        ", ".join(map(str, nonstrings)))
    size = len(list)
    if size == 1:
        sys.stdout.write('%s\n' % str(list[0]))
        return
    # Try every row count from 1 upwards
    for nrows in range(1, len(list)):
        ncols = (size + nrows - 1) // nrows
        colwidths = []
        totwidth = -2
        for col in range(ncols):
            colwidth = 0
            for row in range(nrows):
                i = row + nrows * col
                if i >= size:
                    break
                x = list[i]
                colwidth = max(colwidth, len(x))
            colwidths.append(colwidth)
            totwidth += colwidth + 2
            if totwidth > displaywidth:
                break
        if totwidth <= displaywidth:
            break
    else:
        nrows = len(list)
        ncols = 1
        colwidths = [0]
    for row in range(nrows):
        texts = []
        for col in range(ncols):
            i = row + nrows * col
            if i >= size:
                x = ""
            else:
                x = list[i]
            texts.append(x)
        while texts and not texts[-1]:
            del texts[-1]
        for col in range(len(texts)):
            texts[col] = texts[col].ljust(colwidths[col])
        sys.stdout.write("%s\n" % str("  ".join(texts)))
