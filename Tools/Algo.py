# -*- coding: utf-8 -*-
"""
Created on Mon May  10 02:27:01 2021

@author: Flavio_Loess
"""

from copy import deepcopy
import networkx as nx

# Algorithme de Pierre Marshalll Flavioooooo
class Algo:
    
    def __init__(self):
        self.pile = []
        self.chemins = []
        self.path = []
        self.interdire = []
        
    def CheminsEntreNodes(self, depart, arrivee, G):
        if depart == arrivee:
            return None
        self.__init__()
        self.pile.append([depart])
        self.interdire.append(depart)
        self.getOptimumPath(depart, arrivee, G)
        if len(self.chemins) == 0:
            return None
        chemins_Edges = []
        for chemin in self.chemins:
            chemin_Edges = []
            for i in range(len(chemin)):
                if i > 0:
                    chemin_Edges.append((chemin[i-1],chemin[i]))
            chemins_Edges.append(chemin_Edges)
        return chemins_Edges
        
    def visiteP(self, x, Liste, G):
        Liste.append(x)
        for y in list(G.neighbors(x)):
            if y not in Liste:
                self.visiteP(y, Liste, G)
                
    def visiteL(self, x, Liste, G):
        Vu = []
        Vu.append(x)
        file = []
        file.insert(0, x)
        while not len(file) == 0:
            y = file.pop()
            Liste.append(y)
            for z in list(G.neighbors(y)):
                if z not in Vu:
                    Vu.append(z)
                    file.insert(0, z)
        
    def getOptimumPath(self, x, t, G):
        self.path = deepcopy(self.pile[-1])
        for y in list(G.neighbors(x)):
            if y not in self.path:
                self.path.append(y)
                if y == t:
                    self.chemins.append(self.path)
                    self.path = deepcopy(self.pile[-1])
                else:
                    self.pile.append(self.path)
                    self.getOptimumPath(y, t, G)
        if len(self.pile) > 1:
            self.pile.pop()
        self.path = deepcopy(self.pile[-1])
        
    def CheminsEntreNodesAvecOrdre(self, depart, arrivee, G):
        chemins = self.CheminsEntreNodes(depart, arrivee, G)
        if (chemins == None) or (len(chemins) <= 1):
            return chemins
        tampon = None
        yapermute = True
        while(yapermute):
            yapermute = False
            for i in range(len(chemins)-1):
                if len(chemins[i]) > len(chemins[i+1]):
                    tampon = chemins[i]
                    chemins[i] = chemins[i+1]
                    chemins[i+1] = tampon
                    yapermute = True
        return chemins
    

