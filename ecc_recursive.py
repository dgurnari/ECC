import numpy as np

# given a poincloud, return two dictionaries that rapresents it graph
# obtained by connectin points that are at distance less than the threshold

def create_dicts(points, threshold):
    edict = {} # dict of edges (i,j) where i < j in the ordering
    ndict = {} # dict of each vertex neighbours, each vertex contain only 
               #     its neighbours that came after it in the ordering

    for i, vertex in enumerate(points):
        # initialize the ndict
        ndict[i] = []
    
    for i, vertex in enumerate(points[:-1]):
        for j, other_v in enumerate(points[i+1:]):
            distance = np.linalg.norm(vertex - other_v)
            if distance <= threshold:
                edict[(i, j+i+1)] = distance
                ndict[i] += [j+i+1]
                
    return edict, ndict


def compute_local_contributions(point_cloud, epsilon):
    # for each point, create its local graph and find all the
    #     cliques that belong to the star of the point
    
    ECC_list = []

    for i, vertex in enumerate(point_cloud):
        edict, ndict = create_dicts(point_cloud[i:], epsilon) 
        
        ECC_list.append( extend_clique(clique=[0], # only the first vertex (the one for wich we want the star)
                                       neighbors=ndict[0], # neigh of the first vertex
                                       filtration=0, 
                                       edict=edict,
                                       ndict=ndict,
                                       # remember, list are passed by reference!
                                       contributions_list=ECC_list) )

    
    return(sorted(ECC_list, key = lambda x: x[0]))   


def extend_clique(clique, neighbors, filtration, edict, ndict, contributions_list):
        
    while len(neighbors) > 0:
        # removes the first common neighbour and add it to the clique
        to_add = neighbors.pop(0)
        
        contributions_list.append(extend_clique(clique + [to_add], 
                                                sorted(set(neighbors).intersection(set(ndict[to_add]))),
                                                max([edict[(v,to_add)] for v in clique]+[filtration]) ,
                                                edict,
                                                ndict,
                                                contributions_list) )
        
    return [filtration, (-1)**(len(clique)-1)]