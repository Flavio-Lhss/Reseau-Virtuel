#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 10:26:52 2021

@author: aAdjasso
@source: yhadjadj
"""
from itertools import count
import json
import networkx as nx
import numpy as np

# variable controlling the random generation
step = 1000
SimDuration = 20   # Simulation duration 

class VirtualNetworkRequest:
    _ids = count(0)
    ID_ = 0 
    
    def __init__(self, seed = 1):
        VirtualNetworkRequest.ID_ += 1
        global step
        self.id = next(self._ids)
        self.ID = VirtualNetworkRequest.ID_
        self.seed = seed + step + self.id
        self.BW, self.CPU, self.ROM, self.RAM, self.NumVNFs = self.config_loader()
        self.G_VNR = self.CreateVNR()
        self.G_VNR = self.G_VNR.to_directed()
        self.Add_Paramters()
        #params for simulateur
        """     self.env = env # reference le simulateur à évènements discret
        self.Orchestrator = orchestrator # Orchestrateur
        self.MST = mst
        self.Access = self.env.event() # Créer un évènement pour l'accès
        self.env = env # reference le simulateur à évènements discret
        print("Service {} created ({})".format(self.ID,self.env.now))"""
    
    def CreateVNR(self):
        nnodes = np.asscalar(np.random.randint(self.NumVNFs[0],high=self.NumVNFs[1]+1,size=(1,1)))
        p = 2 * np.log(nnodes)/nnodes
        VNR = nx.erdos_renyi_graph(nnodes,p, seed = self.seed)
        #VNR = nx.erdos_renyi_graph(nnodes,p)
        return VNR
    
    
    @staticmethod
    def config_loader(config_filename = "config.json"):
        with open(config_filename) as json_data_file:
            data = json.load(json_data_file)
            BW = []
            BW.append(int(data["VirtualNetwork"]["Link"]["Bandwidth"]["Min"]))
            BW.append(int(data["VirtualNetwork"]["Link"]["Bandwidth"]["Max"]))
            CPU = []
            CPU.append(int(data["VirtualNetwork"]["Node"]["CPU"]["Min"]))
            CPU.append(int(data["VirtualNetwork"]["Node"]["CPU"]["Max"]))
            ROM = []
            ROM.append(int(data["VirtualNetwork"]["Node"]["ROM"]["Min"]))
            ROM.append(int(data["VirtualNetwork"]["Node"]["ROM"]["Max"]))
            RAM = []
            RAM.append(int(data["VirtualNetwork"]["Node"]["RAM"]["Min"]))
            RAM.append(int(data["VirtualNetwork"]["Node"]["RAM"]["Max"]))
            NumVNFs = []
            NumVNFs.append(int(data["VirtualNetwork"]["NumVNFs"]["Min"]))
            NumVNFs.append(int(data["VirtualNetwork"]["NumVNFs"]["Max"]))
        return BW, CPU, ROM, RAM, NumVNFs
    
    
    def Add_Paramters(self):
        self.Add_LinkParameters()
        self.Add_NodeParameters()
        
    def Add_LinkParameters(self):
        for edge in self.G_VNR.edges():
            node_src = edge[0]
            node_dst = edge[1]
            self.G_VNR[node_src][node_dst]['Bandwidth'] = np.asscalar(np.random.randint(self.BW[0],high=self.BW[1]+1,size=(1,1)))
            
    def Add_NodeParameters(self):
        CPU_Vals = np.random.randint(self.CPU[0],high=self.CPU[1]+1,size=(1,len(self.G_VNR.nodes())))
        RAM_Vals = np.random.randint(self.RAM[0],high=self.RAM[1]+1,size=(1,len(self.G_VNR.nodes()))) 
        ROM_Vals = np.random.randint(self.ROM[0],high=self.ROM[1]+1,size=(1,len(self.G_VNR.nodes())))
        structCPU = {}
        structRAM = {}
        structROM = {}
        for node in self.G_VNR.nodes():
            structCPU[node] = CPU_Vals[0][node]
            structRAM[node] = RAM_Vals[0][node]
            structROM[node] = ROM_Vals[0][node]
        nx.set_node_attributes(self.G_VNR,structCPU,'CPU')
        nx.set_node_attributes(self.G_VNR,structRAM,'RAM')
        nx.set_node_attributes(self.G_VNR,structROM,'ROM')
    
    def getEdges(self):        
        return list(self.G_VNR.edges)

    def getEdgesDetails(self):
        edges = []
        bandwidthRq = []
        for e in self.G_VNR.edges:
            edges.append(e)
            bandwidthRq.append(self.G_VNR[e[0]][e[1]]['Bandwidth'])
        return edges, bandwidthRq
    