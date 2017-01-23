#!/qbrc/software/Python-2.7.7/bin/python
# programmer : bbc
# usage:

import sys
import argparse as ap
import pandas as pd
import logging
logging.basicConfig(level=10)


def prepare_argparser():
  description = "Transcform UCSC::wigAverageOverBed output to matrix. Require name contains peak information and bin information"
  epilog = "For command line options of each command, type %(prog)% COMMAND -h"
  argparser = ap.ArgumentParser(description=description, epilog = epilog)
  argparser.add_argument("-i","--infile",dest = "infile",type=str,required=True, help="input coverage file")
  argparser.add_argument("-o","--output",dest = "outfile",type=str,required=True, help="output")
  argparser.add_argument("--score-type",dest = "scoretype",type=str, help="The column to use for bedgraph score", choices=['sum','mean','mean0','max','min'])
  argparser.add_argument("--bin-count",dest = "bincount",type=int, help="The number of bins for each peak", required=True)
  argparser.add_argument("--bin-name",dest = "binname",type=str, help="The name prefix of bins for each peak", default= "bin")
  argparser.add_argument("--pattern",dest = "pattern",type=str, help="Peak name and bin separator. '_,1' means peak name and bin number are separated by _ and name takes 1", required=True)
  return(argparser)


def main():
  argparser = prepare_argparser()
  args = argparser.parse_args()
  
  infile = pd.read_table(args.infile, header=None)
  (delimitor, count) = args.pattern.split(",")
  count = int(count)

  output = open(args.outfile,"w")

  if infile.shape[1]==6:
    infile.columns = ['name','size','covered','sum','mean0','mean']
  elif infile.shape[1]==8:
    infile.columns = ['name','size','covered','sum','mean0','mean','min','max']
  else:
    logging.error("Coverage file should has 6 or 8 columns. Exit")
    sys.exit(1)
  infile['peakname'] = infile['name'].apply(lambda x: delimitor.join(x.split(delimitor)[0:count]))
  infile['binname'] = infile['name'].apply(lambda x: int(x.split(delimitor)[-1]))
  group_dic = {}
  names = []
  for name, group in infile.groupby('peakname'):
    new_group_dic = group.set_index('binname')[args.scoretype].to_dict()
    names.append(name)
    if len(group_dic.items())==0:
      for k in new_group_dic.keys():
        group_dic[k] = [new_group_dic[k]]
    else:
      for k in group_dic.keys():
        group_dic[k].append(new_group_dic[k])
  df = pd.DataFrame(group_dic)
  update_col = df.columns.tolist()
  for n in range(len(update_col)):
    update_col[n] = args.binname+"_"+str(update_col[n])
  df.columns = update_col
  df['peakname'] = names
  df = df.loc[:,['peakname']+update_col]
  df.to_csv(args.outfile, index=False, sep="\t")


if __name__=="__main__":
  main()
