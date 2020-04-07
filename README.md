# ECC

three different ways to compute euler characteristic curves + function to plot them.

- cliques_counting.py brute force clique counting of the whole graph [requires networkx];

- ecc.py computes the local contributions by calculating the star of every vertex [requires gudhi];

- euler_edges.py computes the contributions by looking at the edges instead of the verticies [requires both];

- ecc_plot.py plots

some comparison can be found in tests.ipynb
