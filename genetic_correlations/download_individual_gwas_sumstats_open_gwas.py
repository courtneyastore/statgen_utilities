#!/usr/bin/env python3
'''

Last updated: 03/11/2021

'''
import pandas as pd
import wget
import argparse
import os
import shutil

def read_open_gwas_file(f):

    all_data = pd.read_csv(f,sep='\t',low_memory=False,quotechar='"')
    df = pd.DataFrame(all_data)
    print(df)

    return df

def gwas_selection(df):
    # Extract GWAS summary statistics with number of total samples > 50k
    #df = df[df['sample_size'] > 10000]

    # Extract GWAS summary statistics from European cohort only
    #df = df[df['population'] == "European"]

    # Extract IDs matching substring
    #df = df[df['id'].str.contains("ukb-")]
    #df = df.dropna(subset=['id','trait'])

    # Extract only Bipolar disorder and Schizophrenia summary statistics
    df = df[(df['id'] == "ieu-b-41") | (df['id'] == "ieu-b-42")]
    print(df)

    df['ID_n'] = df['id'] + "|" + df['sample_size'].astype(str)
    df['ID_n'] = df['ID_n'].str.replace(" ","")

    id_n_lst = df['ID_n'].tolist()

    print(len(id_n_lst), "GWAS summary statistics will be extracted.")
    
    return id_n_lst

def wget_final_lst(id_n_lst):
    out_path = "new_open_gwas_sumstats"
    if not os.path.exists(out_path):
        os.mkdir(out_path)
    else:
        pass
# https://gwas.mrcieu.ac.uk/files/ieu-b-40/ieu-b-40.vcf.gz
    open_gwas_url = "https://gwas.mrcieu.ac.uk/files/"
    for i in id_n_lst:
        id_ = i.split("|")[0]
        n = i.split("|")[1].split(".")[0]
        id_url = open_gwas_url + id_ + "/" + id_ + ".vcf.gz"
        id_url = id_url.replace(" ","")
        out_file = id_ + ".vcf.gz"
        out_file = out_file.replace(" ","")
        out_file_path = str(out_path) + "/" + out_file
        out_file_path = out_file_path.replace(" ","")
        print(out_file_path)

        if not os.path.exists(out_file_path):
            wget.download(id_url)
            shutil.move(out_file, out_path)
            print("Downloading:",out_file)
            # Move file to out_path
        else:
            print(out_file_path,"exists! Moving to next iteration.")
            pass

    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", help = "Please input trait-id map file")
    args = parser.parse_args()

    readFile = read_open_gwas_file(args.f)
    gwasSelection = gwas_selection(readFile)

    wgetFinallst = wget_final_lst(gwasSelection)
    
if __name__ == "__main__":
    main()
