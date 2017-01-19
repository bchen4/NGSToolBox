**Function**
Split bed entry into bins, either by bin size or the number of bins

**Usage**
```python
usage: splitBedToBin.py [-h] -i INFILE -o OUTFILE [--keep-residual]
                        [--bin-length BINLEN | --bin-count BINCOUNT]
```

**Parameter and design**

--bin-count: The total number of each bin
Program will use bed_length/bin_count to determin the length of each bin.
If residual exists:
* If residual < 0.4 * bin_len: discard residual (end up trimming the end of bed file)
* If residule >= 0.6 *bin_len: use bed_length/bin_count+1 as total number of bins (end with a smaller bin at the end of bed file)

--bin-length: The length of each bin
Program will use bed_length/bin_length to dtermin the total number of bin.
If residual exists:
* If --keep-residual is set, use bed_length/bin_length+1 as the total number of bin (end with a smaller bin at the end of bed file)
* Else discard residual (end up trimming the end of bed file)


  
