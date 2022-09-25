#!/usr/bin/env python3
'''
Clean-up/format GWAS summary statistics extracted from Open GWAS

'''
import pandas as pd
import numpy as np
from math import sqrt
import argparse
import os

def read_file(f):

    if not os.path.exists("format_open_gwas_sumstats"):
        os.mkdir("format_open_gwas_sumstats")
    else:
        pass
 
    out_file = "format_open_gwas_sumstats/" + "format_" + os.path.basename(str(f)).replace(".gz","")


    if not os.path.exists(out_file):
        all_data = pd.read_csv(f,sep='\t',low_memory=False,comment="#",names=["CHROM","POS","ID","REF","ALT","QUAL","FILTER","INFO","FORMAT","GWAS"])
        df = pd.DataFrame(all_data)

        current_header = df.columns.values
        gwas_info = df['FORMAT'].iloc[0].split(":")

        df[gwas_info] = df['GWAS'].str.split(':', n=len(gwas_info), expand=True)

        df = df[['CHROM','POS','ID','REF','ALT','ES','SE','LP']]

        df['P'] = df['LP'].astype(float) * -1
        df['P'] = np.power(10,df['P'])

        df = df[['CHROM','POS','ID','REF','ALT','ES','SE','P']]

        df.columns = ['CHROM','POS','SNP','A1','A2','ES','beta','P']

        df.to_csv(out_file,sep="\t",index=False,header=True)
        
        print("Writing",str(f),"to",out_file)
    else:
        print(out_file,"already exists!")
        pass

    return True



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", help = "Please input path to new_open_gwas_sumstats")
    args = parser.parse_args()

    gwas_sumstat_files = os.listdir(args.d)

    for gwas in gwas_sumstat_files:
        input_file = str(args.d) + "/" + gwas
        readFile = read_file(input_file)

    
if __name__ == "__main__":
    main()
