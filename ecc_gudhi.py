import numpy as np
import gudhi as gd


# given a numpy array of poins, and index i and a threshold
# finds the neighbours of the point [i] that have index greater or equal to i

def find_neighbours(points, i, threshold):
    v = points[i]

    return [point for point in points[i:] if np.linalg.norm(v - point) <= threshold]


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