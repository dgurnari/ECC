#!/bin/bash --login

# plots the ECC


###
# job name
#SBATCH --job-name=plot_ecc
# job stdout file
#SBATCH --output=logs/plot_ecc.out.%J
# job stderr file
#SBATCH --error=logs/plot_ecc.err.%J
# maximum job time in D-HH:MM
#SBATCH --time=0-00:10
# maximum memory in  megabytes
#SBATCH --mem-per-cpu=1000
# run a single task, using a single CPU core
#SBATCH --ntasks=1
###

module load anaconda/2019.03
source activate
conda activate ecc_test

python code/plot_ecc.py results/contributions.csv 1 1