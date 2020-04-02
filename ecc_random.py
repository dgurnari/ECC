#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import random
import gudhi as gd

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

def compute_local_contributions(points, epsilon):
    local_contributions = []

    for i in range(len(points)):
        neigh_of_i = find_neighbours(points, i, epsilon)

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
            local_contributions.append((contribution, filtration)) # list of tuples (simplex dimension, filtration)

    return sorted(local_contributions, key = lambda x: x[1])




if __name__ == "__main__":
    if len(argv) < 4:
        raise ValueError('please specify DIMENSION, N_POINTS and EPSILON')
    DIMENSION = int(argv[1])
    N_POINTS = int(argv[2])
    EPSILON = float(argv[3])

    point_cloud = np.random.rand(N_POINTS,DIMENSION)

    # ECC
    print("Local Simplex")
    print("DIMENSION {}, N_POINTS {}, EPSILON {}".format(DIMENSION, N_POINTS, EPSILON))
    start = datetime.now()
    lc_list = compute_local_contributions(point_cloud, EPSILON)
    print("\t time:", datetime.now() - start)

    print("\nsaving to local_contributions.npy")
    np.save('local_contributions.npy', lc_list)
    print("saved")
