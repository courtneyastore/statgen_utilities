# Statistical genetics and Bioinformatics resources
This repository contains various utilities for analyzing genetic/genomic data. Each utility is a component of larger pipelines.
### Python scripts
1. annotate_variants/annotate_pathogenic_variants_annovar.py
2. global_pathway_analysis/global_pathway_analysis.py
3. predict_variant_pair_frequency/predict_variant_pair_frequency_HardyWeinberg.py

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
* output_annovar{sample_id}.exonic_variant_function, output_annovar{sample_id}.variant_function and output_annovar{sample_id}.log files will be created for each sample.

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
* /global_pathway_analysis/significant_pathways_pathway_analysis_input.txt file will be created. This file contains only the pathways with p-value < 0.05.

## Predicting variant pair frequencies
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
* /statgen_utilities/predict_variant_pair_frequency/predicted_variant_pair_frequency_NOD2_chr16_clinvar_dbnsfp_gnomad_merged.tsv file will be created. This file contains the variant pair frequency for Non-Finish European (nfe) and African (afr) GNOMAD cohorts.

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
4. 


