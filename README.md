# ECC

two different ways to compute euler characteristic curves of filtered VR simplices + function to plot them.

- ecc_gudhi.py computes the local contributions by calculating the star of every vertex [requires gudhi];

- euler_recursive.py computes the contributions by recursively building up all the cliques in the 1-skeleton graph. It does so via a depth first search on one spanning tree of the VR simplex Hasse diagram [pure python].

- ecc_plot.py contains the functions to plot the ECC.

some comparison and tests can be found in tests.ipynb
