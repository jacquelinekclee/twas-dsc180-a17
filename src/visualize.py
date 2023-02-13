import pandas as pd
import io
import os
import gzip
import sys
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats

def create_visualizations(**kwargs):
    create_locus_plot(**kwargs)
    create_herit_rsquared_scatter(**kwargs)
    get_sig_variants(**kwargs)
    create_gene_count_table(**kwargs)
    create_model_summary_table(**kwargs)

def create_locus_plot(gwas_sumstats, chromosome, out_loc, outfile, **kwargs):
    os.system(f"cat ./{out_loc}/{outfile} | awk 'NR == 1 || $NF < 0.05/2058' > ./{out_loc}/{outfile}.top")
    os.system(f"Rscript ./fusion_twas-master/FUSION.post_process.R \
    --sumstats ./{gwas_sumstats} \
    --input ./{out_loc}/{outfile}.top \
    --out ./{out_loc}/{outfile}.top.analysis \
    --ref_ld_chr ./fusion_twas-master/LDREF/1000G.EUR. \
    --chr {chromosome} \
    --plot --locus_win 100000")
    return f'./{out_loc}/{outfile}.top.analysis'

def create_herit_rsquared_scatter(out_loc, outfile, **kwargs):
    fig, ax = plt.subplots()
    ibd_dat = pd.read_csv(f'./{out_loc}/{outfile}', sep = '\t')
    plt.plot(np.arange(0,1,.1), np.arange(0,1,.1), color = 'black')
    plt.scatter(ibd_dat['HSQ'], ibd_dat['MODELCV.R2'])
    plt.xlabel('Heritability')
    plt.ylabel('R-squared')
    plt.title('Heritability vs. R-squared For Each Gene')
    plt.legend(['y = x'])
    fp = f'./{out_loc}/{outfile}_herit_rsquared_scatter.png'
    plt.savefig(fp, bbox_inches = "tight")
    return fp
    
def get_sig_variants(gwas_sumstats, out_loc, outfile, **kwargs):
    ibd_dat = pd.read_csv(f'./{out_loc}/{outfile}', sep = '\t')
    sum_stats = pd.read_csv(f'./{gwas_sumstats}', sep = '\t')
    sum_stats['pval'] = sum_stats['Z'].apply(scipy.stats.norm.cdf)
    ibd_dat_merged = ibd_dat.merge(sum_stats, left_on = 'BEST.GWAS.ID', right_on = 'SNP', suffixes  = ['_twas, _sumstats'])
    sig_snps = ibd_dat_merged.loc[ibd_dat_merged.pval < (5*10e-8)][['ID', 'SNP', 'pval', 'HSQ']]
    fp = f'./{out_loc}/{outfile}_sig_variants.csv'
    sig_snps.to_csv(fp, index = False)
    return fp

def create_gene_count_table(out_loc, outfile, expressions, **kwargs):
    cd = os.getcwd()
    genes = pd.read_csv(cd + '/' + expressions, sep='\t')
    genes22 = genes.loc[genes.Chr == '22']
    num_genes_at_start = genes22.Gene_Symbol.nunique()
    ibd_dat = pd.read_csv(f'./{out_loc}/{outfile}', sep = '\t')
    num_genes_herit = ibd_dat.ID.nunique()
    percent_genes_herit = f'{round((num_genes_herit / num_genes_at_start) * 100, 2)}%'
    rows = [('Number of Genes At Beginning',num_genes_at_start), ('Number of Genes That Are Cis-Heritable',num_genes_herit), ('% Genes Cis-Heritable',percent_genes_herit)]
    summary_table = pd.DataFrame(data = rows)
    fp = f'./{out_loc}/{outfile}_summary_table.csv'
    summary_table.to_csv(fp, index = False)
    return fp
    
def create_model_summary_table(out_loc, outfile, **kwargs):
    ibd_dat = pd.read_csv(f'./{out_loc}/{outfile}', sep = '\t')
    model_summary_table = ibd_dat['MODEL'].value_counts().to_frame().reset_index()
    model_summary_table.rename({'index':'Best Model', 'MODEL': 'Number Cis-Heritable Genes'}, inplace = True)
    fp = f'./{out_loc}/{outfile}_model_summary_table.csv'
    model_summary_table.to_csv(fp, index = False)
    return fp
    
