#!/usr/bin/env bash

set -e -u -o pipefail

bindir="$(dirname "$0")"


# Create .sumstats.gz file from GWAS summary statistics for input into LDSC munge_sumstats.py

# Run a single instance of LDSC munge_sumstats.py:
# ./munge_sumstats.py --sumstats V2_format_ukb-d-1448_3.vcf --N 348424 --merge-alleles w_hm3.snplist --out Neale_lab_bread_type_wholemeal_wholegrain

# This script checks to see if the output file (*.sumstats.gz) exists, if not it creates it for a single iteration. 

# Usage information: ./ldsc_munge_sumstats_batch.sh -l <path to LDSC directory> -g <path to GWAS directory> -p <GWAS summary statistics file name> -n <number of samples>

# Individual usage information: ./ldsc_genetic_correlation_batch.sh -l /storage/home/hcoda1/1/castore3/p-ggibson3-0/ldsc/ -m munge_sumstats_results/ -p Borges_CM_Omega_3 -x Borges_CM_Omega_6


# Batch usage information: cat pairs.txt | cut -d'\t' -f1,2 | xargs -P 28 -n 2 bash -c'./ldsc_genetic_correlation_batch.sh -l /storage/home/hcoda1/1/castore3/p-ggibson3-0/ldsc/ -m /munge_path/ -p $0 -x $1'
# cat pairs_first_env_variables_IBD_CD_UC.lst | cut -d' ' -f1,2 | xargs -P 2 -n 1 bash -c './ldsc_genetic_correlation_batch.sh -l /storage/home/hcoda1/1/castore3/p-ggibson3-0/ldsc/ -m /munge_sumstats_results/ -p $0 -x $1'


export ldsc_dir gwas_dir phen_gwas n

get_input() {

    while getopts l:g:p:n:h option
    do
        case "${option}"
        in
            l) ldsc_dir=${OPTARG};;
            g) gwas_dir=${OPTARG};;
            p) phen_gwas=${OPTARG};;
            n) n=${OPTARG};;
            h) echo "Use -f flag to input your file";;
            *) echo "./ldsc_genetic_correlation.sh -m /dir/to/munged/sumstats -l /dir/to/ldsc/tool -p phen1 -x phen2";;
        esac
    done
}

run_ldsc(){
	echo "${phen_gwas}"

	munge_path="${ldsc_dir}munge_sumstats.py"
	echo "$munge_path"

	cwd=$(pwd)
	w_hm3_snplist_dir="${ldsc_dir}w_hm3.snplist"

	in_file_name_path="${gwas_dir}/${phen_gwas}"

	out_file_name="${phen_gwas}"
	out_file_name_dir="open_gwas_munged_sumstats/${out_file_name}.sumstats.gz"
	out_file_name1="${out_file_name}.sumstats.gz"
	out_file_name2="${out_file_name}.log"
	
	if [ -f "$out_file_name_dir" ]
	then
		echo "$out_file_name_dir exists! Moving to next iteration."
		exit 1
	else

		echo "Munging ${phen_gwas}"

		python2 "$munge_path" --sumstats "$in_file_name_path" --N "$n" --merge-alleles "$w_hm3_snplist_dir" --out "$out_file_name"

		munge_results_dir="open_gwas_munged_sumstats"

		if [ ! -d "$munge_results_dir" ]
		then
			mkdir -p "${munge_results_dir}"
		fi

		out_file_name_result="${out_file_name}.log"

		mv "${out_file_name1}" "${munge_results_dir}"
		mv "${out_file_name2}" "${munge_results_dir}"
	fi
	
}


main () {
    get_input "$@" || exit 2
    run_ldsc
    echo "All done :)"
}

main "$@"
