#!/usr/bin/env python3

'''

Prior to running:
Please download ANNOVAR. Documentation for ANNOVAR can be found here: https://annovar.openbioinformatics.org/en/latest/user-guide/download/
Use convert2annovar to generate .avinput files from a multi-sample VCF.


Usage information: python3 annotate_pathogenic_variants_annovar.py -a <annovar directory> -v <path to *.avinput files generated from convert2annovar>

'''

import argparse
import os
import subprocess as sp
import shutil

# Annotate the variations found in each annovar file created above. 
def annovar_format_to_variations(annovar_dir,annovar_formatted_files_dir):
    # Get list of your avinput files.
    master_sample_lst = os.listdir(annovar_formatted_files_dir)
    
    # Path to annotate_variation.pl script.
    annotate_variation_path = os.path.join(annovar_dir,'annotate_variation.pl')

    # Path to ANNOVAR human_db directory.
    human_db_path = os.path.join(annovar_dir,'humandb')

    # Loop over .avinput samples in directory.
    for annovar_file in master_sample_lst:
        annovar_file_path = os.path.join(annovar_formatted_files_dir,annovar_file)
        
        # Define all ANNOVAR input and output files.
        annovar_file_prefix = annovar_file.replace(".avinput","")
        out_annovar_file_log = annovar_file_path.replace(".avinput",".log")
        out_annovar_file_exonic_variant = annovar_file_path.replace(".avinput",".exonic_variant_function")
        out_annovar_file_variant = annovar_file_path.replace(".avinput",".variant_function")

        # If the .log file, exonic variant function file, and variant function file don't exist, run ANNOVAR.
        if not os.path.exists(out_annovar_file_log) and not os.path.exists(out_annovar_file_exonic_variant) and not os.path.exists(out_annovar_file_variant):
            try:
                print("ANNOVAR WRAPPER NOTICE:",out_annovar_file_log,"does not exist. Converting ANNOVAR files to variant annotated files.")
                sp.call(["perl",annotate_variation_path,"-out",annovar_file_prefix,"-build","hg38",annovar_file_path,human_db_path])
                out_annovar_file_log = os.path.join(os.getcwd(),os.path.basename(out_annovar_file_log))
                out_annovar_file_exonic_variant = os.path.join(os.getcwd(),os.path.basename(out_annovar_file_exonic_variant))
                out_annovar_file_variant = os.path.join(os.getcwd(),os.path.basename(out_annovar_file_variant))

                # Move output files to directory.
                shutil.move(out_annovar_file_log,annovar_formatted_files_dir)
                shutil.move(out_annovar_file_exonic_variant,annovar_formatted_files_dir)
                shutil.move(out_annovar_file_variant,annovar_formatted_files_dir)
                
            except sp.CalledProcessError:
                print("There was an error running ANNOVAR annotate_variation.pl script.")
                
        # If the files already exist for this iteration, skip and go to next iteration.
        else:
            print("ANNOVAR WRAPPER NOTICE:", out_annovar_file_log,out_annovar_file_exonic_variant,out_annovar_file_variant,"has already been created. Skipping this iteration.")
            pass

    return True 


def main():
    # Define arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", help = "Please enter the path to the directory all of your annovar formatted files.")
    parser.add_argument("-a", help = "Please enter the path to the ANNOVAR directory.")
    args = parser.parse_args()

    annovar_format_files_dir = args.v
    annovar_dir = args.a
    
    # Run function for annotating avinput files. 
    ANNOVAR_to_variant = annovar_format_to_variations(annovar_dir,annovar_format_files_dir)
    
if __name__ == "__main__":
    main()


