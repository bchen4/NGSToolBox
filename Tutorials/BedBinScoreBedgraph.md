##Get bin score for BED file and get a bedgraph output

**Input Files**

1. Bed file with regions of interest;
2. BigWig file. If you have bedgraph file, use [UCSC tools](http://hgdownload.soe.ucsc.edu/admin/exe/macOSX.x86_64/) bedGraghToBigWig to convert it to bigwig, follow the instructions of UCSC;

**Steps of process:**

1: Use bedbin.py to get bins;
```python
python splitBedToBin.py -i original.bed --bin-count 10 -o original_bin10.bed

```

2: (Optional) Add names for each bin if the original bed file only has 3 columns;
```python
python addBedName.py original_bin10.bed peak > original_bin10_name.bed
```

3: Use [UCSC tools](http://hgdownload.soe.ucsc.edu/admin/exe/macOSX.x86_64/) bigWigAverageOverBed to get different scores for each bin;
```shell
bigWigAverageOVerBed bigwigfile original_bin10_name.bed original_bin10_name.tab
```
   
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
   
4: Merge original bin file (BED format) and the output of bigWigAverageOverBed;
```python
python wigAverageOverBedTobedgraph.py -a original_bin10_name.bed -b original_bin10_name.tab 
         --score-type sum -o original_bin10_name.bedgraph
```


