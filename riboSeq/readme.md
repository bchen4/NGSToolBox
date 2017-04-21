### Ribo-seq analysis scripts and pipeline

### Reads analysis
1. Use cutadapt to trim the adaptors. Depending on the experiment design, get rid of the short sequences (< 20nt) after trimming
    * Check for low quality and repetitive reads
2. Align trimmed sequences to the genome, keep uniquely mapped reads
    * Eliminate any reads could be mapped to rRNAs 
3. Calculate reads/alignment density;
    * Reads/Alignment density; scale read counts for each feature by feature length and by the total number of CDS-aligned reads
    * When assign reads to a feature, use the 5' location of reads
4. Calculate ribosome density / 
5. Calculate translation efficiency: the ratio of ribosome footprints to mRNA fragments

### Annotation preparation




### Scripts description
