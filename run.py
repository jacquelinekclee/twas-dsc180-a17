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
    
    if targets[0] == 'all':
        setup.install_fusion(**data_config)
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
            os.system('rm -r data/out/weights/*')


        if 'test' in targets:
            
            pass

if __name__ == '__main__':
    
    targets = sys.argv[1:]
    main(targets)