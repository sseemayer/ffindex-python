#!/usr/bin/env python
import ffindex
import sys

import Bio.SeqIO.FastaIO
import A3MIO

if len(sys.argv) != 2:
    print("usage: {prog} ffindex_data".format(prog=sys.argv[0]))
    sys.exit(1)


for entry in ffindex.read(sys.argv[1], encoding="UTF-8"):
    #for title, seq in A3MIO.SimpleA2MA3MParser(entry, format="a3m", remove_inserts=True):

    aln = list(Bio.SeqIO.FastaIO.SimpleFastaParser(entry))

    nrow = len(aln)
    ncol = len(aln[0][1])

    print("{name}\t{N}\t{L}".format(name=entry.name, N=nrow, L=ncol))
