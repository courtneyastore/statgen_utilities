#!/usr/bin/env python3
'''
Wrapper for Global Pathway Analysis via Reactome content and analysis services API.

Usage information:
python3 global_pathway_analysis.py -f <input proteins (Gene Symbol) file. One Gene Symbol on each line> 

Notes:
- Please double-check that you have the required dependencies on your system (pandas, reactome2py, etc.).
- reactome2py package information can be found here: https://github.com/reactome/reactome2py
- Input file must contain one Gene Symbol per line.
- Only nominally significant pathways are reported, though you may change the p-value threshold on line 57.

'''
import pandas as pd
from reactome2py import content, analysis
import argparse

def read_input_protein_file(f):
    # Read input proteins to df.
    all_data = pd.read_csv(f,sep='\t',low_memory=False, names=["GeneName"])
    df = pd.DataFrame(all_data)

    # Make sure the Gene Symbols are all in lower 
    df['GeneName'] = df['GeneName'].str.lower()
    
    return(df)

def global_pathway_analysis(proteins_df):
    # Append input proteins to list.
    protein_list_ = proteins_df['GeneName'].tolist()
    print(len(protein_list_),"proteins inputted.")
    
    # Remove potential duplicate proteins from list.
    non_red_protein_list_ = []
    for i in protein_list_:
        if i not in non_red_protein_list_:
            non_red_protein_list_.append(i)

    # Format non-redunduant list of proteins for reactome input.       
    protein_list_ = str(non_red_protein_list_).replace("[","").replace("]","").replace("'","").replace(" ","")

    # Run Reactome Global Pathway Analysis via Reactome content and analysis services API.
    result = analysis.identifiers(ids=protein_list_,include_disease=True)
    token = result['summary']['token']

    # Convert Reactome output to pandas df.
    pathways = analysis.pathway2df(token, resource='TOTAL')

    # Ensure p-value calculation is numeric, if not errors='coerce' will insert NaN.
    pathways['Entities pValue'] = pd.to_numeric(pathways['Entities pValue'],errors='coerce')

    # Remove pathways with NaN.
    pathways = pathways.dropna(subset=['Entities pValue'])

    # Extract significant pathways (i.e. those with p-value < 0.05).
    pathways = pathways.loc[(pathways['Entities pValue'] < 0.05)]

    # Ensure that the species is for Homo sapiens.
    pathways = pathways.loc[(pathways['Species name'] == "Homo sapiens")]

    # Pathway identifier, Pathway name, #Entities found, #Entities total, Entities ratio, Entities pValue, Entities FDR
    pathways = pathways[['Pathway identifier','Pathway name','#Entities found','#Entities total','Entities ratio','Entities pValue']]
    
    print(len(pathways),"nominally significant pathways identified (p-value<0.05).")

    return pathways

def write_results(pathways,out_file):
    # Write significant pathways to file.
    pathways.to_csv(out_file,sep="\t",index=False,header=True)
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", help = "Please input a list of Gene Symbols you would like to perform Global Pathway analysis on.")
    args = parser.parse_args()

    # Read in file and re-structure for global pathway analysis.
    inputProteins = read_input_protein_file(args.f)
    
    # Perform global pathway analysis on input set of proteins.
    globalPathwayAnalysis = global_pathway_analysis(inputProteins)

    # Define output file name.
    out_file_name = "significant_pathways_" + str(args.f)

    # Write significant pathways to output file.
    writeResults = write_results(globalPathwayAnalysis,out_file_name)

if __name__ == "__main__":
    main()
