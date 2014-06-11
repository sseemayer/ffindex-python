#!/usr/bin/env python
import ffindex
import sys
import hashlib


if len(sys.argv) != 2:
    print("usage: {prog} ffindex_data".format(prog=sys.argv[0]))
    sys.exit(1)


for entry in ffindex.read(sys.argv[1], encoding="UTF-8"):

    m = hashlib.sha1()
    m.update(entry.read())

    print("{sha1}  -".format(name=entry.name, sha1=m.hexdigest()))
