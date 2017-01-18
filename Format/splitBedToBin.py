#!/usr/bin/python
# programmer : bbc
# usage: split bed entries to bin. User can set bin count or bin length
# When specified bin length, if the last bin did not make 60% of the given
# length, it could be deleted

import sys
import argparse as ap
import logging

logging.basicConfig(level=10)


def prepare_argparser():
	description = "Split bed to bin"
	epilog = "For command line options of each command, type %(prog)% COMMAND -h"
	argparser = ap.ArgumentParser(description=description, epilog = epilog)
	argparser.add_argument("-i","--input",dest = "infile",type=str,required=True, help="input bed file")
	argparser.add_argument("-o","--output",dest = "outfile",type=str,required=True, help="output")
	argparser.add_argument("--keep-residual",dest = "keep",action="store_true", default=False, help="Keep the residual bin even if it is not at least 60% length of requred. Work only with --bin-length")
	group = argparser.add_mutually_exclusive_group()
	group.add_argument("--bin-length",dest = "binlen",type=int, help="The length of each bin")
	group.add_argument("--bin-count",dest = "bincount",type=int, help="The total number of bins")

	return(argparser)


def splitByLength(start,stop,length,keep):
	bincount = (stop-start)/length
	if (stop-start)%length!=0 and keep:
		bincount = (stop-start)/length + 1
	binstarts = []
	binstops = []
	for i in range(bincount):
		binstarts.append(str(start+i*length))
		binstops.append(str(min(stop,start+(i+1)*length)))
	return (binstarts, binstops)

def splitByCount(start, stop, count):
	binlen = (stop-start)/count
	residual = (stop-start)%count
	if float(residual)/binlen >= 0.6:
		binlen += 1
	binstarts = []
	binstops = []
	for i in range(count):
		binstarts.append(str(start+i*binlen))
		binstops.append(str(min(stop,start+(i+1)*binlen)))
	return (binstarts, binstops)


def main():
	argparser = prepare_argparser()
	args = argparser.parse_args()

	try:
		infile = open(args.infile,"r")
		outfile = open(args.outfile,"w")
	except IOError,message:
		print >> sys.stderr, "cannot open file",message
		sys.exit(1)
	for row in infile:
		buf =	row.rstrip().split("\t")
		start = int(buf[1])
		stop = int(buf[2])
		if isinstance(args.binlen,int):
			(binstarts, binstops) = splitByLength(start,stop,args.binlen,keep=args.keep)
		else:
			(binstarts, binstops) = splitByCount(start,stop,args.bincount)

		for i in range(len(binstarts)):
			if len(buf)>3:
				buf[3] = buf[3]+"_"+str(i+1)
			buf[1] = binstarts[i]
			buf[2] = binstops[i]
			print >> outfile,"\t".join(buf)
if __name__=="__main__":
	main()
