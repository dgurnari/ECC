#!/bin/bash --login

# create the ball mapper graph and files in balls/
# requires as input the points.csv path $1 and the filtration $2

###
# job name
#SBATCH --job-name=create_grid
# job stdout file
#SBATCH --output=logs/create_grid.out.%J
# job stderr file
#SBATCH --error=logs/create_grid.err.%J
# maximum job time in D-HH:MM
#SBATCH --time=0-01:00
# maximum memory in  megabytes
#SBATCH --mem-per-cpu=100
# run a single task, using a single CPU core
#SBATCH --ntasks=1
###

module load anaconda/2019.03
source activate ecc_test

python code/create_grid.py "$1" "$2"
