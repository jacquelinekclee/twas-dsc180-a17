import pandas as pd
import io
import os
import gzip
import sys

def create_wgt_index(expressions, **kwargs):
    
    cd = os.getcwd()
    
    exp = pd.read_csv(cd + '/' + expressions, sep='\t')
    
    df = pd.DataFrame(columns=['WGT', 'ID', 'CHR', 'P0', 'P1'])
    df['WGT'] = os.listdir(cd + '/data/out/weights')
    df = df[df['WGT'] != '.ipynb_checkpoints'].reset_index(drop=True)
    df['WGT'] = 'weights/' + df['WGT']

    df['ID'] = df['WGT'].str.split('.').str[1] +'.'+ df['WGT'].str.split('.').str[2]

    merged = pd.merge(df, exp, left_on = 'ID', right_on = 'Gene_Symbol')

    df['CHR'] = merged['Chr'].astype(int)
    df['P0'] = merged['Coord']
    df['P1'] = merged['Coord'] + 3000

    df.to_csv(cd + '/data/tmp/wgtlist.txt', index=False, sep='\t')
    
def run_twas(gwas_sumstats, chromosome, outfile, **kwargs):
    os.system(f"Rscript ./fusion_twas-master/FUSION.assoc_test.R \
    --sumstats ./{gwas_sumstats} \
    --weights ./data/tmp/wgtlist.txt \
    --weights_dir ./data/out/ \
    --ref_ld_chr ./fusion_twas-master/LDREF/1000G.EUR. \
    --chr {chromosome} \
    --out ./data/out/{outfile}")