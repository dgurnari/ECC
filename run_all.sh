# run all the pipeline
# requires as input the points.csv path $1, the filtration $2
# and wether to plot lines $3

python ecc_star_simplex.py "$1" "$2"
python ecc_plot.py results/contributions.csv 1 "$3"
