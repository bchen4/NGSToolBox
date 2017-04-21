#!/usr/bin/python
# programmer : bbc
# usage:

import sys

def main():
	try:
		infile = open(sys.argv[1],"r")
	except IOError,message:
		print >> sys.stderr, "cannot open file",message
		sys.exit(1)
	for item in infile:
		buf = item.rstrip().split("\t")	
			#print positions
		if buf[5]=="-":
			start = int(buf[2])-1
		else:
			start = int(buf[1])
		stop	= start+1
		buf[1] = str(start)
		buf[2] = str(stop)
		print "%s" % "\t".join(buf)	

if __name__=="__main__":
	main()
