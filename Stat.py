# -*- coding: utf-8 -*-
"""
Created on Tue May 25 19:54:40 2021

@author: Flavio_Loess
@source: aAdjasso
"""

import networkx as nx
import matplotlib.pyplot as plt
from copy import deepcopy

class Statistique:
    def __init__(self, G, param1 = "CPU", param2 = "ROM"):
        self.G_Init = deepcopy(G)
        couleurs_Nodes = ["Red", "OrangeRed", "GreenYellow", "Green"]
        couleurs_Edges = ["Red", "OrangeRed", "Magenta", "Blue"]
        taille_Nodes = [300, 500, 700, 900]
        self.tabValeursNodes = dict()
        self.tabValeursEdges = dict()
        self.tabTailleNodes = dict()
        for node in self.G_Init.nodes():
            tabValeurs = dict()
            q = int((self.G_Init.nodes[node][param1]+1)/4)
            tab = list(range((self.G_Init.nodes[node][param1]+1)))
            for i in range(3):
                values = []
                for _ in range(q):
                    values.append(tab.pop(0))
                tabValeurs[couleurs_Nodes[i]] = values
            tabValeurs[couleurs_Nodes[-1]] = tab
            self.tabValeursNodes[node] = tabValeurs
            
        for node in self.G_Init.nodes():
            tabValeurs = dict()
            q = int((self.G_Init.nodes[node][param2]+1)/4)
            tab = list(range((self.G_Init.nodes[node][param2]+1)))
            for i in range(3):
                values = []
                for _ in range(q):
                    values.append(tab.pop(0))
                tabValeurs[taille_Nodes[i]] = values
            tabValeurs[taille_Nodes[-1]] = tab
            self.tabTailleNodes[node] = tabValeurs
            
        count = -1
        for edge in self.G_Init.edges():
            count += 1
            tabValeurs = dict()
            q = int((self.G_Init[edge[0]][edge[1]]["Bandwidth"]+1)/4)
            tab = list(range((self.G_Init[edge[0]][edge[1]]["Bandwidth"]+1)))
            for i in range(3):
                values = []
                for _ in range(q):
                    values.append(tab.pop(0))
                tabValeurs[couleurs_Edges[i]] = values
            tabValeurs[couleurs_Edges[-1]] = tab
            self.tabValeursEdges[count] = tabValeurs
            
    def AfficherGraphe(self, G, param1, param2):
        nodes = []
        edges = []
        tailles = []
        for node in range(len(self.G_Init.nodes())):
            for values in self.tabValeursNodes[node].values():
                if G.nodes[node][param1] in values:
                    for key in self.tabValeursNodes[node].keys():
                        if self.tabValeursNodes[node][key] == values:
                            nodes.append(key)
                            break
                    break
            for values in self.tabTailleNodes[node].values():
                if G.nodes[node][param2] in values:
                    for key in self.tabTailleNodes[node].keys():
                        if self.tabTailleNodes[node][key] == values:
                            tailles.append(key)
                            break
                    break

        count = -1
        for edge in G.edges():
            count += 1
            for values in self.tabValeursEdges[count].values():
                if G[edge[0]][edge[1]]["Bandwidth"] in values:
                    for key in self.tabValeursEdges[count].keys():
                        if self.tabValeursEdges[count][key] == values:
                            edges.append(key)
                            break
                    break

        options = {
            'cmap'       : plt.get_cmap('viridis'),
            'node_color' : nodes,
            'node_size'  : tailles,
            'edge_color' : edges,
            'with_labels': True,
            }
        nx.draw(G,**options)
        plt.show()