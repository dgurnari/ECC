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
    local_contributions = []

    elist = find_all_edges(points, epsilon)

    G=nx.Graph()

    G.add_weighted_edges_from(elist)

    for clique in nx.enumerate_all_cliques(G):
        f = 0
        # finds the longest edge in the clique
        for edge in itertools.combinations(clique, 2):
            d = G.edges[edge]['weight']
            if d>f:
                f = d
        local_contributions.append([clique, f])

    return sorted(local_contributions, key = lambda x: x[1])
