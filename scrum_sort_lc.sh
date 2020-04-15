#!/bin/bash --login

# sorts the contributions in local-contributions/
# and creates a file in results/

###
# job name
#SBATCH --job-name=sort_lc
# job stdout file
#SBATCH --output=log/sort_lc.out.%J
# job stderr file
#SBATCH --error=log/sort_lc.err.%J
# maximum job time in D-HH:MM
#SBATCH --time=0:00:10
# maximum memory in  megabytes
#SBATCH --mem-per-cpu=1000
# run a single task, using a single CPU core
#SBATCH --ntasks=1
# set email alerts
###

module load anaconda/2019.03
source activate
conda activate ecc_test


python code/sort_contributions.py local-contributions/*
