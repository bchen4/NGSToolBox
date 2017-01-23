#!/usr/bin/python
# programmer : bbc
# usage:

import sys
import re
import pandas as pd
import numpy as np
from scipy.stats import zscore
import argparse as ap
import logging

logging.basicConfig(level=10)


def prepare_argparser():
  description = "Make wig file for given bed using bam"
  epilog = "For command line options of each command, type %(prog)% COMMAND -h"
  argparser = ap.ArgumentParser(description=description, epilog = epilog)
  argparser.add_argument("-i","--input",dest = "infile",type=str,required=True, help="input BAM file")
  argparser.add_argument("-o","--output",dest = "outfile",type=str,required=True, help="output")
  argparser.add_argument("--axis",dest="axis",type=int,required=True,default=0, help = "1 by row, 0 by column")
  return(argparser)



def main():
  argparser = prepare_argparser()
  args = argparser.parse_args()

  try:
    infile = pd.read_table(args.infile,index_col=0)
  except IOError,message:
    print >> sys.stderr, "cannot open file",message
    sys.exit(1)
  df = infile.apply(lambda x: zscore(np.array(x)) ,axis=args.axis).reset_index()
  df.to_csv(args.outfile,sep="\t",index=False)

if __name__=="__main__":
  main()
