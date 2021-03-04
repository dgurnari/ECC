import numpy as np
import networkx as nx





def create_dicts(points, threshold):
    edict = {}
    ndict = {}

    for i, vertex in enumerate(points):
        ndict[i] = []
    
    for i, vertex in enumerate(points[:-1]):
        for j, other_v in enumerate(points[i+1:]):
            distance = np.linalg.norm(vertex - other_v)
            if distance <= threshold:
                edict[(i, j+i+1)] = distance
                ndict[i] += [j+i+1]
                
    return edict, ndict








def ECC_recursive(point_cloud, epsilon):
    
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


















def find_all_edges(points, threshold):
    elist = []

    for i, vertex in enumerate(points[:-1]):
        for j, other_v in enumerate(points[i+1:]):
            distance = np.linalg.norm(vertex - other_v)
            if distance <= threshold:
                elist.append([i, j+i+1, distance])

    return elist


def create_graph_from_pointcloud(points, epsilon):
    #create graph
    elist = find_all_edges(points, epsilon)
    G=nx.Graph()

    G.add_nodes_from(list(range(len(points))))
    G.add_weighted_edges_from(elist)
    
    return G


def ECC_recursive_NX(point_cloud, epsilon):
    
    ECC_list = []

    for i, vertex in enumerate(point_cloud):
        
        #create local graph
        G_i = create_graph_from_pointcloud(point_cloud[i:], epsilon)
        
        ECC_list.append( extend_clique_NX(clique={0}, # only the first vertex (the one for wich we want the star)
                                       neighbors=set([n for n in G_i.neighbors(0)]), # neigh of the first vertex
                                       filtration=0, 
                                       graph=G_i, 
                                       # remember, list are passed by reference!
                                       contributions_list=ECC_list) )

    
    return(sorted(ECC_list, key = lambda x: x[0]))   
    
    
        
def extend_clique_NX(clique, neighbors, filtration, graph, contributions_list):
        
    while len(neighbors) > 0:
        # removes the first common neighbour and add it to the clique
        to_add = neighbors.pop()
        
        # find new filtration by cheching the new edges
        new_filtration = filtration
        for v in clique:
            if graph.edges[v,to_add]['weight'] > new_filtration:
                new_filtration = graph.edges[v,to_add]['weight']
        
        contributions_list.append(extend_clique_NX(clique.union({to_add}), 
                                      neighbors.intersection([n for n in graph.neighbors(to_add)]), 
                                      new_filtration,
                                      graph,
                                      contributions_list) )
        
    return [filtration, (-1)**(len(clique)-1)]       