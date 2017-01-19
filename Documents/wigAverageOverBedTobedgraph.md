**Function**
Combine bed and its coverage (output of bigWigAverageOverBed) into bedgraph

**Usage**
```python
usage: wigAverageOverBedTobedgraph.py [-h] -a BEDFILE -b COVFILE -o OUTFILE
                                      [--score-type {sum,mean,mean0,max,min}]

Combine bed file and default output of UCSC::wigAverageOverBed

optional arguments:
  -h, --help            show this help message and exit
  -a BEDFILE, --bedfile BEDFILE
                        input BED file
  -b COVFILE, --covfile COVFILE
                        input coverage file
  -o OUTFILE, --output OUTFILE
                        output
  --score-type {sum,mean,mean0,max,min}
                        The column to use for bedgraph score
```
More about score type:
   
  Column name|Explaination
---|---|
sum|   sum of values over all bases covered
mean0 |  average over bases with non-covered bases counting as zeroes
mean | average over just covered bases
min | minimum value (with -minmax turned on)
max | maximum value (with -minmax turned on)
