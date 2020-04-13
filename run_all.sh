# run all the pipeline
# requires as input the points.csv path $1 and the filtration $2
# and wether to plot lines $3

rm -fr balls/*
rm -fr local-contributions/*

python ball_mapper.py "$1" "$2"

for datafile in balls/*
do
    echo $datafile
    python single_ball_contribution.py "$datafile" "$2"
done

python sort_contributions.py local-contributions/*
python ecc_plot.py results/contributions.csv 1 "$3"
