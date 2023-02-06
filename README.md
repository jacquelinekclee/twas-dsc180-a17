# Transcriptome-Wide Association Study

## Running the analysis

This repository provides a pipeline to perform a TWAS analysis.

To run the analysis, run `python run.py all`

If running another analysis with the same gene expression and variant data but different GWAS summary statistics, we do not need to recompute weights for each gene. Just run  `python run.py assoc` with an updated data-params.json

To run the respository on test data, run `python run.py test`

## Obtaining raw data

The primary vcfs used in the analysis can be downloaded from [here](http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20110521/ALL.chr22.phase1_release_v3.20101123.snps_indels_svs.genotypes.vcf.gz) and [here](http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20110521/ALL.chr22.phase1_release_v3.20101123.snps_indels_svs.genotypes.vcf.gz.tbi). This analysis used the Chromosome 22 vcfs.

The gene expression data can downloaded from [here](https://zenodo.org/record/6998955) (The file beginning with GD462).

The population data can be downloaded from [here](http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20110521/phase1_integrated_calls.20101123.ALL.panel).

Various summary statistic files can be downloaded from [here](https://github.com/TiffanyAmariuta/TCSC/tree/main/sumstats) based on a disease of interest.

[This file](https://drive.google.com/uc?export=download&id=1gd6FP4qlteo1dBoAH8zGkXzbZvs2PPt4), which provides IDs and locations for various genes, is also required for plotting purposes.

All of these files should be placed directly in data/raw
