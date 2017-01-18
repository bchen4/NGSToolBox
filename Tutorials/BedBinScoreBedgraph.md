##Get bin score for BED file and get a bedgraph output

**Input Files**

1. Bed file with regions of interest;
2. BigWig file. If you have bedgraph file, use UCSC tool bedgraghToBigWig to convert it to bigwig, follow the instructions of UCSC;

**Steps of process:**

1. Use bedbin.py to get bins;
2. (Optional) Add names for each bin if the original bed file only has 3 columns;
3. Use UCSC tools bigWigAverageOverBed to get different scores for each bin;
   
   The output columns are:
   
   Columns|Column name|Explaination
   ---|---|---|
   1 |name | name field from bed, which should be unique
   2 |size | size of bed (sum of exon sizes
   3 |covered | # bases within exons covered by bigWig
   4 |sum|   sum of values over all bases covered
   5 |mean0 |  average over bases with non-covered bases counting as zeroes
   6 |mean | average over just covered bases
   7 | min | minimum value (with -minmax turned on)
   8 | max | maximum value (with -minmax turned on)
   
4. Merge original bin file (BED format) and the output of bigWigAverageOverBed;

