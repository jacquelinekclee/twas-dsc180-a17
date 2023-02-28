import pandas as pd
import io
import os
import gzip
import sys


def create_pheno_plink(expressions_ch, pops, ch, gene_id, cis_thresh, temp_loc, out_loc):
    
    pheno = pd.DataFrame(columns=['Pop', 'Sample', 'Phenotype'])
    
    start = expressions_ch.iloc[int(gene_id)]['Coord'] - cis_thresh
    end = expressions_ch.iloc[int(gene_id)]['Coord'] + cis_thresh
    gene = expressions_ch.iloc[int(gene_id)][4:]
    gene = gene.rename("phenotypes")
    
    merged = pd.merge(gene, pops, left_index=True, right_on='sample')
    
    pheno['Pop'] = merged['sample']
    pheno['Sample'] = merged['sample']
    pheno['Phenotype'] = merged['phenotypes']
    
    pheno.to_csv(os.getcwd() + f'/{temp_loc}/phenotype.txt',sep='\t', header=False, index=False)
    
    os.system(f"plink --bfile {temp_loc}/cleaned --pheno {temp_loc}/phenotype.txt --make-bed --silent --out {temp_loc}/tmp --chr {str(ch)} --from-bp {start} --to-bp {end} --allow-no-sex --keep {temp_loc}/phenotype.txt")
    
    return
    
def run_fusion_script(g, temp_loc, out_loc):
    
    os.system(f"Rscript fusion_twas-master/FUSION.compute_weights.R \
--bfile {temp_loc}/tmp \
--tmp {temp_loc}/tmp.{g} \
--out {out_loc}/weights/out.{g} \
--save_hsq \
--models top1,lasso,enet \
--PATH_gcta fusion_twas-master/gcta_nr_robust")
    
    

def fusion(expressions, populations, chromosome, cis_thresh, temp_loc, out_loc, **kwargs):
    
    cd = os.getcwd()
    exp = pd.read_csv(cd + '/' + expressions, sep='\t')
    expressions_ch = exp[exp['Chr'].astype(str) == str(chromosome)]
    pops = pd.read_csv(cd + '/' + populations, sep='\t', usecols=[0, 1, 2], header=None, names=['sample', 'population', 'group'])
    pops = pops[pops['population'].isin(['GBR', 'FIN', 'CEU', 'TSI'])]

    
    for i in range(expressions_ch.shape[0]):
        create_pheno_plink(expressions_ch, pops, chromosome, i, cis_thresh, temp_loc, out_loc)
        run_fusion_script(expressions_ch.iloc[i]['Gene_Symbol'], temp_loc, out_loc)
    
    