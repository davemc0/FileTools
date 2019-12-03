#!/usr/bin/python

import sys
import argparse

def fixFileWhitespace(file_path, doCRLF, doWrite, verbose):
    with open(file_path, 'rb') as open_file:
        content = open_file.read()

    orig_content = content

    if verbose:
        print(
            content.count(b'\r\n'), 'CRLF,',
            content.count(b'\r'), 'CR,',
            content.count(b'\n'), 'LF,',
            content.count(b'\t'), 'TAB.', end='  ')

    content = content.replace(b'\r\r\n', b'\n') # Workaround clang-format 8.0.1 bug that does this
    content = content.replace(b'\r\n', b'\n') # Replace CRLF with LF
    content = content.replace(b'\r', b'\n') # Replace rogue CR with LF
    content = content.replace(b'\t', b' ') # Replace tab with space

    if verbose:
        print('Trailing space lines: ', end='')

    tspaceCnt = content.count(b' \n')
    while tspaceCnt > 0:
        if verbose:
            print(tspaceCnt, end=' ')
        content = content.replace(b' \n', b'\n') # Remove last trailing space
        tspaceCnt = content.count(b' \n')
    if verbose:
        print(tspaceCnt, end='  ')

    # As we finish, switch to CRLF if desired
    if doCRLF:
        if verbose:
            print('To CRLF', end='  ')
        content = content.replace(b'\n', b'\r\n') # Replace LF with CRLF

    if verbose:
        print('Orig length:', len(orig_content), 'new length:', len(content), end='  ')

    if content != orig_content:
        if doWrite:
            with open(file_path, 'wb') as open_file:
                open_file.write(content)
            if verbose:
                print('Saved changes.', end='')
        else:
            if verbose:
                print('Changes not saved.', end='')
    else:
        if verbose:
            print('No changes needed.', end='')

def main():
    parser = argparse.ArgumentParser(
        description='eatwhite.py - Fix up CR, LF, tabs, and spaces in text files')

    parser.add_argument('-n', '--no-write',
                        action='store_true',
                        default=False,
                        help='Do not write output files with changes')
    parser.add_argument('-r', '--to-crlf',
                        dest='to_crlf',
                        action='store_true',
                        default=True,
                        help='Convert all lines to CRLF')
    parser.add_argument('-l', '--to-lf',
                        dest='to_crlf',
                        action='store_false',
                        default=True,
                        help='Convert all lines to LF')
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        default=False,
                        help='Say everything')
    parser.add_argument('fname', nargs='+', help='File to convert')

    args = parser.parse_args()

    for fname in args.fname:
        print(fname, end=' ')
        fixFileWhitespace(fname, args.to_crlf, not args.no_write, args.verbose)
        print('')

if __name__ == "__main__":
    main()
