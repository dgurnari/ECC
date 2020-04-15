#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
from matplotlib import pyplot as plt
import random
import gudhi as gd
import itertools

import tadasets


# # The algorithm

# In[2]:


# given a numpy array of poins, and index i and a threshold
# finds the neighbours of the point [i] that have index greater or equal to i

def find_neighbours(points, i, threshold):
    v = points[i]

    return [point for point in points[i:] if np.linalg.norm(v - point) <= threshold]



# In[3]:


# given a numpy array of points and a threshold epsilon
# for each point [i] in the list constructs its local complex (a Rips complex by default) with the point's neighbours
# and computes the local contribution to the Euler characteristic by taking the star of the point [i]
# returns the sorted list of all the local contributions

def compute_local_contributions(points, epsilon, simplex_type = "rips", verbose = False):
    local_contributions = []

    if verbose:
        print("computing local contributions, {} points".format(len(points)))

    for i in range(len(points)):
        if verbose:
            print("\t {}".format(i))
        neigh_of_i = find_neighbours(points, i, epsilon)

        if simplex_type == "alpha":
            local_alpha_complex = gd.AlphaComplex(points=neigh_of_i)
            # if epsilon is the max_edge_lenght, max_alpha = sqrt(epsilon/2)
            simplex_tree = local_alpha_complex.create_simplex_tree(max_alpha_square=(epsilon/2)**2)

        elif simplex_type == "alpha-new-f":
            local_alpha_complex = gd.AlphaComplex(points=neigh_of_i)
            # if epsilon is the max_edge_lenght, max_alpha = sqrt(epsilon/2)
            simplex_tree = local_alpha_complex.create_simplex_tree(max_alpha_square=(epsilon/2)**2)

            simplex_tree = new_filtration_for_alpha(local_alpha_complex, simplex_tree)

        elif simplex_type == "rips":
            local_rips_complex = gd.RipsComplex(points=neigh_of_i, max_edge_length=epsilon)
            simplex_tree = local_rips_complex.create_simplex_tree(max_dimension=len(neigh_of_i)-1)
        else:
            raise ValueError("simplex type {} not defined".format(simplex_type))


        star = simplex_tree.get_star([0]) #the first element of the simplex tree is the point [i]

        # if the simplex is made by only one vertex, get_star returns the empty list,
        # we need to manually add the single vertex contribution
        if not star:
            star = [([0], 0.0)]

        local_contributions.extend(star) # list of tuples (simplex, filtration)

    return sorted(local_contributions, key = lambda x: x[1])


# In[4]:


def new_filtration_for_alpha(a_complex, s_tree):
    for s in s_tree.get_filtration(): # s is a tuple (simplex, filtration)
        if len(s[0]) >= 2 :
            # check all the possible combinations
            max_d = 0

            for edge in itertools.combinations(s[0], 2):
                f = s_tree.filtration(edge)
                d = np.linalg.norm(np.array(a_complex.get_point(edge[0])) - np.array(a_complex.get_point(edge[1])))

                if d>max_d :
                    max_d = d

                #print("\t edge {} con f:{} e d:{}".format(edge, f, d))
            s_tree.assign_filtration(s[0], max_d)

    s_tree.initialize_filtration()

    return s_tree