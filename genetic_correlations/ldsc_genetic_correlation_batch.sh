#!/usr/bin/env bash

set -e -u -o pipefail

bindir="$(dirname "$0")"


#  *******************************************************************
#  *******-Batch input for running genetic correlation via LDSC-******
#  *******************************************************************

# Individual usage information: ./ldsc_genetic_correlation_batch.sh -l /storage/home/hcoda1/1/castore3/p-ggibson3-0/ldsc/ -m munge_sumstats_results/ -p Borges_CM_Omega_3 -x Borges_CM_Omega_6
# Batch usage information: cat pairs.txt | cut -d'\t' -f1,2 | xargs -P 28 -n 2 bash -c'./ldsc_genetic_correlation_batch.sh -l /storage/home/hcoda1/1/castore3/p-ggibson3-0/ldsc/ -m /munge_path/ -p $0 -x $1'
# cat pairs_first_env_variables_IBD_CD_UC.lst | cut -d' ' -f1,2 | xargs -P 2 -n 1 bash -c './ldsc_genetic_correlation_batch.sh -l /storage/home/hcoda1/1/castore3/p-ggibson3-0/ldsc/ -m /munge_sumstats_results/ -p $0 -x $1'

export ldsc_dir munge_dir phen1_gwas phen2_gwas

get_input() {

    while getopts l:m:p:x:h option
    do
        case "${option}"
        in
            l) ldsc_dir=${OPTARG};;
            m) munge_dir=${OPTARG};;
            p) phen1_gwas=${OPTARG};;
            x) phen2_gwas=${OPTARG};;
            h) echo "Use -f flag to input your file";;
            *) echo "./ldsc_genetic_correlation.sh -m /dir/to/munged/sumstats -l /dir/to/ldsc/tool -p phen1 -x phen2";;
        esac
    done
}

run_ldsc(){
	echo "$phen1_gwas"
	echo "$phen2_gwas"
	#phen1_gwas="$1"
	#phen2_gwas="$2"
	ldsc_path="${ldsc_dir}ldsc.py"

	eur_w_ld_chr_dir="${ldsc_dir}eur_w_ld_chr/"

	out_file_name="${phen1_gwas}_${phen2_gwas}"
	out_file_name_log_dir="genetic_correlation_pairwise/${out_file_name}.log"

	if [ -f "$out_file_name_log_dir" ]
	then
		echo "$out_file_name_log_dir exists! Moving to next iteration."
		exit 1
	else
		phen1_gwas_dir="${munge_dir}format_${phen1_gwas}.vcf.sumstats.gz"
		phen2_gwas_dir="${munge_dir}format_${phen2_gwas}.vcf.sumstats.gz"

		echo "${phen1_gwas_dir} and ${phen2_gwas_dir}"
		rg_var="${phen1_gwas_dir},${phen2_gwas_dir}"

		python2 "$ldsc_path" --rg "$rg_var" --ref-ld-chr "$eur_w_ld_chr_dir" --w-ld-chr "$eur_w_ld_chr_dir" --out "$out_file_name"

		gen_corr_results_dir="genetic_correlation_pairwise"

		if [ ! -d "$gen_corr_results_dir" ]
		then
			mkdir -p "${gen_corr_results_dir}"
		fi

		out_file_name_result="${out_file_name}.log"

		mv "${out_file_name_result}" "${gen_corr_results_dir}"
	fi
	
}


main () {
    get_input "$@" || exit 2
    run_ldsc
    echo "All done :)"
}

main "$@"
