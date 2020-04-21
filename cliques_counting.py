#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
from matplotlib import pyplot as plt
import gudhi as gd
import random
import networkx as nx

import itertools


# In[9]:


# given a numpy array of poins, and index i and a threshold
# finds all the edges shorther than the threshold value

def find_all_edges(points, threshold):
    elist = []

    for i, vertex in enumerate(points[:-1]):
        for j, other_v in enumerate(points[i+1:]):
            distance = np.linalg.norm(vertex - other_v)
            if distance <= threshold:
                elist.append([i, j+i+1, distance])

    return elist




# In[10]:


def compute_all_contributions_nx(points, epsilon):
    
    local_contributions = {} # dict {filtration: contribution}
    simplex_counter = 0

    elist = find_all_edges(points, epsilon)

    G=nx.Graph()

    G.add_nodes_from(list(range(len(points))))
    G.add_weighted_edges_from(elist)

    for clique in nx.enumerate_all_cliques(G):
        filtration = 0
        # finds the longest edge in the clique
        for edge in itertools.combinations(clique, 2):
            d = G.edges[edge]['weight']
            if d>filtration:
                filtration = d
        contribution = (-1)**(len(clique)-1) # len(simplex) - 1 = dimension of the simplex
        # store the contribution at the right filtration value
        local_contributions[filtration] = local_contributions.get(filtration, 0) + contribution

        simplex_counter += 1

    # remove the contributions that are 0
    to_del = []
    for key in local_contributions:
        if local_contributions[key] == 0:
            to_del.append(key)

    for key in to_del:
        del local_contributions[key]

    # convert the dict into a list, sort it according to the filtration and return it
    return sorted(list(local_contributions.items()), key = lambda x: x[0]), simplex_counter
