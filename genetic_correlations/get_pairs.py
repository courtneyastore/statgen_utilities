#!/usr/bin/env python3
'''
Extract unique pairs
'''
import pandas as pd
import numpy as np
from math import sqrt
import argparse
import shutil
import os
from itertools import combinations

def read_file(f):
    all_data = pd.read_csv(f,sep='\t',low_memory=False,names=['file','n'])
    df = pd.DataFrame(all_data)
    df['phenotypes'] = df['file'].str.replace("format_","").str.replace(".vcf","")
    phen_lst = df['phenotypes'].tolist()

    return phen_lst

def get_pairs(phen_lst):
    comb_lst = [" ".join(map(str, comb)) for comb in combinations(phen_lst, 2)]
    pairs_df = pd.DataFrame(comb_lst)
    pairs_df.columns = ['phenotype1']
    pairs_df[['phenotype1','phenotype2']] = pairs_df['phenotype1'].str.split(" ",expand=True)
    pairs_df.to_csv("genetic_correlation_input.lst",sep="\t",header=False,index=False)
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", help = "Please input munge_input.lst")
    args = parser.parse_args()

    readFile = read_file(args.f)
    getPairs = get_pairs(readFile)

    
if __name__ == "__main__":
    main()
