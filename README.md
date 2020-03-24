# ECC

three different way to compute euler characteristic curves + function to plot them.

- ecc.py computes the local contributions by calculating the star of every vertex [requires gudhi];

- ecc_nx does the same but constructs only the 1-skeleton graph of the local VR simplex and computes the local contributions using the cliques counting algorithmn from networkx;

- cliques_counting.py brute force clique counting of the whole graph;

- ecc_plot.py plots

some comparison can be found in tests.ipynb
