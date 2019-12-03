#!/bin/python

import optparse

def load_bin_file(fname):
    with open(fname, "rb") as binary_file:
        # Read the whole file at once
        data = binary_file.read()
        return data

def save_bin_file(fname, data):
    with open(fname, "wb") as binary_file:
        # Read the whole file at once
        binary_file.write(data)

def eggify(data):
    for i in range(len(data)):
        data[i] = (~data[i]) & 0xff

parser = optparse.OptionParser()

parser.add_option("-f", "--file",
                  default='blob.bin',
                  action="store",
                  dest="infname",
                  help="Input file")

parser.add_option("-o", "--outfile",
                  default='outblob.bin',
                  action="store",
                  dest="outfname",
                  help="Output file")

(options, args) = parser.parse_args()

data = bytearray(load_bin_file(options.infname))

eggify(data)

save_bin_file(options.outfname, data)
