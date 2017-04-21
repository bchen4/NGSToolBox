#!/usr/bin/python
# programmer : bbc
# usage:

import sys
import re
import random
import string

def main():
  try:
    bedfile = open(sys.argv[1],"r+")
    genepredfile = open(sys.argv[2],"r+")
  except IOError,message:
    print >> sys.stderr, "cannot open file",message
    sys.exit(1)
  exoncount = {}
  for row in genepredfile:
    buf = row.rstrip().split("\t")
    exoncount[buf[0]] = int(buf[7])
  for item in bedfile:
    buf = item.rstrip().split("\t")
    if buf[-1] == "UTR3":
      if buf[5]=="+":
        start = int(buf[1])-13
        stop = int(buf[2])-28
      elif buf[5]=="-":
        start = int(buf[1])+28
        stop = int(buf[2])+13
      if start<stop:
          buf[1] = str(start)
          buf[2] = str(stop)
          print "\t".join(buf)
    if buf[-1] == "UTR5":
      if buf[5]=="+":
        start = int(buf[1])
        stop = int(buf[2])-17
      elif buf[5]=="-":
        start = int(buf[1])+17
        stop = int(buf[2])
      if start<stop:
          buf[1] = str(start)
          buf[2] = str(stop)
          print "\t".join(buf)
    if buf[-1] == "Coding_intron":
      if buf[5]=="+":
        start = int(buf[1])
        stop = int(buf[2])-8
      elif buf[5]=="-":
        start = int(buf[1])+8
        stop = int(buf[2])
      if start<stop:
          buf[1] = str(start)
          buf[2] = str(stop)
          print "\t".join(buf)
    if buf[-1] == "Coding_cdsexon":
      if buf[5]=="+":
        if int(buf[4])==1:#first exon
          buf[1] = str(int(buf[1])-17)
        if int(buf[4])==exoncount[buf[3]]:#last exon
          buf[2] = str(int(buf[2])-13)
        if int(buf[4])>1 and int(buf[4])<exoncount[buf[3]]:#middle exon
          buf[1] = str(int(buf[1])-8)
        if int(buf[1])<int(buf[2]):
          print "\t".join(buf)
      elif buf[5]=="-":
        if int(buf[4])==1:#first exon
          buf[2] = str(int(buf[2])+17)
        if int(buf[4])==exoncount[buf[3]]:#last exon
          buf[1] = str(int(buf[1])+13)
        if int(buf[4])>1 and int(buf[4])<exoncount[buf[3]]:#middle exon
          buf[2] = str(int(buf[2])+8)
        if int(buf[1])<int(buf[2]):
          print "\t".join(buf)
        
if __name__=="__main__":
  main()
