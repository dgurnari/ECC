#!/bin/bash --login

# run all the pipeline
# requires as input the points.csv path $1 and the filtration $2


###
# job name
#SBATCH --job-name=run_all_sequential
# job stdout file
#SBATCH --output=logs/ecc_sequential.out.%J
# job stderr file
#SBATCH --error=logs/ecc_sequential.err.%J
# maximum job time in D-HH:MM
#SBATCH --time=0-01:00
# maximum memory in  megabytes
#SBATCH --mem-per-cpu=2000
# run a single task, using a single CPU core
#SBATCH --ntasks=1
###

module load anaconda/2019.03
source activate
conda activate ecc_test


rm -fr balls/*
rm -fr local-contributions/*

python code/ball_mapper.py "$1" "$2"


time for datafile in balls/*
do
    echo $datafile
    python code/single_ball_contribution.py "$datafile" "$2"
done

python code/sort_contributions.py local-contributions/*
python code/ecc_plot.py results/contributions.csv 1 1
