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
  count =1
 
  for item in infile:
    buf = item.rstrip().split("\t")
    name = sys.argv[2]+str(count)
    count +=1
    #print "\t".join(buf[0:3]+[name,"0",buf[3]])
    print "\t".join(buf[0:3]+[name,"0"]+buf[3:])
if __name__=="__main__":
  main()
