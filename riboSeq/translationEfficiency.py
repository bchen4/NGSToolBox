#!/usr/bin/python
# programmer : bbc
# usage:

import sys
import pysam
import pandas as pd
import numpy as np
import argparse as ap
import logging

logging.basicConfig(level=10)


def prepare_argparser():
  description = "Calculate translation efficiency"
  epilog = "For command line options of each command, type %(prog)% COMMAND -h"
  argparser = ap.ArgumentParser(description=description, epilog = epilog)
  argparser.add_argument("-i","--rfp",dest = "rfpfile",type=str,required=True, help="input 5' bed file")
  argparser.add_argument("-o","--output",dest = "outfile",type=str,required=True, help="output")
  argparser.add_argument("-r","--rna",dest="rnafile",type=str,required=True, help = "Gene detail annotation")
  argparser.add_argument("-g","--gene-name",dest="gfile",type=str,required=True)
  #argparser.add_argument("-n","--name",dest="trackName",type=str,default="UserTrack",help = "track name for bedgraph header")
  return(argparser)

def align_density(rc,tc,fl):
  d = rc*1000000000.0/(tc*fl)
  return d

def main():
  argparser = prepare_argparser()
  args = argparser.parse_args()

  try:
    rfpfile = pd.read_table(args.rfpfile)
    rnafile = pd.read_table(args.rnafile)
    gfile = pd.read_table(args.gfile)
  except IOError,message:
    print >> sys.stderr, "cannot open file",message
    sys.exit(1)

  #annobed = gfile.intersect(infile, s=s_flag, S=S_flag,wo=True).saveas(args.infile+".intersect")
  #start to parse
  df = pd.merge(rfpfile, rnafile,on='transcript_id',how="right")
  print df.head()
  df = df[df['align_density_y']>0]#Only genes that are expressed
  
  df['translation_efficiency'] = df['align_density_y']/df['align_density_x']
  anno = gfile.loc[:,['transcript_id','gene_name']].drop_duplicates()
  df = df.merge(anno,on='transcript_id',how='left')
  df.to_csv(args.outfile,sep="\t",index=False)

if __name__=="__main__":
  main()
