#!/usr/bin/env python3

'''
Generate variant pair predicted frequencies using Hardy-Weinberg equillibrium equation. 
Usage information:
python3 predict_variant_pair_frequency_HardyWeinberg.py -f NOD2_chr16_clinvar_dbnsfp_gnomad_merged.tsv

Notes:
- The input file was pre-generated annotation file and only represents NOD2 genomic region.
- The variants were filtered to just those that are damaging according to either Polyphen2 HDIV or SIFT scores.
- The predicted frequency of variant pairs were generated using Non-Finish European (nfe) and African (afr) AFs from GNOMAD.
'''

import argparse
import pandas as pd
import numpy as np

def read_var_annotations(annotation_file):
    # Read in annotation file to df.
    d = pd.read_csv(annotation_file,sep="\t",low_memory=False)
    df = pd.DataFrame(d)

    # Extract variant identifiers, SIFT prediction, Polyphen2 HDIV prediction, GNOMAD Non-Finish European AF, and GNOMAD African AF columns.
    df = df[['pos','chr','varID','SIFT_pred','Polyphen2_HDIV_pred','AF_nfe','AF_afr']]
    df = df.dropna()

    # Remove variants that are not predicted to be damaging (D) according to Polyphen2 HDIV or SIFT.
    pathogenic_df = df[(df['Polyphen2_HDIV_pred'] == "D") | (df['SIFT_pred'] == "D")]

    # Include only columns we need.
    pathogenic_df = pathogenic_df[['varID','AF_nfe','AF_afr']]

    print(len(pathogenic_df),"unique variants predicted to be damaging according to Polyphen2 or SIFT.")

    # Compute number of unique pairs expected
    unique_pairs_n = len(pathogenic_df) * (len(pathogenic_df) - 1) / 2
    print("Expected number of unique pairs = n(n-1)/2 = ",str(unique_pairs_n))

    return pathogenic_df

def create_pathogenic_variant_pairs_table(pathogenic_df):
    # Initialize two dfs with the variant IDs to create variant pairs with. 
    variant1_df = pathogenic_df[['varID']]
    variant2_df = pathogenic_df[['varID']]

    # Create list of variant-variant pairs.
    outlist = [ (i, j)
        for i in variant1_df.varID
        for j in variant2_df.varID ]

    # Construct df of variant-variant pairs. 
    pairs_df = pd.DataFrame(data=outlist, columns=['variant1','variant2'])

    # Remove diagonals (same variant pairs).
    pairs_df = pairs_df[pairs_df['variant1'] != pairs_df['variant2']]

    # Remove redundant variant pairs.
    pairs_df = pairs_df.loc[pd.DataFrame(np.sort(pairs_df[['variant1','variant2']],1),index=pairs_df.index).drop_duplicates(keep='first').index]

    # Ensure that there are no duplicate variant pairs created.
    pairs_df = pairs_df.drop_duplicates()

    print(len(pairs_df),"unique variants pairs generated.")
    
    return pairs_df

def annotate_variant_AF(pairs_df,annotation_df):
    # Re-label annotation file columns for variant 1 merge.
    annotation_df.columns = ['variant1','AF_nfe_variant1','AF_afr_variant1']
    
    # Merge variant annotations for variant 1.
    merge_df  = pd.merge(pairs_df,annotation_df,on="variant1",how="left")

    # Re-label annotation file columns for variant 2 merge.
    annotation_df.columns = ['variant2','AF_nfe_variant2','AF_afr_variant2']

    # Merge variant annotations for variant 2.
    merge_df = pd.merge(merge_df,annotation_df,on="variant2",how="left")
    
    return merge_df

def predict_pairwise_frequency(variant_pair_df):

    # Compute 2pq percent for variants 1 and 2 for NFE AF. 
    variant_pair_df['2pq_perc_variant1_AF_nfe'] = (2 * variant_pair_df['AF_nfe_variant1'].astype(float) * (1 - variant_pair_df['AF_nfe_variant1'].astype(float))) * 100
    variant_pair_df['2pq_perc_variant2_AF_nfe'] = (2 * variant_pair_df['AF_nfe_variant2'].astype(float) * (1 - variant_pair_df['AF_nfe_variant2'].astype(float))) * 100

    # Compute 2pq percent for variants 1 and 2 for AFR AF. 
    variant_pair_df['2pq_perc_variant1_AF_afr'] = (2 * variant_pair_df['AF_afr_variant1'].astype(float) * (1 - variant_pair_df['AF_afr_variant1'].astype(float))) * 100
    variant_pair_df['2pq_perc_variant2_AF_afr'] = (2 * variant_pair_df['AF_afr_variant2'].astype(float) * (1 - variant_pair_df['AF_afr_variant2'].astype(float))) * 100

    # Compute 2pq fraction for variants 1 and 2 for NFE AF. 
    variant_pair_df['2pq_fraction_variant1_AF_nfe'] = (variant_pair_df['2pq_perc_variant1_AF_nfe'] / 100) 
    variant_pair_df['2pq_fraction_variant2_AF_nfe'] = (variant_pair_df['2pq_perc_variant2_AF_nfe'] / 100)

    # Compute variant pair AF using NFE AF 2pq fractions. 
    variant_pair_df['variant_pair_AF_nfe'] = variant_pair_df['2pq_fraction_variant1_AF_nfe'] * variant_pair_df['2pq_fraction_variant2_AF_nfe']

    # Compute 2pq fraction for variants 1 and 2 for AFR AF. 
    variant_pair_df['2pq_fraction_variant1_AF_afr'] = (variant_pair_df['2pq_perc_variant1_AF_afr'] / 100)
    variant_pair_df['2pq_fraction_variant2_AF_afr'] = (variant_pair_df['2pq_perc_variant2_AF_afr'] / 100)

    # Compute variant pair AF using AFR AF 2pq fractions. 
    variant_pair_df['variant_pair_AF_afr'] = variant_pair_df['2pq_fraction_variant1_AF_afr'] * variant_pair_df['2pq_fraction_variant2_AF_afr']

    return variant_pair_df

def write_results(variant_pair_df,out_file):
    # Write variant pair predicted frequencies to file.
    variant_pair_df.to_csv(out_file,sep="\t",index=False,header=True)
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", help = "Please input tab sep file with gene_symbol and chromosome number")
    args = parser.parse_args()
    
    # Read in NOD2 variant annotation file.
    readVariantAnnotations = read_var_annotations(args.f)
    
    # Extract only pathogenic variants according to aformentioned thresholds and generate variant pairs df.
    createPathogenicVariantPairs = create_pathogenic_variant_pairs_table(readVariantAnnotations)

    # Merge variant annotations for variant 1 and variant 2. 
    addVariantAnnotationstoPairs = annotate_variant_AF(createPathogenicVariantPairs,readVariantAnnotations)

    # Calculate the predicted variant pair frequency for African and Non-Finish European AFs from GNOMAD. 
    calculateVariantPairFrequency = predict_pairwise_frequency(addVariantAnnotationstoPairs)

    # Define output file and write results to output file. 
    out_file = "predicted_variant_pair_frequency_" + str(args.f)
    writeResults = write_results(calculateVariantPairFrequency,out_file)

if __name__ == "__main__":
    main()
