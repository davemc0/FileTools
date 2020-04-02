#!python

# Copyright 2010-2019 by David McAllister

import argparse
import eatwhite
import os
import shutil
import filecmp
import pathlib

clangFilterExts = {'.c', '.cpp', '.cl', '.cu', '.h', '.hpp', '.cuh'}
clangFilterCPPExts = {'.cl', '.cu', '.cuh'} # Extensions that we rename to .cpp before running clang-format
eatWhiteExts = clangFilterExts | {'.txt', '.cfg', '.md', '.py', '.bat', '.sh', '.y', '.l', '.py', '.pl', '.csh'}
skipFolders = {'assets', 'build', 'deps', 'output', '.git', 'DMcTools_vc120', 'DMcTools_vc141', 'DMcTools_vc142', 'GenArt_vc142', 'GenArt_vc120'}

clangFormatArgs = ''
clangFormatPath = 'clang-format.exe'

def tryCFPath(tryPath):
    global clangFormatPath
    
    pth = pathlib.Path(tryPath)
    if pth.exists():
        clangFormatPath = str(pth)
        return True
    return False
    
def setCFPath(firstTry):
    global clangFormatPath

    if tryCFPath(firstTry):
        return

    pth = pathlib.Path(__file__).parent / './clang-format.exe'
    cf = str(pth.resolve())

    if tryCFPath(cf):
        return
    if tryCFPath('C:/Program Files/LLVM/bin/clang-format.exe'):
        return
    if tryCFPath('./clang-format.exe'):
        return
    if tryCFPath('C:/Users/davemc/AppData/Local/Microsoft/VisualStudio/14.0/Extensions/nv5n2tts.1vr/clang-format.exe'):
        return
    print("Can't find clang-format.exe.")
    exit(1)

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
            eatwhite.fixFileWhitespace(file, doCRLF, doWrite, False, 0, 0, verbose, '  ')

        if fileext in clangFilterExts and doClangFormat:
            fileInTmp = file
            if fileext in clangFilterCPPExts:
                fileInTmp = file + '_CF.cpp'
                shutil.copyfile(file, fileInTmp)

            fileOutTmp = file + '.CF'
            cmd = clangFormatPath + ' ' + clangFormatArgs + ' ' + fileInTmp + ' > ' + fileOutTmp
            # print('\n', cmd)
            os.system(cmd)

            if fileInTmp != file:
                # print('Remove', fileInTmp)
                os.remove(fileInTmp)

            if filecmp.cmp(file, fileOutTmp):
                print(' Clang-format matched.')
            else:
                if doWrite:
                    #os.remove(file)
                    shutil.copyfile(fileOutTmp, file)
                    print(' Clang-format saved.')
                else:
                    print(' Clang-format changes not saved.')

            os.remove(fileOutTmp)
        elif fileext not in eatWhiteExts:
            print('Skipping:', file)
        else:
            print('')

def main():
    global clangFormatPath
    
    parser = argparse.ArgumentParser(
        description='cleancode.py - Clean whitespace and formatting in all files in tree')

    parser.add_argument('--clang-format-path',
                        default=clangFormatPath,
                        help='The first path of a clang-format executable to try')
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
                        dest='do_clang_format',
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

    setCFPath(args.clang_format_path)
    print('Using:', clangFormatPath)

    cleanDirs(args.fname, args.to_crlf, not args.no_write, args.eatwhite, args.do_clang_format, not args.quiet)

if __name__ == "__main__":
    main()
