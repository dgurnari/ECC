#!/usr/bin/env python
# coding: utf-8

# cliques counting using igraph


import numpy as np
from matplotlib import pyplot as plt

import igraph as ig

import itertools


# In[9]:


# given a numpy array of poins, and index i and a threshold
# finds all the edges shorther than the threshold value

def find_all_edges(points, threshold):
    elist = []
    wlist = []

    for i, vertex in enumerate(points[:-1]):
        for j, other_v in enumerate(points[i+1:]):
            distance = np.linalg.norm(vertex - other_v)
            if distance <= threshold:
                elist.append((i, j+i+1))
                wlist.append(distance)

    return elist, wlist




# In[10]:

def compute_all_contributions_ig(points, epsilon):
    
    local_contributions = {} # dict {filtration: contribution}
    simplex_counter = 0

    edges, weights = find_all_edges(points, epsilon)

    G = ig.Graph()
    G.add_vertices(len(points))
    G.add_edges(edges)
    G.es['weight'] = weights

    for clique in G.cliques():
        filtration = 0
        # finds the longest edge in the clique
        for edge in itertools.combinations(clique, 2):
            len_e = G[edge]
            if len_e > filtration:
                filtration = len_e
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

