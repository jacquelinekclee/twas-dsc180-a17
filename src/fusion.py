import pandas as pd
import io
import os
import gzip
import sys


def create_pheno_plink(expressions_ch, pops, ch, gene_id, cis_thresh):
    pheno = pd.DataFrame(columns=['Pop', 'Sample', 'Phenotype'])
    
    start = expressions_ch.iloc[int(gene_id)]['Coord'] - cis_thresh
    end = expressions_ch.iloc[int(gene_id)]['Coord'] + cis_thresh
    gene = expressions_ch.iloc[int(gene_id)][4:]
    gene = gene.rename("phenotypes")
    
    merged = pd.merge(gene, pops, left_index=True, right_on='sample')
    
    pheno['Pop'] = merged['sample']
    pheno['Sample'] = merged['sample']
    pheno['Phenotype'] = merged['phenotypes']
    
    pheno.to_csv(os.getcwd() + '/data/tmp/phenotype.txt',sep='\t', header=False, index=False)
    
    
    
    os.system(f"plink --bfile data/tmp/cleaned --pheno data/tmp/phenotype.txt --silent --make-bed --out data/tmp/tmp --chr {str(ch)} --from-bp {start} --to-bp {end} --allow-no-sex --keep data/tmp/phenotype.txt")
    
    return
    
def run_fusion_script(g):
    
    os.system(f"Rscript fusion_twas-master/FUSION.compute_weights.R \
--bfile data/tmp/tmp \
--tmp data/tmp/tmp.{g} \
--out data/out/weights/out.{g} \
--models top1,lasso,enet \
--PATH_gcta fusion_twas-master/gcta_nr_robust")
    
    

def fusion(expressions, populations, chromosome, cis_thresh, **kwargs):
    
    cd = os.getcwd()
    exp = pd.read_csv(cd + '/' + expressions, sep='\t')
    expressions_ch = exp[exp['Chr'].astype(str) == str(chromosome)]
    pops = pd.read_csv(cd + '/' + populations, sep='\t', usecols=[0, 1, 2], header=None, names=['sample', 'population', 'group'])
    
    
    for i in range(expressions_ch.shape[0]):
        create_pheno_plink(expressions_ch, pops, chromosome, i, cis_thresh)
        run_fusion_script(expressions_ch.iloc[i]['Gene_Symbol'])
    
    