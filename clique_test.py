import numpy as np
import networkx as nx

import random
from memory_profiler import profile



def find_all_edges(points, threshold):
    elist = []

    for i, vertex in enumerate(points[:-1]):
        for j, other_v in enumerate(points[i+1:]):
            distance = np.linalg.norm(vertex - other_v)
            if distance <= threshold:
                elist.append([i, j+i+1, distance])

    return elist

@profile
def ECC_prog(point_cloud, epsilon):
    
    ECC_list = []

    for i, vertex in enumerate(point_cloud):
        
        elist = find_all_edges(point_cloud[i:], epsilon)
        G=nx.Graph()

        G.add_nodes_from(list(range(len(point_cloud[i:]))))
        G.add_weighted_edges_from(elist)
        
        clique = [0] # only the first vertex (the one for wich we want the star)
        filtration = 0

        neighbors = [n for n in G.neighbors(0)] # neigh of the first vertex

        ECC_list.append( extend_clique(clique, neighbors, filtration, G, ECC_list) )

    
    return(sorted(ECC_list, key = lambda x: x[0]))  
    
    
        
def extend_clique(clique, neighbors, filtration, graph, ECC_list):
        
    while len(neighbors) > 0:
        to_add = neighbors.pop(0)
        #find new filtration
        new_filtration = filtration
        for v in clique:
            if graph.edges[v,to_add]['weight'] > new_filtration:
                new_filtration = graph.edges[v,to_add]['weight']
        
        ECC_list.append(extend_clique(clique+[to_add], 
                                      list( set(neighbors).intersection([n for n in graph.neighbors(to_add)]) ), 
                                      new_filtration,
                                      graph,
                                      ECC_list))
        
    return [filtration, (-1)**(len(clique)-1)]  




if __name__ == '__main__':
    point_cloud = []

    NUMBER_OF_POINTS = 100

    random.seed(42)
    for i in range(NUMBER_OF_POINTS):
        angle = random.uniform(0,2*np.pi)
        point_cloud.append([np.cos(angle), np.sin(angle)])
    
    point_cloud = np.array(point_cloud)
    
    epsilon = 1
    ECC_prog(point_cloud, epsilon)
    
