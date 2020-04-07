#!/usr/bin/env python
# coding: utf-8

# In[50]:


import numpy as np
from matplotlib import pyplot as plt
import gudhi as gd
import random
import networkx as nx

import itertools


# In[51]:


# given a numpy array of poins, and index i and a threshold 
# finds the neighbours of the point [i] 

def find_neighbours(points, i, threshold):  
    v = points[i]
    
    return [point for point in points if np.linalg.norm(v - point) <= threshold]
        


# In[52]:


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
            
    


# In[53]:


def create_graph(points, epsilon):
    
    elist = find_all_edges(points, epsilon) 
    G=nx.Graph()
    G.add_weighted_edges_from(elist)
    
    return G


# In[5]:


# def create_local_graph(G, edge):
#     local_G = nx.Graph()
#     elist = []
    
#     threshold = G.edges[edge]["weight"]
    
#     for edge in G.edges(nbunch=edge, data=True):
#         print("analizzo", edge)
#         if edge[2]["weight"] <= threshold:
#             elist.append([edge[0], edge[1], edge[2]["weight"]])
            
#     local_G.add_weighted_edges_from(elist)
    
#     return local_G


# In[ ]:


# def create_local_graph(G, edge):
#     local_G = nx.Graph()
#     elist = []
    
#     threshold = G.edges[edge]["weight"]
    
#     for edge in G.edges(nbunch=edge, data=True):
#         print("analizzo", edge)
#         if edge[2]["weight"] <= threshold:
#             elist.append([edge[0], edge[1], edge[2]["weight"]])
            
#     local_G.add_weighted_edges_from(elist)
    
#     return local_G


# In[6]:


# def count_edge_contributions(G, edge):
    
#     print("\n considering ", edge)
    
#     local_G = create_local_graph(G, edge)
#     filtration = G.edges[edge]["weight"]
    
#     contribution = 0
    
#     for clique in nx.enumerate_all_cliques(local_G):
#         print("\t", clique)
#         f = 0
#         for clique_edge in itertools.combinations(clique, 2):
#             print(clique_edge)
#             d = local_G.edges[clique_edge]['weight']
#             if d>f:
#                 f = d
#         if f == filtration:
#             print("\t", clique, " contributes")
#             contribution += (-1)**(len(clique)-1)
            
#     return [filtration, contribution]


# In[7]:


# def compute_local_contributions(point_cloud, epsilon):
#     G = create_graph(point_cloud, epsilon)
    
#     contributions_list = []
    
#     contributions_list.append( [0, len(point_cloud)] )
    
#     for edge in G.edges:
#         contributions_list.append(count_edge_contributions(G, edge))
        
#     return sorted(contributions_list, key = lambda t: t[0])
        


# In[42]:


def compute_local_contributions_gd(point_cloud, epsilon):
    G = create_graph(point_cloud, epsilon)
    
    contributions_list = []
    
    contributions_list.append( [0, len(point_cloud)] )
    
    for edge in G.edges:
        edge_lenght = G.edges[edge]["weight"]
        local_points = [point_cloud[edge[0]], point_cloud[edge[1]]] # we start with only the edge nodes
        
        neigh_0 = set()
        for n in nx.neighbors(G, edge[0]):
            if G.edges[(edge[0], n)]["weight"] <= edge_lenght:
                neigh_0.add(n)
        
        neigh_1 = set()
        for n in nx.neighbors(G, edge[1]):
            if G.edges[(edge[1], n)]["weight"] <= edge_lenght:
                neigh_1.add(n)
                
        for point_idx in neigh_0 & neigh_1:
            local_points.append(point_cloud[point_idx])
        
        
        local_rips_complex = gd.RipsComplex(points=local_points, max_edge_length=edge_lenght)
        simplex_tree = local_rips_complex.create_simplex_tree(max_dimension=len(local_points)-1)
        
        
        contribution = 0
        
        for simplex, filtration in simplex_tree.get_filtration():
            if filtration == edge_lenght:
                contribution += (-1)**(len(simplex)-1)
                
        contributions_list.append([filtration , contribution])
        
        
    return sorted(contributions_list, key = lambda t: t[0])


# In[43]:


def euler_characteristic_list_from_edges(contributions):
    chi = 0
    
    chi_list = []
    
    for filtration, contribution in contributions:
        chi += contribution
        chi_list.append([filtration, chi])
        
    return np.array(chi_list)


# In[44]:


def plot_chi(e_list, with_lines = True):
    plt.figure()
    plt.scatter(e_list[:, 0], e_list[:, 1])
    
    
    if with_lines:
        
        for i in range(len(e_list) - 1):
            plt.vlines(x=e_list[i+1][0], ymin=min(e_list[i][1], e_list[i+1][1]),ymax=max(e_list[i][1], e_list[i+1][1]))

            plt.hlines(y=e_list[i][1], xmin=e_list[i][0], xmax=e_list[i+1][0])
    
    plt.show()

