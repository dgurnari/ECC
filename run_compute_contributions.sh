# Calculate ecc contributions for ball files.
# requires the value of the max filtration
for datafile in balls/*
do
    echo $datafile
    python single_ball_contribution.py "$datafile" "$1"
done
