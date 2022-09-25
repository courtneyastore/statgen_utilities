# Statistical genetics and Bioinformatics resources
Utilities for analyzing genetic/genomic data.
## Variant annotation
### Requirements
* Python 3.7
* Perl 
* ANNOVAR: a tool for functional annotation of variants. Can be downloaded by filling out this form: https://www.openbioinformatics.org/annovar/annovar_download_form.php 

### Steps
1. Run conver2annovar.pl to create annovar-formatted files for variant annotation.
```sh
perl convert2annovar.pl -format vcf4 <multi-sample VCF> -allsample -outfile output_annovar
```
2. Create output directory.
 ```sh
  mkdir avinput_output
  ```
3. Move avinput files to avinput_output.
```sh
  mv *.avinput avinput_output/
```
4. Annotate variants for each sample.
```sh
  python3 annotate_pathogenic_variants_annovar.py -a <annovar directory> -v avinput_output
```

### Outputs
* output_annovar{sample_id}.exonic_variant_function, output_annovar{sample_id}.variant_function and output_annovar{sample_id}.log files will be created for each sample.

## Global pathway analysis
### Requirements
* 
## Predicting variant pair frequencies
### Requirements
* 
