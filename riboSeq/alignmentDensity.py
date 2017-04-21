#!/usr/bin/python
# programmer : bbc
# usage:

import sys
import pysam
from pysam import *
from pybedtools import BedTool
import pandas as pd
import numpy as np
import argparse as ap
import logging

logging.basicConfig(level=10)


def prepare_argparser():
  description = "Calculate alignment density, CDS level"
  epilog = "For command line options of each command, type %(prog)% COMMAND -h"
  argparser = ap.ArgumentParser(description=description, epilog = epilog)
  argparser.add_argument("-i","--input",dest = "infile",type=str,required=True, help="input 5' bed file")
  argparser.add_argument("-o","--output",dest = "outfile",type=str,required=True, help="output")
  argparser.add_argument("-g","--gene",dest="gfile",type=str,required=True, help = "Gene detail annotation")
  argparser.add_argument("-s","--strandtype",dest="strand",type=str,default="none", choices=["none","sense","reverse"])
  argparser.add_argument("-f","--feature",dest="feature",type=str,default="Coding_cdsexon", help="The genomic feature user want to use for alignment density calculation. Default is Coding_cdsexon")
  return(argparser)

def align_density(rc,tc,fl):
  d = rc*1000000000.0/(tc*fl)
  return d

def sumLen(df):
  df['len'] = df.iloc[:,1]-df.iloc[:,0]
  return sum(df['len'])

def main():
  argparser = prepare_argparser()
  args = argparser.parse_args()

  try:
    infile = BedTool(args.infile)
    gfile = BedTool(args.gfile)
  except IOError,message:
    print >> sys.stderr, "cannot open file",message
    sys.exit(1)
  if args.strand == "none":
    s_flag = False
    S_flag = False
  elif args.strand == "sense":
    s_flag = True
    S_flag = False
  elif args.strand == "reverse":
    s_flag = False
    S_flag = True

  annobed = gfile.intersect(infile, s=s_flag, S=S_flag,wao=True).saveas(args.infile+".intersect")
  #start to parse
  annofile = pd.read_table(args.infile+".intersect",header=None)
  #annofile = annofile.loc[:,0:7]
  annofile.columns = ['f_chrom','f_start','f_stop','transcript_id','score','strand','gene_id','annotype','r_chrom','r_start','r_stop','r_id','r_mapq','r_strand','overlap_len']
  cds_df = annofile[annofile['annotype']=="Coding_cdsexon"].iloc[:,0:7].drop_duplicates()#keep all transcripts
  t_len_df = pd.DataFrame({'total_len': cds_df.groupby("transcript_id").apply(lambda x:sumLen(x.loc[:,['f_start','f_stop']]))}).reset_index()
  covered_df = annofile[annofile['overlap_len']>0]
  #cds_covered = covered_df[covered_df['annotype']=="Coding_cdsexon"].iloc[:,0:7]
  cds_covered = covered_df[covered_df['annotype']==args.feature].iloc[:,0:7]
  total_cds_count = cds_covered.shape[0]
  #logging.debug(total_cds_count)
  tdf = pd.DataFrame({'total_count':cds_covered.groupby('transcript_id').size()}).reset_index()
  #print tdf.head()
  tc_df = pd.merge(t_len_df,tdf,on="transcript_id")
  #print tc_df.head()
  tc_df['align_density']=tc_df.apply(lambda x: align_density(x['total_count'],total_cds_count, x['total_len']),axis=1)
  tc_df.to_csv(args.outfile,sep="\t",index=False)

if __name__=="__main__":
  main()
