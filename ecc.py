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
    local_contributions = {} # dict {filtration: contribution}

    simplex_counter = 0

    # cicle over points
    for idx, p in enumerate(points):

        neigh_of_p = find_neighbours(points, idx, epsilon)

        local_rips_complex = gd.RipsComplex(points=neigh_of_p, max_edge_length=epsilon)
        simplex_tree = local_rips_complex.create_simplex_tree(max_dimension=len(neigh_of_p)-1)

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


# In[4]:



###################################
# outdated function to create an alpha simplex
# add the folloqionf to compute_local_contributions

#         elif simplex_type == "alpha-new-f":
#             local_alpha_complex = gd.AlphaComplex(points=neigh_of_i)
#             # if epsilon is the max_edge_lenght, max_alpha = sqrt(epsilon/2)
#             simplex_tree = local_alpha_complex.create_simplex_tree(max_alpha_square=(epsilon/2)**2)



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
