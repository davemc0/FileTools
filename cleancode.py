#!/usr/bin/python

import argparse
import eatwhite
import os
import shutil
import filecmp

clangFilterExts = {'.c', '.cpp', '.cl', '.cu', '.h', '.hpp', '.cuh'}
eatWhiteExts = clangFilterExts | {'.txt', '.cfg', '.md', '.py', '.bat', '.sh', '.y', '.l', '.py', '.pl', '.csh'}
skipFolders = {'assets', 'build', 'deps', 'output', '.git', 'DMcTools_vc120', 'DMcTools_vc141', 'DMcTools_vc142', 'GenArt_vc142', 'GenArt_vc120'}

#clangFormatPath = '"C:/Program Files/LLVM/bin/clang-format.exe"'
clangFormatPath = '"C:/Users/davemc/AppData/Local/Microsoft/VisualStudio/14.0/Extensions/qd5ak3fn.lc0/clang-format.exe"'
clangFormatArgs = ''

# Returns a generator
def allFiles(dirs):
    '''Lists all files in the given directories'''

    for dirPath in dirs:
        for root, dirs, filenames in os.walk(dirPath, topdown=True):
            dirs[:] = [d for d in dirs if d not in skipFolders]

            for f in filenames:
                path = os.path.join(root, f)
                if os.path.isfile(path):
                    yield path

def cleanDirs(dirs, doCRLF, doWrite, doEatWhite, doClangFormat, verbose):
    files = allFiles(dirs)
    for file in files:
        print(file, end='    ')

        filename, fileext = os.path.splitext(file)

        if fileext in eatWhiteExts and doEatWhite:
            eatwhite.fixFileWhitespace(file, doCRLF, doWrite, False, 0, 0, verbose)

        if fileext in clangFilterExts and doClangFormat:
            fileTmp = file + '.CF'
            cmd = clangFormatPath + ' ' + clangFormatArgs + ' ' + file + ' > ' + fileTmp
            # print('\n', cmd)
            os.system(cmd)
            if filecmp.cmp(file, fileTmp):
                print(' Clang-format matched.')
            else:
                if doWrite:
                    #os.remove(file)
                    shutil.copyfile(fileTmp, file)
                    print(' Clang-format saved.')
                else:
                    print(' Clang-format changes not saved.')

            os.remove(fileTmp)
        elif fileext not in eatWhiteExts:
            print('Skipping:', file)
        else:
            print('')

def main():
    parser = argparse.ArgumentParser(
        description='cleancode.py - Clean whitespace and formatting in all files in tree')

    parser.add_argument('-n', '--no-write',
                        action='store_true',
                        default=False,
                        help='Do not write output files with changes')
    parser.add_argument('-r', '--to-crlf',
                        dest='to_crlf',
                        action='store_true',
                        default=True,
                        help='Convert all lines to CRLF')
    parser.add_argument('--no-eatwhite',
                        dest='eatwhite',
                        action='store_false',
                        default=True,
                        help='Do not eat white')
    parser.add_argument('--no-clang-format',
                        dest='clang_format',
                        action='store_false',
                        default=True,
                        help='Do not do clang-format')
    parser.add_argument('-l', '--to-lf',
                        dest='to_crlf',
                        action='store_false',
                        default=True,
                        help='Convert all lines to LF')
    parser.add_argument('-q', '--quiet',
                        action='store_true',
                        default=False,
                        help='Say little')
    parser.add_argument('fname',
                        nargs='*',
                        default=['.'],
                        help='Files to convert')

    args = parser.parse_args()

    cleanDirs(args.fname, args.to_crlf, not args.no_write, args.eatwhite, args.clang_format, not args.quiet)

if __name__ == "__main__":
    main()
