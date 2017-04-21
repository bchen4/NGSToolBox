#!/usr/bin/python
# programmer : bbc
# usage:

import sys
import re
import random
import string

def main():
  try:
    infile = open(sys.argv[1],"r+")
  except IOError,message:
    print >> sys.stderr, "cannot open file",message
    sys.exit(1)
  for item in infile:
    buf = item.rstrip().split("\t")
    if buf[2]=="+":
      buf[5] = str(int(buf[5])-17)#modify 5'UTR and CDS start
      buf[6] = str(int(buf[6])-13)#modify 3'UTR
      buf[4] = str(int(buf[4])-28)#modify 3'UTR
      buf[3] = str(min(int(buf[3]),int(buf[5])))
      #modify introns and exons
      exon_starts = buf[8].rstrip(",").split(",")
      exon_stops = buf[9].rstrip(",").split(",")
      exon_stops[-1] = buf[4]
      new_exon_starts = [buf[5]]
      for ss in exon_starts[1:]:
        new_exon_starts.append(str((int(ss)-8)))
      buf[8] = ",".join(new_exon_starts)+","
      buf[9] = ",".join(exon_stops)+","
    elif buf[2]=="-":
      buf[6] = str(int(buf[6])+17) #modify 5' UTR
      buf[3] = str(int(buf[3])-28)
      buf[5] = str(int(buf[5])+13)
      exon_starts = buf[8].rstrip(",").split(",")
      exon_starts[0] = buf[3]
      exon_stops = buf[9].rstrip(",").split(",")
      new_exon_stops = [buf[6]]
      buf[4] = str(max(int(buf[4]),int(buf[6])))
      for st in exon_stops[0:int(buf[7])-1]:
        new_exon_stops.insert(0,str(int(st)+8))
      buf[8] = ",".join(exon_starts)+","
      buf[9] = ",".join(new_exon_stops)+","
    print "\t".join(buf)

if __name__=="__main__":
  main()
