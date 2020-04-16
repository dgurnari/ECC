+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
++ run the setup.sh script to make sure you have all the required subdirectories ++
++ $ bash setup.sh                                                               ++
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
$ bash setup.sh

the pipeline is the following:
$ python ball_mapper.py [points.csv] [filtration]
- for each file in balls/ 
    $ python single_ball_contribution.py [filtration]
$ python run sort_contributions.py
$ python plot_ecc.py [contributions.cvs] [png 1/0] [lines 1/0]




to run the program on sunbird run the bash scripts instead of the code

$ sbatch scrum_ball_mapper.sh [points.csv] [filtration]
$ sbatch scrum_parallel_lc.sh [filtration] <<<-- this is the parallel part
$ sbatch scrum_sort_lc.sh
$ sbatch scrum_plot.sh


if you want to run all the pipeline in a sequential fashion
$ sbatch run_all_sequential.sh [points.csv] [filtration]
