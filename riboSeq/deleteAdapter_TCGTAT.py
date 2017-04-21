#!/usr/bin/python
# programmer : bbc
# usage:

import sys
import re
import random
import string

def findsubloc(st,seed):
	'''Return a list with locations'''
	return [m.start() for m in re.finditer(seed,st)]

def main():
	try:
		infile = open(sys.argv[1],"r+")
	except IOError,message:
		print >> sys.stderr, "error in openning file",message
		sys.exit(1)
	
	#ada = 'CTGTAGGCACCATCAATCGTATGCCGTCTTCTGCTTG'
	ada_seed = 'TCGTAT'
	buf = infile.readlines()	
	seqbuf = []
	for index in range(len(buf)):
		if buf[index][0]=='@' and buf[index+2][0]=="+":
			seqbuf.append(buf[index].strip())
			seqbuf.append(buf[index+1].strip())
			seqbuf.append(buf[index+2].strip())
			seqbuf.append(buf[index+3].strip())
			#start to find out the adapter seq
			a =	findsubloc(buf[index+1],ada_seed)
			b = re.findall('^N*',buf[index+1])
			start_index = 0
			stop_index = len(seqbuf[1])
			if len(a)>0:
				stop_index = a[-1]	
			if len(b)>0:
				start_index = len(b[0])
			if stop_index - start_index >=25:
				print seqbuf[0]
				print seqbuf[1][start_index:stop_index]
				print seqbuf[2]
				print seqbuf[3][start_index:stop_index]
			#initialize
			seqbuf=[]
			index = index+4


if __name__=="__main__":
	main()
