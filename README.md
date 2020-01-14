# Amazon Review Valitator
My data science project to guess if an amazon review is helpful for galvanize DSI. 
## Automoation Pipleline
### Planning and Reasoning
Amazon Customer Review dataset is on Amazon S3, but my $1000 AWS credit is not available yet. I decided to use my Azure VMs, which utlized around 20%.

I am going to deploy Spark docker containers to perform data analysis, may create a spark cluster in production stage.

### Data Migration AWS S3 Bucket -> Azure Blob Storage
Azure Documentations are outdated but its staff responded to my questions within a reasonable timeframe.

`
Azcopy ss
`
### Data Preparation
convert tsv to parquet in partitions because spark optimize performance with parquet files and the some of original tsv data files are more than 2GB, which can be partitioned and read by Spark in parallel.

## EDA
## Hypothesis
### In reviews with rating>4 and <2, people found reviews with words top 50 occurances are more helpful
 More frequently used words are more helpful or less frequently used words are more helpful?
 1)
 - [ ] H0: the helpfulness mean of most used 100 words > the helpfulness mean of the population
 - [x] H1: the helpfulness mean of most used 100 words < the helpfulness mean of the population
 2) 
- [x] H0: the helpfulness mean of least used 100 words > the helpfulness mean of the population
- [ ] H1: the helpfulness mean of least used 100 words < the helpfulness mean of the population
 
### How about ratings?
  Higher rating reviews or lower rating reviews are more helpful?
 1)
 H0: the helpfulness mean of Higher rating reviews > the helpfulness mean of the population
 H1: the helpfulness mean of Higher rating reviews < the helpfulness mean of the population
 
 2) 
 H0: the helpfulness mean of lower rating reviews > the helpfulness mean of the population
 H1: the helpfulness mean of lower rating reviews < the helpfulness mean of the population
 