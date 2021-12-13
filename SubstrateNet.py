#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 21:29:41 2021

@author: Flavio_Loess
@source_1: aAdjasso
@source: yhadjadj
"""

import json
import networkx as nx
import numpy as np
from Tools import Tools
import Controleur as control

class SubstrateNetwork:
    
    def __init__(self, path='Topo/BtEurope.gml'):
        self.SN_G = Tools.LoadGML(path)
        self.SN_G = self.SN_G.to_directed()
        self.BW, self.CPU, self.RAM, self.ROM = self.config_loader()
        self.Add_Paramters()
        self.Contoleur = control.Controleur(self.SN_G)
      
    @staticmethod
    def config_loader(config_filename = "config.json"):
        with open(config_filename) as json_data_file:
            data = json.load(json_data_file)
            BW = []
            BW.append(int(data["SubstrateNetwork"]["Link"]["Bandwidth"]["Min"]))
            BW.append(int(data["SubstrateNetwork"]["Link"]["Bandwidth"]["Max"]))
            CPU = []
            CPU.append(int(data["SubstrateNetwork"]["Node"]["CPU"]["Min"]))
            CPU.append(int(data["SubstrateNetwork"]["Node"]["CPU"]["Max"]))
            ROM = []
            ROM.append(int(data["SubstrateNetwork"]["Node"]["ROM"]["Min"]))
            ROM.append(int(data["SubstrateNetwork"]["Node"]["ROM"]["Max"]))
            RAM = []
            RAM.append(int(data["SubstrateNetwork"]["Node"]["RAM"]["Min"]))
            RAM.append(int(data["SubstrateNetwork"]["Node"]["RAM"]["Max"]))
        return BW, CPU, RAM, ROM

    
    def Add_Paramters(self):
        self.Add_LinkParameters()
        self.Add_NodeParameters()
        
    def Add_LinkParameters(self):
        for edge in self.SN_G.edges():
            node_src = edge[0]
            node_dst = edge[1]
            self.SN_G[node_src][node_dst]['Bandwidth'] = np.random.randint(self.BW[0],high=self.BW[1]+1,size=(1,1)).item()
            
    def Add_NodeParameters(self):
        CPU_Vals = np.random.randint(self.CPU[0],high=self.CPU[1]+1,size=(1,len(self.SN_G.nodes())))
        RAM_Vals = np.random.randint(self.RAM[0],high=self.RAM[1]+1,size=(1,len(self.SN_G.nodes()))) 
        ROM_Vals = np.random.randint(self.ROM[0],high=self.ROM[1]+1,size=(1,len(self.SN_G.nodes())))
        structCPU = {}
        structRAM = {}
        structROM = {}
        idVNRPlaced ={} 
        for node in self.SN_G.nodes():
            structCPU[node] = CPU_Vals[0][node]
            structRAM[node] = RAM_Vals[0][node]
            structROM[node] = ROM_Vals[0][node]
            idVNRPlaced[node] = {}
        nx.set_node_attributes(self.SN_G,structCPU,'CPU')
        nx.set_node_attributes(self.SN_G,structRAM,'RAM')
        nx.set_node_attributes(self.SN_G,structROM,'ROM')
        nx.set_node_attributes(self.SN_G,idVNRPlaced,'idVNRPlaced') # dictionnary of id's vnr placed on the node

            
    # LES ACTIONS DU CONTROLLEUR : le corp est definit dans le controleur qui gere le reseau substrat
    def forcerAzero(self):
        self.Contoleur.forcerAzero()
        
    def GetSolutionDePlacement(self, VNR):
        return self.Contoleur.GetSolutionDePlacement(VNR)
    
    def PlacerSolution(self, Solution):
        self.Contoleur.PlacerSolution(Solution)
                 
    def RetirerSolution(self, Solution):
        self.Contoleur.RetirerSolution(Solution)
        
    def FirstFit_placement(self,VNRs):
        return self.Contoleur.FirstFit_placement(VNRs)
    
    def removeVNR(self,idVNRPlaced):
        self.Contoleur.removeVNR(idVNRPlaced)
    
