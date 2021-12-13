# -*- coding: utf-8 -*-
"""
Created on Wed May 19 18:32:53 2021

@author: AKA CYRILLE
"""

import os
import csv
import matplotlib.pyplot as plt
import pandas
import networkx as nx 
from math import ceil


def ressourcesOccuped(node, ressource='CPU', mode='normal'): #ressource = CPU, RAM, ROM
    sumRessource=0
    for i in node['idVNRPlaced'].keys() :
        sumRessource+=node['idVNRPlaced'][i][ressource+'_rq']
    if mode == 'normal':
        return sumRessource
    elif mode =='%':
        return ceil((sumRessource/(sumRessource+node[ressource]))*100)

def colorNodes(G, listeDExecution, ressource='CPU', mode='%'):
    color_map = []
    dico_color = {'green':list(range(0,26)), 'yellow':list(range(26,51)), 'orange':list(range(51,76)), 'red':list(range(76,101))}
    for node in G.nodes():
        for keyColor in dico_color.keys():    
            if ressourcesOccuped(G.nodes[node],ressource,mode) in dico_color[keyColor]:
                color_map.append(keyColor)
    return color_map


def ployGraph(G, ressource='CPU'):
    print("Charge des noeuds : ", ressource)
    color_map = colorNodes(G, ressource, mode='%')
    nx.draw(G, node_color=color_map, with_labels=True)
    plt.show()
