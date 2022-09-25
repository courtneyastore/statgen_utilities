# Statistical genetics and Bioinformatics resources
This repository contains various utilities for analyzing genetic/genomic data. Each utility is a component of larger pipelines.
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
3. Run Reactome Global Pathway Analysis via Reactome content and analysis services API using your input set of proteins.
```sh
  python3 global_pathway_analysis.py -f pathway_analysis_input.txt
```
## Outputs
* significant_pathways_pathway_analysis_input.txt file will be created. This file contains only the pathways with p-value < 0.05.

## Predicting variant pair frequencies
### Requirements
* 
