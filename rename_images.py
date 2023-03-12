#!python

# Rename all image and video files consistently
# Clean up capitalization and punctuation of textual filenames, if any
# Number similar-named files sequentially
# Use date and time of image stored in metadata, if any
# Use file modification date as name if no other info

import sys
import os
import getopt
import exifread
import time
import re
import random
from iptcinfo3 import IPTCInfo
# Sometime I should switch to py3exiv2 but I couldn't get it to compile.

iptcKeys = ['by-line', 'by-line title', 'caption/abstract', 'category', 'city', 'contact', 'country/primary location name', 'credit', 'custom12', 'date created', 'headline', 'image type', 'keywords', 'nonstandard_125', 'nonstandard_14', 'nonstandard_166', 'nonstandard_192', 'nonstandard_221', 'nonstandard_231', 'nonstandard_243', 'nonstandard_248', 'nonstandard_66', 'nonstandard_68', 'nonstandard_76', 'nonstandard_88', 'object name', 'original transmission reference', 'originating program', 'program version', 'province/state', 'source', 'special instructions', 'time created', 'urgency', 'writer/editor']
iptcTitleKeys = ['caption/abstract', 'headline', 'keywords', 'object name', 'category', 'city', 'contact', 'by-line', 'by-line title', 'country/primary location name', 'credit', 'original transmission reference', 'province/state', 'source', 'writer/editor']

def bytesToString(bstr):
    st = ''
    for cod in ['ascii', 'windows-1252', 'utf-8', 'utf-16']:
        try:
            st = bstr.decode(cod)
            break
        except UnicodeDecodeError as err:
            print('Decoding error:', err)
            st = ''
        except AttributeError as err:
            st = ''

    return st

def getIPTCTitle(pathName):
    iptcTags = IPTCInfo(pathName)

    for tag in iptcTitleKeys:
        if iptcTags[tag]:
            return bytesToString(iptcTags[tag])

def getAllTags(pathName):
    getAllIPTC = False
    if getAllIPTC:
        iptcTags = IPTCInfo(pathName)

        tags = {}
        for tag in iptcKeys:
            if iptcTags[tag]:
                tags[tag] = iptcTags[tag]
                print(tags[tag])

    # Open image file for reading (binary mode)
    f = open(pathName, 'rb')

    # Return Exif tags
    exifTags = exifread.process_file(f, details=True, strict=False)

    # Convert byte array to unicode
    for k in ['Image XPTitle', 'Image XPComment', 'Image XPAuthor', 'Image XPKeywords', 'Image XPSubject']:
        if k in exifTags:
            exifTags[k].values = bytesToString(exifTags[k].values)

    return exifTags

def printAllTags(tags):
    for tag in tags.keys():
        if tag not in ('JPEGThumbnail', 'TIFFThumbnail'):
            try:
                val = str(tags[tag])
                if 'UserComment' in tag:
                    val = ''.join(tags[tag])
                print('Key:', tag, 'Value:', val)
            except (TypeError, UnicodeEncodeError) as err:
                print('Tag print error:', err, type(tags[tag]))

def getImageDate(pathName, tags):
    dateStr = ''
    if 'Image DateTime' in tags:
        dateStr = tags['Image DateTime'].printable
        if '-' in dateStr:
            print('Nonstandard date format in image:', dateStr)
            ts = time.strptime(tags['Image DateTime'].printable,"%Y-%m-%dT%H:%M:%S%z")
            dateStr = '%04d%02d%02d_%02d%02d%02d' % (ts.tm_year, ts.tm_mon, ts.tm_mday, ts.tm_hour, ts.tm_min, ts.tm_sec)
            print('Remapping to:', dateStr)

    if 'EXIF DateTimeOriginal' in tags:
        ndate = tags['EXIF DateTimeOriginal'].printable
        if ndate < dateStr or not dateStr:
            dateStr = ndate

    if 'EXIF DateTimeDigitized' in tags:
        ndate = tags['EXIF DateTimeDigitized'].printable
        if ndate < dateStr or not dateStr:
            dateStr = ndate

    if not dateStr:
        # See if there is an IPTC date
        iptcTags = IPTCInfo(pathName)
        idate = iptcTags['date created']
        if idate and len(idate) < 10:
            dateStr = bytesToString(idate) + '_000000'

    if not dateStr:
        # There are no date tags, so use the file timestamp
        ct = os.path.getctime(pathName)
        mt = os.path.getmtime(pathName)
        ft = min(ct, mt)
        ts = time.localtime(ft)
        dateStr = '%04d%02d%02d_%02d%02d%02d' % (ts.tm_year, ts.tm_mon, ts.tm_mday, ts.tm_hour, ts.tm_min, ts.tm_sec)
        print('Date from timestamp:', dateStr)

    return dateStr

def dateName(pathName):
    '''Compute the new baseName from date and camera model'''

    title = getIPTCTitle(pathName)
    if title:
        return textName(title)

    tags = getAllTags(pathName)

    dateStr = getImageDate(pathName, tags)
    dateStr = dateStr.replace(':', '').replace(' ', '_')

    camera = 'Image' # Prefix to use for unknown camera models
    if 'Image Model' in tags:
        camNameTag = tags['Image Model'].printable
        nameTrans = {
            'iPhone X':'iPhoneX',
            'iPhone 7':'iPhone7',
            'iPhone 6s':'iPhone6s',
            'iPhone 6':'iPhone6',
            'iPhone 5s':'iPhone5S',
            'iPhone 5c':'iPhone5C',
            'iPhone 5':'iPhone5',
            'iPhone 4S':'iPhone4S',
            'iPhone 4':'iPhone4',
            'iPhone 3GS':'iPhone3GS',
            'iPhone 3G':'iPhone3G',
            'Canon PowerShot S5 IS':'Canon',
            'DSC-P150':'Sony'}
        if camNameTag in nameTrans:
            camera = nameTrans[camNameTag]

    return dateStr + '_' + camera

def textName(pathName):
    '''Compute the new baseName by prettying up the words of the existing name'''

    print('Text renaming:', pathName)

    base = os.path.splitext(os.path.basename(pathName))[0]
    # print('Basename:', base)

    out = ''
    space = ''
    wordStart = True
    for c in base:
        if not c.isupper() and not c.islower():
            wordStart = True
        else:
            if c.isupper():
                out += space + c
            else:
                out += (space + c.upper()) if wordStart else c
            space = ' '
            wordStart = False

    return out

def longestString(str):
    '''Return length of longest alphabetic substring'''

    ln = 0
    maxLen = 0

    for c in str:
        if c.isalpha():
            ln += 1
            if ln > maxLen:
                maxLen = ln
        else:
            ln = 0

    return maxLen

def getImageName(pathName, forceNumeric):
    '''Compute the best new baseName for this image'''

    # If the baseName is already words, not numbers, don't rename it.
    base = os.path.splitext(os.path.basename(pathName))[0]
    maxLen = longestString(base)
    if maxLen > 3 and len([c for c in base if c.isalpha()]) > int(len(base)/2) and not forceNumeric:
        return textName(pathName)
    else:
        return dateName(pathName)

def tryRename(pathName, suffix, reallyRename):
    '''Rename pathName to new path'''

    dirName = os.path.dirname(pathName)
    baseName = getImageName(pathName, False)
    # baseName = str(random.randrange(100000,1000000)) # Give them random file names

    target = os.path.join(dirName, baseName + suffix)
    serial = 1

    if pathName != target:
        if reallyRename:
            os.rename(pathName, 'tmpdeadbeef')
        while os.path.exists(target):
            # print('NAME ALREADY TAKEN:', target)
            target = os.path.join(dirName, baseName + '_' + str(serial) + suffix)
            serial = serial + 1

        print('New name:', target)
        if reallyRename:
            os.rename('tmpdeadbeef', target)

def deleteFile(f):
    print('Deleting:', f)
    os.remove(f)

# Returns a generator
def allFiles(dirs):
    '''Lists all files in the given directories'''

    for dirPath in dirs:
        for dirName, _, filenames in os.walk(dirPath):
            for f in filenames:
                path = os.path.join(dirName, f)
                if os.path.isfile(path):
                    yield path
                elif path.endswith('.picasaoriginals'):
                    print('You should delete:', path)
                    #os.rmdir(path)

def renameImages(dirs, reallyRename):
    files = allFiles(dirs)
    for file in files:
        print('Old name:', file)
        sys.stdout.flush()
        sys.stderr.flush()

        if file.endswith('.JPG') or file.endswith('.jpg') or file.endswith('.JPEG') or file.endswith('.jpeg') or file.endswith('.jpg3'):
            tryRename(file, '.jpg', reallyRename)
        elif file.endswith('.TIF') or file.endswith('.tif') or file.endswith('.TIFF') or file.endswith('.tiff'):
            tryRename(file, '.tif', reallyRename)
        elif file.endswith('.PNG') or file.endswith('.png'):
            tryRename(file, '.png', reallyRename)
        elif file.endswith('.GIF') or file.endswith('.gif'):
            tryRename(file, '.gif', reallyRename)
        elif file.endswith('.WEBP') or file.endswith('.webp'):
            tryRename(file, '.webp', reallyRename)
        elif file.endswith('.AVI') or file.endswith('.avi'):
            tryRename(file, '.avi', reallyRename)
        elif file.endswith('.M4A') or file.endswith('.m4a'):
            tryRename(file, '.m4a', reallyRename)
        elif file.endswith('.3GP') or file.endswith('.3gp'):
            tryRename(file, '.3gp', reallyRename)
        elif file.endswith('.WMV') or file.endswith('.wmv'):
            tryRename(file, '.wmv', reallyRename)
        elif file.endswith('.MP4') or file.endswith('.mp4'):
            tryRename(file, '.mp4', reallyRename)
        elif file.endswith('.MPG') or file.endswith('.mpg'):
            tryRename(file, '.mpg', reallyRename)
        elif file.endswith('.MOV') or file.endswith('.mov'):
            tryRename(file, '.mov', reallyRename)
        elif file.endswith('.db') or file.endswith('.db (1)') or file.endswith('.ini') or file.endswith('.thm') or file.endswith('.THM') or file.endswith('.THM'):
            deleteFile(file)
        else:
            print('Ignoring:', file)

def main():
    try:
        opts, paths = getopt.getopt(sys.argv[1:], 'hm:')
        if len(paths) == 0:
            paths = ['.']

        reallyRename = True
        print('Options:', opts)
        renameImages(paths, reallyRename)
    except getopt.GetoptError as err:
        print(err)

if __name__ == '__main__':
    main()
