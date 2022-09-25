#!/usr/bin/env python3
'''

Last updated: 03/11/2021

'''
import pandas as pd
import argparse
import os

def read_open_gwas_file(f):

    all_data = pd.read_csv(f,sep='\t',low_memory=False,quotechar='"')
    df = pd.DataFrame(all_data)
    df = df[['id','sample_size']]
    df = df.dropna()
    df['sample_size'] = df['sample_size'].astype(int)
    return df

def read_gwas_lst_file(d):
    files_lst = os.listdir(d)
    df = pd.DataFrame(files_lst)
    df.columns = ['id']
    df['file'] = df['id']
    df['id'] = df['id'].str.replace("format_","").str.replace(".vcf","")

    return df


def merge_data(gwas_lst_df,open_gwas_df):
    merge_df = pd.merge(gwas_lst_df,open_gwas_df,on="id")
    merge_df = merge_df[['file','sample_size']]

    merge_df.to_csv("munge_input.lst",sep="\t",index=False,header=False)
    return True



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", help = "Please input trait-id map file")
    parser.add_argument("-d", help = "Please input path to format_open_gwas_sumstats")
    args = parser.parse_args()

    readFile = read_open_gwas_file(args.f)
    readGWASlst = read_gwas_lst_file(args.d)
    mergeData = merge_data(readGWASlst,readFile)

if __name__ == "__main__":
    main()
