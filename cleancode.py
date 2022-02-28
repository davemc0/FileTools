#!python

# Copyright 2010-2019 by David McAllister

from __future__ import print_function
import sys
import multiprocessing
import math
import timeit

if sys.hexversion < 0x03050000:
    print('Python 3.5 or newer is required. Download it from python.org.')
    exit(1)

import argparse
import eatwhite
import re
import os
import shutil
import hashlib
import filecmp
import pathlib

clangFilterExts = {'.c', '.cpp', '.cl', '.cu', '.h', '.hpp', '.cuh'}
clangFilterCPPExts = {'.cl', '.cu', '.cuh'} # Extensions that we rename to .cpp before running clang-format
eatWhiteExts = clangFilterExts | {'.txt', '.cfg', '.md', '.py', '.bat', '.sh', '.y', '.l', '.py', '.pl', '.csh'}
skipFolders = {'__pycache__', 'assets', 'build', 'deps', 'output', 'input', '.git', 'DMcTools_vc120', 'DMcTools_vc141', 'DMcTools_vc142', 'GenArt_vc142', 'GenArt_vc120', 'default'}

clangFormatArgs = ''
clangFormatPath = pathlib.Path('clang-format.exe')

# kwargs is keyword args.
def red(text, **kwargs):
    print('\033[31m', text, '\033[0m', sep='', **kwargs)

def green(text, **kwargs):
    print('\033[32m', text, '\033[0m', sep='', **kwargs)

def yellow(text, **kwargs):
    print('\033[33m', text, '\033[0m', sep='', **kwargs)

def tryClangFormatPath(tryPath, verbose):
    global clangFormatPath

    pth = pathlib.Path(tryPath)
    if verbose:
        print('Trying:', pth)
    if pth.exists():
        clangFormatPath = pth
        return True
    return False

def setClangFormatPath(firstTry, verbose):
    '''Find clang-format.exe'''

    if tryClangFormatPath(firstTry, verbose):
        return

    # Try the directory relative to this script
    pth = pathlib.Path(__file__).parent.parent / 'tools/clang-format.exe'
    if tryClangFormatPath(str(pth.resolve()), verbose):
        return

    # Try the same directory containing this script
    pth = pathlib.Path(__file__).parent / 'clang-format.exe'
    if tryClangFormatPath(str(pth.resolve()), verbose):
        return

    if tryClangFormatPath('./clang-format.exe', verbose):
        return
    if tryClangFormatPath('C:/Program Files (x86)/Microsoft Visual Studio/2019/Community/VC/Tools/Llvm/x64/bin/clang-format.exe', verbose):
        return
    if tryClangFormatPath('C:/Program Files/LLVM/bin/clang-format.exe', verbose):
        return

    red("Can't find clang-format.exe.")
    exit(1)

# Returns a list.
def allFiles(dirs):
    '''Lists all files in the given directories'''
    paths = []

    for dirPath in dirs:
        if os.path.isfile(dirPath):
            paths.append(dirPath)
        else:
            for root, dirs, filenames in os.walk(dirPath, topdown=True):
                dirs[:] = [d for d in dirs if d not in skipFolders]

                for f in filenames:
                    path = os.path.join(root, f)
                    if os.path.isfile(path):
                        paths.append(path)

    return paths

def lineUnwrap(file, doWrite):
    '''Unwrap lines of C-like code to be semantically equivalent but as few lines as possible'''

    # This operation is not safe. Don't do it normally.
    wrapBlockers = {'//', '/*', '*/', '#', '\\'}
    inBlockComment = False
    outFile = ''
    wrapMe = True
    wrapLast = False
    inBlockComment = False
    inClangFormatOff = False
    SlSlComment = []

    with open(file, 'r') as theFile:
        for line in theFile:
            line = ('x' + line).strip()[1:]

            wrapMe = not any([x in line for x in wrapBlockers])
            if line == '':
                wrapMe = False
            if '/*' in line and '*/' not in line:
                inBlockComment = True
            if 'clang-format off' in line:
                inClangFormatOff = True

            if outFile:
                outFile += ' ' if wrapMe and wrapLast and not inBlockComment and not inClangFormatOff else '\r\n'
            outFile += line

            if re.search("^ *//", line):
                SlSlComment.append(line)
            else:
                if len(SlSlComment) > 1:
                    print()
                    for l in SlSlComment:
                        yellow(l)
                    print()
                SlSlComment = []

            if '*/' in line:
                inBlockComment = False
            if 'clang-format on' in line:
                inClangFormatOff = False
            wrapLast = wrapMe

    outFile += '\r\n'

    if doWrite:
        with open(file, 'w') as outF:
            outF.write(outFile)

def commentFix(file, doWrite):
    '''Capitalize comments'''

    capStoppers = {'=', ';', '>', '[', ':', '<', 'vvv', 'm_', 'namespace', 'elif', 'endif', 'typedef', 'static', 'printf', 'fprintf'}
    inFile = ''
    outFile = ''
    inClangFormatOff = False
    SlSlComment = []

    with open(file, 'r') as theFile:
        for line in theFile:
            inFile += line
            endl = '\r\n' in line
            line = ('x' + line).strip()[1:]

            if 'clang-format off' in line:
                inClangFormatOff = True

            if re.search("^ *//", line):
                SlSlComment.append(line)
            else:
                SlSlComment = []

            if len(SlSlComment) < 2 and not inClangFormatOff:
                m = re.search("// [a-z]", line)
                if m:
                    ind = m.start() + 3
                    comment = line[m.start():]

                    if not any([x in comment for x in capStoppers]):
                        line = line[:ind] + line[ind].upper() + line[ind+1:]
                        # yellow(line)

            outFile += line + ('\r\n' if endl else '\n')

            if 'clang-format on' in line:
                inClangFormatOff = False

    if doWrite and inFile != outFile:
        yellow(' Cleaned comments.')
        with open(file, 'w') as outF:
            outF.write(outFile)

def cleanFiles(files, doCRLF, doWrite, doLineUnwrap, doEatWhite, doClangFormat, clangFormatArgs, clangFormatPath, verbose):
    for file in files:
        print(file, end='    ')

        filename, fileext = os.path.splitext(file)

        if fileext in clangFilterExts:
            commentFix(file, doWrite)

        if fileext in clangFilterExts and doLineUnwrap:
            lineUnwrap(file, doWrite)

        if fileext in eatWhiteExts and doEatWhite:
            eatwhite.fixFileWhitespace(file, doCRLF, doWrite, False, 0, 0, verbose, '  ')

        if fileext in clangFilterExts and doClangFormat:
            fileInTmp = file
            if fileext in clangFilterCPPExts:
                fileInTmp = file + '_CF.cpp'
                shutil.copyfile(file, fileInTmp)

            fileOutTmp = file + '.CF'
            cmd = '"' + clangFormatPath.as_posix() + '" ' + clangFormatArgs + ' ' + fileInTmp + ' > ' + fileOutTmp
            os.system(cmd)

            if fileInTmp != file:
                os.remove(fileInTmp)

            if not os.path.exists(fileOutTmp):
                red(' Failed to create temp output file:' + fileOutTmp)
            else:
                if filecmp.cmp(file, fileOutTmp):
                    green(' Clang-format matched.')
                elif os.path.getsize(fileOutTmp) > 0:
                    if doWrite:
                        #os.remove(file)
                        shutil.copyfile(fileOutTmp, file)
                        yellow(' Clang-format saved.')
                    else:
                        red(' Clang-format changes not saved.')
                elif os.path.getsize(file) > 0:
                    red(' Temp output file should not be empty!!!\nCommand:' + cmd)
                else:
                    red(' Input and temp files empty')

            os.remove(fileOutTmp)
        elif fileext not in eatWhiteExts:
            green('Skipping: ' + file)
        else:
            print('')

def cleanDirs(dirs, doCRLF, doWrite, doLineUnwrap, doEatWhite, doClangFormat, doParallel, verbose):
    files = allFiles(dirs)

    if doParallel:
        # Reorder the list of files arbitrarily to decorrelate the easy ones so thread workload is more uniform
        files = [y for x,y in sorted(zip([hashlib.md5(f.encode('utf-8')).hexdigest() for f in files], files))]

        # Parallel implementation
        filesPerChunk = math.ceil(len(files) / multiprocessing.cpu_count())
        fileChunks = [files[i * filesPerChunk:(i + 1) * filesPerChunk] for i in range((len(files) + filesPerChunk - 1) // filesPerChunk )]

        processes = []
        for cur_test in fileChunks:
            p = multiprocessing.Process(target=cleanFiles, args=(cur_test, doCRLF, doWrite, doLineUnwrap, doEatWhite,
                doClangFormat, clangFormatArgs, clangFormatPath, verbose))
            processes.append(p)
            p.start()

        for process in processes:
            process.join()

    else:
        cleanFiles(files, doCRLF, doWrite, doLineUnwrap, doEatWhite, doClangFormat, clangFormatArgs, clangFormatPath, verbose)

def main():
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
    parser.add_argument('--line-unwrap',
                        dest='do_line_unwrap',
                        action='store_true',
                        default=False,
                        help='Do not remove non-semantic line breaks before formatting')
    parser.add_argument('--no-eatwhite',
                        dest='do_eatwhite',
                        action='store_false',
                        default=True,
                        help='Do not eat white')
    parser.add_argument('--no-clang-format',
                        dest='do_clang_format',
                        action='store_false',
                        default=True,
                        help='Do not do clang-format')
    parser.add_argument('--no-parallel',
                        dest='parallel',
                        action='store_false',
                        default=True,
                        help='Do not eat white')
    parser.add_argument('-l', '--to-lf',
                        dest='to_crlf',
                        action='store_false',
                        default=True,
                        help='Convert all lines to LF')
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        default=False,
                        help='Say more')
    parser.add_argument('fname',
                        nargs='*',
                        default=['.'],
                        help='Files to convert')

    args = parser.parse_args()

    setClangFormatPath(args.clang_format_path, args.verbose)
    print('Using:', clangFormatPath, '\n')

    cleanDirs(args.fname, args.to_crlf, not args.no_write, args.do_line_unwrap, args.do_eatwhite, args.do_clang_format, args.parallel, args.verbose)

if __name__ == "__main__":
    startTime = timeit.default_timer()
    main()
    stopTime = timeit.default_timer()
    print('Script Runtime: ', stopTime - startTime)
