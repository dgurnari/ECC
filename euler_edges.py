#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
from matplotlib import pyplot as plt
import gudhi as gd
import random
import networkx as nx

import itertools


# In[2]:


# given a numpy array of poins, and index i and a threshold 
# finds the neighbours of the point [i] 

def find_neighbours(points, i, threshold):  
    v = points[i]
    
    return [point for point in points if np.linalg.norm(v - point) <= threshold]
        


# In[3]:


# given a numpy array of poins
# finds all the edges shorther than the threshold value

def find_all_edges(points, threshold):
    elist = []

    for i, vertex in enumerate(points[:-1]):
        for j, other_v in enumerate(points[i+1:]):
            distance = np.linalg.norm(vertex - other_v)
            if distance <= threshold:
                elist.append([i, j+i+1, distance])
                
    return elist
            
    


# In[69]:


def create_graph(points, epsilon):
    
    elist = find_all_edges(points, epsilon) 
    G=nx.Graph()
    G.add_nodes_from(range(len(points)))
    G.add_weighted_edges_from(elist)
    
    return G


# In[111]:


def compute_local_contributions_gd(point_cloud, epsilon):
    G = create_graph(point_cloud, epsilon)
    
    contributions_list = []
    
    contributions_list.append( [0, len(point_cloud)] )
    
    for edge in G.edges: #edge is a tuple
        
        edge_lenght = G.edges[edge]["weight"]
        #print("analizzo: ", edge, edge_lenght)
        
        #consider the first vertex
        neigh_0 = set(nx.neighbors(G, edge[0]))
        
        #consider the second
        neigh_1 = set(nx.neighbors(G, edge[1]))
                
        # common neighbours + the two vertices
        local_points = (neigh_0 & neigh_1) | set(edge)
        #print("\t creo grafo con: ", local_points)
        
        # creates a local graph 
        local_G = G.subgraph(local_points).copy()
        
        # remove edges longer than edge_lenght
        to_be_removed = []
        for local_edge in local_G.edges:
            if local_G.edges[local_edge]["weight"] > edge_lenght:
                to_be_removed.append(local_edge)
        #print("\t ",local_G.edges)
        local_G.remove_edges_from(to_be_removed)
        #print("\t rimuovo:", to_be_removed)
        #print("\t ",local_G.edges)

        contribution = 0
        
        for clique in nx.enumerate_all_cliques(local_G):
            if (edge[0] in clique) and (edge[1] in clique):
                #print("\t clique", clique)
                contribution += (-1)**(len(clique)-1)
        
        #print("\t" , contribution)
                
        contributions_list.append([edge_lenght , contribution])
        
        
    return sorted(contributions_list, key = lambda t: t[0])


# In[112]:


def euler_characteristic_list_from_edges(contributions):
    chi = 0
    
    chi_list = []
    
    for filtration, contribution in contributions:
        chi += contribution
        chi_list.append([filtration, chi])
        
    return np.array(chi_list)


# In[113]:


def plot_chi(e_list, with_lines = True):
    plt.figure()
    plt.scatter(e_list[:, 0], e_list[:, 1])
    
    
    if with_lines:
        
        for i in range(len(e_list) - 1):
            plt.vlines(x=e_list[i+1][0], ymin=min(e_list[i][1], e_list[i+1][1]),ymax=max(e_list[i][1], e_list[i+1][1]))

            plt.hlines(y=e_list[i][1], xmin=e_list[i][0], xmax=e_list[i+1][0])
    
    plt.show()


# In[ ]:




