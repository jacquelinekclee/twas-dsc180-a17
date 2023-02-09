import pandas as pd
import io
import os
import sys
import gzip
import json


import src.setup as setup
import src.fusion as fusion
import src.assoc as assoc


def main(targets):

    data_config = json.load(open('config/data-params.json'))
    
    if not os.path.exists(os.getcwd() + '/data'):                
        os.system("mkdir data")
        
    if not os.path.exists(os.getcwd() + '/data/raw'):                
        os.system("mkdir data/raw")
    
    if not os.path.exists(os.getcwd() + '/data/out'):                
        os.system("mkdir data/out")
        
    if not os.path.exists(os.getcwd() + '/data/tmp'):                
        os.system("mkdir data/tmp")
        
    if not os.path.exists(os.getcwd() + '/data/out/weights'):                
        os.system("mkdir data/out/weights")
        
    if not os.path.exists(os.getcwd() + '/test/out'):                
        os.system("mkdir test/out")
        
    if not os.path.exists(os.getcwd() + '/test/out/weights'):                
        os.system("mkdir test/out/weights")   
        
    if not os.path.exists(os.getcwd() + '/test/tmp'):                
        os.system("mkdir test/tmp")
    
    if targets[0] == 'all':
        setup.install_fusion()
        setup.create_cleaned_vcf(**data_config)
        
        fusion.fusion(**data_config)
        
        assoc.create_wgt_index(**data_config)
        assoc.run_twas(**data_config)
        
    else:
    
        if 'setup' in targets:

            setup.install_fusion()
            setup.create_cleaned_vcf(**data_config)

        if 'fusion' in targets:
            
            fusion.fusion(**data_config)
            
        if 'assoc' in targets:
            
            assoc.create_wgt_index(**data_config)
            assoc.run_twas(**data_config)
            
        if 'clean' in targets:
            
            os.system('rm -r data/tmp/*')
            os.system('rm -r data/out/*')
            
            os.system('rm -r test/tmp/*')
            os.system('rm -r test/out/*')


        if 'test' in targets:
                
            setup.install_fusion()
            setup.create_cleaned_vcf(**{**data_config, 'vcf': 'test/testdata/test_genotypes.vcf', 'expressions': 'test/testdata/test_expressions.txt', 'populations': 'test/testdata/test_populations.txt', 'temp_loc': 'test/tmp', 'out_loc': 'test/out'})
            
            fusion.fusion(**{**data_config, 'vcf': 'test/testdata/test_genotypes.vcf', 'expressions': 'test/testdata/test_expressions.txt', 'populations': 'test/testdata/test_populations.txt', 'temp_loc': 'test/tmp', 'out_loc': 'test/out'})
            
            assoc.create_wgt_index(**{**data_config, 'vcf': 'test/testdata/test_genotypes.vcf', 'expressions': 'test/testdata/test_expressions.txt', 'populations': 'test/testdata/test_populations.txt', 'temp_loc': 'test/tmp', 'out_loc': 'test/out', 'gwas_sumstats': 'test/testdata/test_sumstats.txt', 'outfile': 'test','gene_list': 'test/testdata/genelist.txt'})
            
            assoc.run_twas(**{**data_config, 'vcf': 'test/testdata/test_genotypes.vcf', 'expressions': 'test/testdata/test_expressions.txt', 'populations': 'test/testdata/test_populations.txt', 'temp_loc': 'test/tmp', 'out_loc': 'test/out', 'gwas_sumstats': 'test/testdata/test_sumstats.txt', 'outfile': 'test.dat', 'gene_list': 'test/testdata/test_genelist.txt'})
            
            
          

if __name__ == '__main__':
    
    targets = sys.argv[1:]
    main(targets)