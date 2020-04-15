#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import random
import gudhi as gd

import networkx as nx

from datetime import datetime
from sys import argv


# # The algorithm

# given a numpy array of poins, and index i and a threshold
# finds the neighbours of the point [i] that have index greater or equal to i

def find_neighbours(points, i, threshold):
    v = points[i]

    return [point for point in points[i:] if np.linalg.norm(v - point) <= threshold]



# given a numpy array of points and a threshold epsilon
# for each point [i] in the list constructs its local complex (a Rips complex by default) with the point's neighbours
# and computes the local contribution to the Euler characteristic by taking the star of the point [i]
# returns the sorted list of all the local contributions

def compute_local_contributions(points, points_extended, epsilon):

    # separate the points and index
    points_no_idx = points[:,1:]
    p_index = list(points[:,0])

    points_ext_no_idx = points_extended[:,1:]
    p_ext_index = list(points_extended[:,0])


    local_contributions = {} # dict {filtration: contribution}


    # cicle over points in the considered ball
    # for each of them consider its neighbors in the same ball and the adjacents ones
    for idx in p_index:
        # trovo indice di idx
        i = p_ext_index.index(idx)

        neigh_of_i = find_neighbours(points_ext_no_idx, i, epsilon)

        local_rips_complex = gd.RipsComplex(points=neigh_of_i, max_edge_length=epsilon)
        simplex_tree = local_rips_complex.create_simplex_tree(max_dimension=len(neigh_of_i)-1)

        star = simplex_tree.get_star([0]) # the first element of the simplex tree is the point [i]
                                          # return list of tuples (simplex, filtration)

        # if the simplex is made by only one vertex, get_star returns the empty list,
        # we need to manually add the single vertex contribution
        if not star:
            star = [([0], 0.0)]

        for simplex, filtration in star:
            contribution = (-1)**(len(simplex)-1) # len(simplex) - 1 = dimension of the simplex
            # store the contribution at the right filtration value
            local_contributions[filtration] = local_contributions.get(filtration, 0) + contribution


    # convert the dict into a list, sort it according to the filtration and return it
    return sorted(list(local_contributions.items()), key = lambda x: x[0])




if __name__ == "__main__":
    if len(argv) < 2:
        raise ValueError('please specify FILE PATH and EPSILON')
    FILE_PATH = argv[1] #.../../IDX.csv
    IDX = FILE_PATH.split("/")[-1].split(".")[0]
    DIR_PATH = FILE_PATH.split("{}.csv".format(IDX))[0]

    EPSILON = float(argv[2])

    # load graph
    e_net = nx.read_gml("e_net.gml")

    idx_list = [IDX] # list of neighbors of IDX, strings
    idx_list.extend(nx.neighbors(e_net, IDX))

    # load the points
    POINT_CLOUD = np.loadtxt("{}".format(FILE_PATH), delimiter=",", ndmin=2)
    print("{} points in ball {} loaded".format(len(POINT_CLOUD), IDX))

    # load the neighbors
    POINT_CLOUD_EXTENDED = np.copy(POINT_CLOUD)
    print("\t neighbors are {}".format(list(nx.neighbors(e_net, IDX))))
    for n_idx in nx.neighbors(e_net, IDX):
        nth_ball = np.loadtxt("{}{}.csv".format(DIR_PATH, n_idx), delimiter=",", ndmin=2)
        POINT_CLOUD_EXTENDED = np.concatenate( (POINT_CLOUD_EXTENDED, nth_ball) )
        print("\t {} points from neigh ball {} loaded".format(len(nth_ball), n_idx))

    # sort them according to the first colum (index)
    ind = np.argsort( POINT_CLOUD[:,0] )
    POINT_CLOUD = POINT_CLOUD[ind]

    ind_n = np.argsort( POINT_CLOUD_EXTENDED[:,0] )
    POINT_CLOUD_EXTENDED = POINT_CLOUD_EXTENDED[ind_n]

    # ECC
    print("Local Simplex with epsilon ", EPSILON)
    start = datetime.now()
    lc_list = compute_local_contributions(POINT_CLOUD, POINT_CLOUD_EXTENDED, EPSILON)
    print("\t time:", datetime.now() - start)

    print("\nsaving to local-contributions/lc_{}.csv".format(IDX))
    np.savetxt("local-contributions/lc_{}.csv".format(IDX), lc_list, delimiter = ",", fmt = ["%.18e", "%d"])
    print("saved\n")
