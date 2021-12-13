'''
Created on 23 nov. 2014

@author: yhadjadj
'''

import networkx as nx
import Tools.Calculations as calc
import Tools.Tools as tl

#import os
#import glob
#import sys


def EnrichWithDelay(G):
    
    nodes = G.nodes(True)
    
    for edge in G.edges():
        node_src = edge[0]
        lat1 = nodes[node_src].get('Latitude')
        if lat1 == None:
            lat1 = 0.0
        long1 = nodes[node_src].get('Longitude')
        if long1 == None:
            long1 = 0.0
        node_dst = edge[1]
        lat2 = nodes[node_dst].get('Latitude')
        if lat2 == None:
            lat2 = 0.0
        long2 = nodes[node_dst].get('Longitude')
        if long2 == None:
            long2 = 0.0
        delay = calc.getLinkDelay(lat1, long1, lat2, long2)
        if delay > 0.1:
            delay = 0.1
        G[node_src][node_dst]['delay'] = delay
    return G

if __name__ == "__main__":    
    G = tl.LoadGML('../Topo/BtEurope.gml')
    G = EnrichWithDelay(G)
    print(G.edges.data())
    #PlotGraph(G)
