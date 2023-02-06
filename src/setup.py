import pandas as pd
import io
import os
import gzip
import sys

def install_fusion():
    
    if not os.path.exists(os.getcwd() + '/fusion_twas-master'):                
    
        os.system("wget https://github.com/gusevlab/fusion_twas/archive/master.zip")
        os.system("unzip master.zip")
        os.chdir("fusion_twas-master")

        os.system("wget https://data.broadinstitute.org/alkesgroup/FUSION/LDREF.tar.bz2")
        os.system("tar xjvf LDREF.tar.bz2")

        os.system("wget https://github.com/gabraham/plink2R/archive/master.zip")
        os.system("unzip master.zip")
        
        os.chdir("..")
              
    os.system("R -e \"install.packages('fusion_twas-master/plink2R-master/plink2R/',repos=NULL)\"")
    
    
    
def create_cleaned_vcf(vcf, populations, temp_loc, **kwargs):

    cd = os.getcwd()
    
    pheno = pd.DataFrame(columns=['Pop', 'Sample'])
    pops = pd.read_csv(cd + '/' + populations, sep='\t', usecols=[0, 1, 2], header=None, names=['sample', 'population', 'group'])
    pops = pops[pops['population'].isin(['GBR', 'FIN', 'CEU', 'TSI'])]
    pheno['Pop'] = pops['sample']
    pheno['Sample'] = pops['sample']
    pheno.to_csv(cd + f'/{temp_loc}/phenotype.txt',sep='\t', header=False, index=False)
    
    if not os.path.exists(os.getcwd() + f'/{temp_loc}/cleaned.bed'):
        
        os.system(f"plink --vcf {vcf} --make-bed --out {temp_loc}/cleaned --keep {temp_loc}/phenotype.txt --silent --allow-no-sex --extract fusion_twas-master/LDREF/1000G.EUR.22.bim")
            
            
            
    
        
        
    

