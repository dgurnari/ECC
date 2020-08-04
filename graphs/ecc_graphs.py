import numpy as np
from matplotlib import pyplot as plt
import random
import gudhi as gd
import itertools



def compute_local_contributions(simplex_tree, verbose = False):
    local_contributions = {} # dict {filtration: contribution}

    simplex_counter = 0
    
    vertices_list = [s[0][0] for s in simplex_tree.get_skeleton(0)]
    
    # cicle over points
    for idx in vertices_list:
        star = simplex_tree.get_star([idx]) # the first element of the simplex tree is the point [i]
                                          # return list of tuples (simplex, filtration)

        # if the simplex is made by only one vertex, get_star returns the empty list,
        # we need to manually add the single vertex contribution
        if not star:
            star = [([idx], simplex_tree.filtration([idx]))]

        for simplex, filtration in star:
            # we want only the vertices after the considered one!
            skip = False
            for v in simplex:
                if v < idx:
                    skip = True
                    break
            if skip:
                continue
                
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



def euler_characteristic_list(local_contributions):

    euler_characteristic = []

    current_characteristic = 0
    old_f = 0
    filtration = 0

    for filtration, contribution in local_contributions:
        if filtration > old_f:
            euler_characteristic.append([old_f, current_characteristic])
            old_f = filtration

        current_characteristic += contribution

    # add last contribution
    euler_characteristic.append([filtration, current_characteristic])

    return np.array(euler_characteristic)



# WARNING
# when plotting a lot of points, drawing the lines can take some time
def plot_euler_curve(e_list, with_lines=False, title = None):
    plt.figure()
    plt.scatter([f[0] for f in e_list], [f[1] for f in e_list])

    # draw horizontal and vertical lines b/w points
    if with_lines:
        for i in range(len(e_list)-1):
            plt.hlines(y=e_list[i][1], xmin=e_list[i][0], xmax=e_list[i+1][0])
            
            plt.vlines(x=e_list[i+1][0], ymin=min(e_list[i][1], e_list[i+1][1]),ymax=max(e_list[i][1], e_list[i+1][1]))

            

    plt.xlabel("filtration")
    plt.ylabel("euler characteristic")
    plt.title(title)