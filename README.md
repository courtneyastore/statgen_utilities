# Statistical genetics and Bioinformatics resources
This repository contains various utilities for analyzing genetic/genomic data. Each utility is a component of larger pipelines.
### Python scripts
1. annotate_variants/annotate_pathogenic_variants_annovar.py
2. global_pathway_analysis/global_pathway_analysis.py
3. predict_variant_pair_frequency/predict_variant_pair_frequency_HardyWeinberg.py
4. genetic_correlations/download_individual_gwas_sumstats_open_gwas.py
5. genetic_correlations/format_opengwas_vcf.py
6. genetic_correlations/create_mungesumstats_input_file.py
7. genetic_correlations/get_pairs.py

### R script
1. genetic_correlations/download_open_gwas_file.R

### Bash scripts
1. genetic_correlations/ldsc_munge_sumstats_batch.sh
2. genetic_correlations/ldsc_genetic_correlation_batch.sh

## Variant annotation
### Requirements
* Python 3.7
* Perl 
* ANNOVAR: a tool for functional annotation of variants. Can be downloaded by filling out this form: https://www.openbioinformatics.org/annovar/annovar_download_form.php 

### Steps
1. Navigate to annotate_variants directory
```sh
  cd annotate_variants
```
2. Run conver2annovar.pl to create annovar-formatted files for variant annotation.
```sh
perl convert2annovar.pl -format vcf4 <multi-sample VCF> -allsample -outfile output_annovar
```
3. Create output directory.
 ```sh
  mkdir avinput_output
  ```
4. Move avinput files to avinput_output.
```sh
  mv *.avinput avinput_output/
```
5. Annotate variants for each sample.
```sh
  python3 annotate_pathogenic_variants_annovar.py -a <annovar directory> -v avinput_output
```
### Outputs
* output_annovar{sample_id}.exonic_variant_function
* output_annovar{sample_id}.variant_function
* output_annovar{sample_id}.log

## Global pathway analysis
### Requirements
* Python 3.7
* Pandas: Installation instructions can be found here: https://pypi.org/project/pandas/
* reactome2py: Installation instructions can be found here: https://github.com/reactome/reactome2py

### Steps
1. Navigate to global_pathway_analysis directory
```sh
  cd global_pathway_analysis
```
2. Generate an input list of proteins (Gene Symbols). One Gene Symbol per line. An example input file was created: /global_pathway_analysis/pathway_analysis_input.txt
3. Run wrapper for Reactome Global Pathway Analysis via Reactome content and analysis services API using your input set of proteins.
```sh
  python3 global_pathway_analysis.py -f pathway_analysis_input.txt
```
### Outputs
* significant_pathways_pathway_analysis_input.txt

## Predicting variant pair frequencies for Non-Finnish European and African GNOMAD AFs
### Requirements
* Python 3.7
* Pandas: Installation instructions can be found here: https://pypi.org/project/pandas/
* Numpy: Installation instructions can be found here: https://numpy.org/install/

### Steps
1. Navigate to predict_variant_pair_frequency directory
```sh
  cd predict_variant_pair_frequency
```
2. An example input file was pre-generated, which contains annotations for the NOD2 genomic region. This annotations include GNOMAD AFs and various pathogenicity scores (e.g., Polyphen2 HDIV and SIFT): /predict_variant_pair_frequency/NOD2_chr16_clinvar_dbnsfp_gnomad_merged.tsv
3. Predict the pairwise frequency of the pathogenic (damaging according to either Polyphen2 HDIV or SIFT scores) NOD2 variants via Hardy-Weinberg equation:
```sh
  python3 predict_variant_pair_frequency_HardyWeinberg.py -f NOD2_chr16_clinvar_dbnsfp_gnomad_merged.tsv
```

### Outputs
* predicted_variant_pair_frequency_NOD2_chr16_clinvar_dbnsfp_gnomad_merged.tsv

## Genetic correlation analysis
### Requirements
* Data acquisition 
	* Python 3.7
	* Pandas: Installation instructions can be found here: https://pypi.org/project/pandas/
	* Wget: Installation instructions can be found here: https://pypi.org/project/wget/
	* R 3.6
	* TwoSampleMR: Installation instructions can be found here: https://mrcieu.github.io/TwoSampleMR/
* Running genetic correlation
	* Python 2
	* LDSC tool: Installation instructions can be found here: https://github.com/bulik/ldsc

### Steps
1. Navigate to genetic_correlations directory
```sh
  cd genetic_correlations
```
2. Create Open GWAS available outcomes file (open_gwas_file.tsv).
```sh
  Rscript download_open_gwas_file.R
```
3. Extract the summary statistics from Open GWAS. Only Schizophrenia and Bipolar disorder GWAS summary statistics are extracted for example purposes. This will create a new directory storing the summary statistics: new_open_gwas_sumstats
```sh
  python3 download_individual_gwas_sumstats_open_gwas.py -f open_gwas_file.tsv
```
4. Format the summary statistics for input into LDSC. This will create a new directory storing the formatted summary statistics: format_open_gwas_sumstats
```sh
  python3 format_opengwas_vcf.py -d new_open_gwas_sumstats
```
5. Create munge sumstats batch input file. This will create munge_input.lst file
```sh
  python3 create_mungesumstats_input_file.py -f open_gwas_file.tsv -d format_open_gwas_sumstats
```
6. Create genetic correlation batch input file. This will create genetic_correlation_input.lst file
```sh
  python3 get_pairs.py -f munge_input.lst
```
7. Activate conda environment for LDSC.
```sh
  source activate ldsc
```
8. Download pre-computed LD-scores and SNP lists shown here: https://github.com/bulik/ldsc/wiki/Heritability-and-Genetic-Correlation
```sh
  wget https://data.broadinstitute.org/alkesgroup/LDSCORE/eur_w_ld_chr.tar.bz2
  tar -jxvf eur_w_ld_chr.tar.bz2
  mv eur_w_ld_chr ldsc/

  wget https://data.broadinstitute.org/alkesgroup/LDSCORE/w_hm3.snplist.bz2
  bunzip2 w_hm3.snplist.bz2
  mv w_hm3.snplist ldsc/
```
9. Run LDSC munge_sumstats function. This will create new directory storing the munged summary statistics: open_gwas_munged_sumstats
```sh
  cat munge_input.lst | cut -f1,2 | xargs -P 2 -n 2 bash -c './ldsc_munge_sumstats_batch.sh -l ldsc/ -g format_open_gwas_sumstats -p $0 -n $1'
```
10. Run LDSC to calculate genetic correlation between trait pairs in genetic_correlation_input.lst file. This will create a new directory storing the .log genetic correlations: genetic_correlation_pairwise
```sh
  cat genetic_correlation_input.lst | cut -f1,2 | xargs bash -c './ldsc_genetic_correlation_batch.sh -l ldsc/ -m open_gwas_munged_sumstats/ -p $0 -x $1'
```
11. Navigate to genetic_correlation_pairwise and explore trait correlations in the .log files. 
```sh
  cd genetic_correlation_pairwise
  grep -A1 "p1" ieu-b-42_ieu-b-41.log
```

### Outputs
* open_gwas_file.tsv
* new_open_gwas_sumstats/
* format_open_gwas_sumstats/
* open_gwas_munged_sumstats/
* genetic_correlation_pairwise/

### It looks like we get an rg value of 0.7748 and a p close to 0, which is expected according to literature: https://www.sciencedirect.com/science/article/pii/S0140673609600726?via%3Dihub

