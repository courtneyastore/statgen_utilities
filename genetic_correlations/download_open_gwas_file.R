library(data.table)
install.packages("remotes")
remotes::install_github("MRCIEU/TwoSampleMR")
library(TwoSampleMR)


ao <- available_outcomes()

write.table(ao,file="open_gwas_file.tsv",row.names=FALSE,sep="\t")
