#!/bin/bash --login

# create the ball mapper graph and files in balls/
# requires as input the points.csv path $1 and the filtration $2

###
# job name
#SBATCH --job-name=ball_mapper
# job stdout file
#SBATCH --output=log/ball_mapper.out.%J
# job stderr file
#SBATCH --error=log/ball_mapper.err.%J
# maximum job time in D-HH:MM
#SBATCH --time=0:00:10
# maximum memory in  megabytes
#SBATCH --mem-per-cpu=1000
# run a single task, using a single CPU core
#SBATCH --ntasks=1
###

module load anaconda/2019.03
source activate
conda activate ecc_test


rm -fr balls/*
rm -fr local-contributions/*

python code/ball_mapper.py "$1" "$2"
