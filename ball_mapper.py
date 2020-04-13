#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
from matplotlib import pyplot as plt
import random
import networkx as nx

from datetime import datetime
from sys import argv


# In[2]:


def create_net_dict(points, epsilon):
    B_dict = {} # dict of dicts {key: {idx: point} }
                # the center is idx = key

    centers = [] # list of points [[idx, point], ... ]

    for idx, p in enumerate(points):
        is_covered = False

        for key in B_dict:
            center = B_dict[key][key]
            distance = np.linalg.norm(p - center)
            if distance <= epsilon:
                is_covered = True
                B_dict[key][idx] = p
                break

        if not is_covered:
            B_dict[idx] = {idx: p}
            centers.append([idx, p])

    return B_dict, centers


# In[3]:


def save_dict(b):
    for key in b:
        with open('balls/{}.csv'.format(key),'w') as f:
            for idx in b[key]:
                f.write(str(idx))
                for n in b[key][idx]:
                    f.write("," + str(n))
                f.write("\n")


# In[4]:


def find_edges(points, threshold): # points = list of points [[idx, point], ... ]
    elist = []

    for i, vertex in enumerate(points[:-1]):
        for other_v in points[i+1:]:
            distance = np.linalg.norm(vertex[1] - other_v[1])
            if distance <= threshold:
                elist.append([vertex[0], other_v[0], distance])

    return elist


# In[5]:


def create_graph(points, epsilon):
    # points = list of points [[idx, point], ... ]
    G=nx.Graph()
    G.add_nodes_from([idx for idx, p in points])

    elist = find_edges(points, epsilon)
    G.add_weighted_edges_from(elist)

    return G


# In[7]:


def save_graph(G, out_name):
    nx.write_gml(G, out_name)


# In[8]:


if __name__ == "__main__":
    if len(argv) < 3:
        raise ValueError('please specify the input csv file and the value of epsilon')
    POINTS_PATH = argv[1]
    EPSILON = float(argv[2])

    POINTS = np.loadtxt(POINTS_PATH, delimiter=',', ndmin=2)
    print("points loaded")

    B_dict, centers = create_net_dict(POINTS, EPSILON)
    print("cover vector created")
    save_dict(B_dict)
    print("cover vector saved in out/")


    e_net = create_graph(centers, 3*EPSILON) #note the 3*EPSILON !!!!
    print("e-net created")
    save_graph(e_net, "e_net.gml")
    print("e-net saved in e_net.gml")
