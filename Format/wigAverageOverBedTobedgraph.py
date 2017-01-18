#!/qbrc/software/Python-2.7.7/bin/python
# programmer : bbc
# usage:

import sys
import argparse as ap
import pandas as pd
import logging
logging.basicConfig(level=10)


def prepare_argparser():
	description = "Combine bed file and default output of UCSC::wigAverageOverBed"
	epilog = "For command line options of each command, type %(prog)% COMMAND -h"
	argparser = ap.ArgumentParser(description=description, epilog = epilog)
	argparser.add_argument("-a","--bedfile",dest = "bedfile",type=str,required=True, help="input BED file")
	argparser.add_argument("-b","--covfile",dest = "covfile",type=str,required=True, help="input coverage file")
	argparser.add_argument("-o","--output",dest = "outfile",type=str,required=True, help="output")
	argparser.add_argument("--score-type",dest = "scoretype",type=str, help="The column to use for bedgraph score", choices=['sum','mean','mean0','max','min'])
	return(argparser)


def main():
	argparser = prepare_argparser()
	args = argparser.parse_args()
	
	bedfile = pd.read_table(args.bedfile,header=None)
	covfile = pd.read_table(args.covfile, header=None)
	output = open(args.outfile,"w")

	if covfile.shape[1]==6:
		covfile.columns = ['name','size','covered','sum','mean0','mean']
	elif covfile.shape[1]==8:
		covfile.columns = ['name','size','covered','sum','mean0','mean','min','max']
	else:
		logging.error("Coverage file should has 6 or 8 columns. Exit")
		sys.exit(1)
	bedfile = bedfile.iloc[:,[0,1,2,3]]
	bedfile.columns = ['chr','start','stop','name']
	df = bedfile.merge(covfile,on='name',how='outer')
	df = df.fillna(0)
	df = df.loc[:,['chr','start','stop']+[args.scoretype]]
	df.to_csv(args.outfile,header=False, index=False, sep="\t")


if __name__=="__main__":
	main()
