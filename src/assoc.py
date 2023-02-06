import pandas as pd
import io
import os
import gzip
import sys

def create_wgt_index(genelist, temp_loc, out_loc, **kwargs):
    
    cd = os.getcwd()
    
    genes = pd.read_csv(cd + '/' + genelist, sep='\t')
    
    df = pd.DataFrame(columns=['WGT', 'ID', 'CHR', 'P0', 'P1'])
    df['WGT'] = os.listdir(cd + f'/{out_loc}/weights')
    df = df[df['WGT'] != '.ipynb_checkpoints'].reset_index(drop=True)
    df['WGT'] = 'weights/' + df['WGT']

    df['ID'] = df['WGT'].str.split('.').str[1] +'.'+ df['WGT'].str.split('.').str[2]

    merged = pd.merge(df, genes, left_on = 'ID', right_on = 'Gene_Symbol')

    df['CHR'] = merged['Chr'].astype(int)
    df['ID'] = merged['Name']
    df['P0'] = merged['Start']
    df['P1'] = merged['End']

    df.to_csv(cd + f'/{temp_loc}/wgtlist.txt', index=False, sep='\t')
    
def run_twas(gwas_sumstats, chromosome, outfile, temp_loc, out_loc, **kwargs):
    os.system(f"Rscript ./fusion_twas-master/FUSION.assoc_test.R \
    --sumstats ./{gwas_sumstats} \
    --weights ./{temp_loc}/wgtlist.txt \
    --weights_dir ./{out_loc}/ \
    --ref_ld_chr ./fusion_twas-master/LDREF/1000G.EUR. \
    --chr {chromosome} \
    --out ./{out_loc}/{outfile}")