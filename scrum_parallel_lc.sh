#!/bin/bash --login

###
# Number of processors we will use (40 will fill one nodes)
#SBATCH --ntasks 20
# Output file location
#SBATCH --output=logs/parallel_lc.out.%J
#SBATCH --error=logs/parallel_lc.err.%J
# Time limit for this job
# maximum job time in D-HH:MM
#SBATCH --time 00-01:00
###

# Ensure that parallel is available to us
module load parallel

# Define srun arguments:
srun="srun --nodes 1 --ntasks 1"
# --nodes 1 --ntasks 1         allocates a single core to each task

# Define parallel arguments:
parallel="parallel --max-procs $SLURM_NTASKS --joblog parallel_joblog"
# --max-procs $SLURM_NTASKS  is the number of concurrent tasks parallel runs, so number of CPUs allocated
# --joblog name     parallel's log file of tasks it has run

###
# calculates the local contribution in parallel
# requires the filtration in $1


module load anaconda/2019.03
source activate
conda activate ecc_test

# Run the tasks:
$parallel "$srun python code/single_ball_contribution.py {1} "$1" " ::: balls/*
