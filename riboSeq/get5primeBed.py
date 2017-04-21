#!/usr/bin/python
# programmer : bbc
# usage:

import sys
import pysam

def main():
  try:
    infile = pysam.Samfile(sys.argv[1],"r")
  except IOError,message:
    print >> sys.stderr, "cannot open file",message
    sys.exit(1)
  for item in infile:
    if not item.is_unmapped:
      chrom = infile.getrname(item.reference_id)
      positions = item.get_reference_positions()
      #print positions
      if item.is_reverse:
        strand = "-"
        start = positions[-1]
      else:
        strand = "+"
        start = positions[0]
      stop  = start+1
      print "%s" % "\t".join([chrom,str(start),str(stop),item.qname,str(item.mapping_quality),strand])  

if __name__=="__main__":
  main()
