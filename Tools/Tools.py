#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 19:26:01 2019

@author: Flavio_Loess
@source: yhadjadj
"""

import networkx as nx
import matplotlib.pyplot as plt
import Tools.GraphStructure as gs


def LoadGML(file):
    G = nx.read_gml(path=file,label='id')
    G = gs.EnrichWithDelay(G)
    return G

def PlotGraph(G):
    nx.draw(G)
    plt.show()

def PrintEdges(G):
    print(G.edges.data())
    
def PrintVertices(G):
    print(G.nodes())
    
def PrintAll(G):
    PrintVertices(G)
    PrintEdges(G)
    # PlotGraph(G)
    
def PrintInfoGraphe(G):
    print("Les nodes")
    for node in G.nodes():
        print(node, ' : CPU=', G.nodes[node]["CPU"], ' RAM=', G.nodes[node]["RAM"], ' ROM=', G.nodes[node]["ROM"])
    print('\n', "Les edges")
    for edge in G.edges():
        print(edge, ' : BW=', G[edge[0]][edge[1]]['Bandwidth'])
        
def PrintSolution(Solution):
    print("Les nodes")
    for node in Solution.nodes():
        print(node, ' => ', Solution.nodes[node]["NODE_EQ"])
    print('\n', "Les edges et chemins")
    for edge in Solution.edges():
        print(edge, ' => ', Solution[edge[0]][edge[1]]['PATH'])

def compare(G, g):
    for node in G.nodes():
        if G.nodes[node]["CPU"] != g.nodes[node]["CPU"]:
            return False
        elif G.nodes[node]["RAM"] != g.nodes[node]["RAM"]:
            return False
        elif  G.nodes[node]["ROM"] !=  g.nodes[node]["ROM"]:
            return False
    for edge in G.edges():
        if G[edge[0]][edge[1]]['Bandwidth'] != g[edge[0]][edge[1]]['Bandwidth']:
            return False
    return True

def Afficher(G):
    nodes = ["Grey"]*len(G.nodes())
    edges = ["Blue"]*len(G.edges())
    tailles = [500]*len(G.nodes())
    options = {
        'cmap'       : plt.get_cmap('viridis'),
        'node_color' : nodes,
        'node_size'  : tailles,
        'edge_color' : edges,
        'with_labels': True,
        }
    nx.draw(G,**options)
    plt.show()