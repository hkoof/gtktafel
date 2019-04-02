#!/usr/bin/env python3

import sys
import re    # module voor regular expressions vergelijkbaar met grep, sed enz.

def leeg(string):
    return re.match('^\s*$', string) != None

def commentaar(string):
    return re.match('^\s*#.*$', string) != None

if len(sys.argv) != 2:
    print("Usage: {} file.py".format(sys.argv[0]), file=sys.stderr)
    sys.exit(1)

filenaam = sys.argv[1]
filelezer = open(filenaam)
in_commentaarblok = False

for regel in filelezer:
    if in_commentaarblok:
        if commentaar(regel) or leeg(regel):
            continue
        else:
            print()   # wel 1 lege regel printen waar commentaar stond
            in_commentaarblok = False
    elif leeg(regel):
        in_commentaarblok = True
        continue
    print(regel, end='')

filelezer.close()
