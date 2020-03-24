#!/usr/bin/env python
# coding: utf-8

# In[12]:


import numpy as np
from matplotlib import pyplot as plt
import gudhi as gd
import random
import networkx as nx

import itertools


# In[13]:


# given a numpy array of poins, and index i and a threshold
# finds the neighbours of the point [i] that have index greater or equal to i

def find_neighbours_nx(points, i, threshold):
    v = points[i]

    neigh_list = []

    for j, p in enumerate(points[i:]):
        distance = np.linalg.norm(v - p)
        if distance <= threshold:
            neigh_list.append(p)

    return neigh_list



# In[14]:


# given a numpy array of poins, and index i and a threshold
# construct the local graph around the point i
# by finding all the edges shorther than the threshold value

def find_local_edges_nx(points, i, threshold):
    elist = []

    neigh = find_neighbours_nx(points, i, threshold)

    for i, vertex in enumerate(neigh[:-1]):
        for j, other_v in enumerate(neigh[i+1:]):
            distance = np.linalg.norm(vertex - other_v)
            if distance <= threshold:
                elist.append([i, j+i+1, distance])

    return elist




# In[15]:


def compute_local_contributions_nx(points, epsilon):
    local_contributions = []

    for i in range(len(points)):

        elist = find_local_edges_nx(points, i, epsilon)


        G=nx.Graph()
        G.add_node(0)
        G.add_weighted_edges_from(elist)

        for clique in nx.enumerate_all_cliques(G):
            if 0 in clique:
                f = 0
                for edge in itertools.combinations(clique, 2):
                    d = G.edges[edge]['weight']
                    if d>f:
                        f = d
                local_contributions.append([clique, f])


    return sorted(local_contributions, key = lambda x: x[1])
