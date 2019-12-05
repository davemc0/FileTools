#!/usr/bin/python

import sys
import argparse

def replaceLoop(content, oldt, newt, verbose):
    replCnt = content.count(oldt)
    while replCnt > 0:
        if verbose:
            print(replCnt, end=' ')
        content = content.replace(oldt, newt)
        replCnt = content.count(oldt)
    if verbose:
        print(replCnt, end='  ')

    return content

def fixFileWhitespace(file_path, doCRLF, doWrite, doCollapseSpaces, nlPerParaIn, nlPerParaOut, verbose):
    '''Get rid of all whitespace issues in the given file, with modes for source code and text files.'''
    '''Can convert line endings to LF or CRLF. Can specify how to do paragraph endings.'''

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
    content = replaceLoop(content, b' \n', b'\n', verbose) # Remove trailing spaces

    # Do cleanup for .txt files that don't apply to code

    if nlPerParaIn > 0:
        # Paragraph Mode
        # A paragraph break in input text is defined as nlPerParaIn newlines.
        # Replace these with \r as a temporary paragraph break (since \r is now not in content).
        content = content.replace(b'\n' * nlPerParaIn, b'\r')

        # There may be remaining \n at end of file that were not enough to form a paragraph break.
        # Remove file end whitespace
        while content[-1] == ord('\n') or content[-1] == ord(' '):
            content = content[0:-1]

        # Remaining \n are line breaks within a paragraph. Replace with spaces.
        content = content.replace(b'\n', b' ')

        if verbose:
            print('Multiple paragraph breaks: ', end='')
        content = replaceLoop(content, b'\r\r', b'\r', verbose) # Collapse multiple paragraph breaks into one

    if doCollapseSpaces:
        if verbose:
            print('Multiple spaces: ', end='')
        content = replaceLoop(content, b'  ', b' ', verbose) # Remove multiple spaces.

    if nlPerParaIn > 0:
        # Paragraph Mode
        content = content.replace(b'\r', b'\n' * nlPerParaOut) # Convert paragraph breaks back to nlPerParaOut newlines

        # Make sure file ends with one newline
        if content[-1] != ord('\n'):
            content = content + b'\n'

    if doCollapseSpaces:
        content = content.replace(b'\n ', b'\n') # Remove leading spaces.
        while content[0] == ord('\n') or content[0] == ord(' '):
            content = content[1:]

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
    parser.add_argument('-c', '--collapse',
                        action='store_true',
                        default=False,
                        help='Collapse multiple spaces; remove leading spaces')
    parser.add_argument('--paragraph',
                        nargs=2,
                        metavar=('NIN', 'NOUT'),
                        dest='para',
                        default=(0, 0),
                        help='Convert paragraph breaks from NIN newlines to NOUT newlines; convert newlines in paragraphs to spaces; collapse multiple newlines')
    parser.add_argument('-q', '--quiet',
                        action='store_true',
                        default=False,
                        help='Say little')
    parser.add_argument('fname',
                        nargs='+',
                        help='Files to convert')

    args = parser.parse_args()

    for fname in args.fname:
        print(fname, end=' ')
        fixFileWhitespace(fname, args.to_crlf, not args.no_write, args.collapse,
            int(args.para[0]), int(args.para[1]), not args.quiet)
        print('')

if __name__ == "__main__":
    main()
