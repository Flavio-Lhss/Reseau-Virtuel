#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 21:29:41 2021

@author: aAdjasso / Flavio_Loess
@source: yhadjadj
"""

import networkx as nx
import numpy as np
from Tools import Algo # C'est un module dans le quel se trouve certans algorithme qui intervienne dans la tache du controleur
from copy import deepcopy

class Controleur:
    
    def __init__(self, SN_G):
        self.SN_G = SN_G
        self.Attendre = 0
        
    def forcerAzero(self):
        self.Attendre = 0
    
    def CheckVNFPlacement_CPU(self,node, CPU_rq):
        return self.SN_G.nodes[node]["CPU"]>=CPU_rq
    
    def CheckVNFPlacement_RAM(self,node, RAM_rq):
        return self.SN_G.nodes[node]["RAM"]>=RAM_rq
    
    def CheckVNFPlacement_ROM(self,node, ROM_rq):
        return self.SN_G.nodes[node]["ROM"]>=ROM_rq
            
    def ListeAleatoire(self, level):
        Parcours = []
        for i in range(level):
            alea = np.random.randint(0,high=level, size=(1,1)).item()
            if alea not in Parcours:
                Parcours.append(alea)
        for i in range(level):
            if i not in Parcours:
                Parcours.append(i)
        return Parcours
    
    def PlacementEstPossibleSurCeNoeud(self, sn_node, CPU, RAM, ROM):
        if not self.CheckVNFPlacement_CPU(sn_node, CPU):
            return False
        elif not self.CheckVNFPlacement_RAM(sn_node, RAM):
            return False
        elif not self.CheckVNFPlacement_ROM(sn_node, ROM):
            return False
        return True
    
    # 1 :  Chercher une solution de placement d'un service pour le mode Evolutionary
    # 2 : La boucle de debut permet juste d'attendre si il y a un eventuel placement ou retrait du service, en gros
    # on attent que le controleur finissent la tache en cours afin quelle nous revienne. Si on fait pas ca, on pourrait ne pas avoir de la place tant dis que le controleur est entrain
    # de liberer des ressources quelque part.
    def GetSolutionDePlacement(self, VNR):
        while(True):
            if self.Attendre == 0:
                break
        self.Attendre += 1 # cest pour signifier que le controleur travaille et dès qu'on fini on va decrementer
        VN_G = VNR.G_VNR
        # Parcours est une liste aleatoire des noeuds du graphe substart
        # Cette liste permet de savoir par où devons nous attaquer le substart afin de chercher une solution.
        # Donc forcement il existe un meilleur moyen de l'attaquer.
        Parcours = self.ListeAleatoire(len(self.SN_G.nodes()))
        for debut in Parcours:
            SN_G_Copy = deepcopy(self.SN_G)
            Solution = deepcopy(VN_G) # Ici Solution a la meme striucture qu'un VNR et en plus de ca à chaque noeud on va faire correspondre un noeud du substart et à chaque lien on va faire correspondre le chemin utiliser sur le substart.
            SN_nodes = [] # Ce sont les nodes deja visiter
            # 
            Algorithme = Algo.Algo()
            # ici debut est le noeud par le quel on souhait attaquer le reseau.
            # Donc en commencant par debut, on souhaite parcourir le reseau par un parcours en largeur, donc cerrer une liste d'adjacence de bout en bout afin que le depot des noeuds du service soient les plus optimal(leur chemin est cours, par ce qu'ils sont de plus en plus adjacent)
            Algorithme.visiteP(debut, SN_nodes, self.SN_G) # cette liste est mis dans SN_Nodes
            structEqNode = {}
            ListeNodesSolution = []
            NodesPlacer = True
            for node in VN_G.nodes(): # pour tous les npoeuds du VNR
                NodesPlacer = False
                for sn_node in SN_nodes: # on cherche ou placer les noeuds en parcours le graphe de maniere adjacent de bout en bout
                    if sn_node in ListeNodesSolution:
                        continue
                    if self.PlacementEstPossibleSurCeNoeud(sn_node,VN_G.nodes[node]["CPU"],VN_G.nodes[node]["RAM"],VN_G.nodes[node]["ROM"]):
                        structEqNode[node] = sn_node # on enregistre le noeud equivalent
                        ListeNodesSolution.append(sn_node)
                        NodesPlacer = True
                        break
                if not NodesPlacer:
                    break
            
            # On va vers les liens
            if NodesPlacer:
                nx.set_node_attributes(Solution,structEqNode,'NODE_EQ') # on enregistre dans solution les noeuds du substrat sur lesquel on souhait placer
                EdgesPlacer = True
                for edge in VN_G.edges():
                    EdgesPlacer = False
                    nodeEqSrc = Solution.nodes[edge[0]]["NODE_EQ"]
                    nodeEqDst = Solution.nodes[edge[1]]["NODE_EQ"]
                    Algorithme = Algo.Algo()
                    # listeChemins contient tous les chemins possibles entre deux noeud du substrat
                    # En fait on ne va pas se contenter de vouloir placer uniquement sur le plus cours chemin en matiere de distance, 
                    # Mets plutot chercher un autre chemin par lequel on peut acheminer les paquets entre deux noeuds.
                    listeChemins = Algorithme.CheminsEntreNodesAvecOrdre(nodeEqSrc, nodeEqDst, SN_G_Copy)
                    if listeChemins == None:
                        break
                    for chemin in listeChemins:
                        chemin_BW = []
                        for lien in chemin:
                            chemin_BW.append(SN_G_Copy[lien[0]][lien[1]]['Bandwidth'])
                        chemin_BW.sort()
                        BW_Min = chemin_BW[0]
                        if VN_G[edge[0]][edge[1]]['Bandwidth'] > BW_Min:
                            continue
                        for lien in chemin:
                            SN_G_Copy[lien[0]][lien[1]]['Bandwidth'] -= VN_G[edge[0]][edge[1]]['Bandwidth']
                        Solution[edge[0]][edge[1]]['PATH'] = chemin
                        Solution[edge[0]][edge[1]]['LINK_EQ'] = (nodeEqSrc,nodeEqDst)
                        EdgesPlacer = True
                        break
                    if not EdgesPlacer:
                        break
                if EdgesPlacer:
                    self.Attendre -= 1
                    return Solution
        
        self.Attendre -= 1
        return None
        
    def PlacerSolution(self, Solution):
        self.Attendre += 1
        for node in Solution.nodes():
            node_eq = Solution.nodes[node]["NODE_EQ"]
            self.SN_G.nodes[node_eq]["CPU"] -= Solution.nodes[node]["CPU"]
            self.SN_G.nodes[node_eq]["RAM"] -= Solution.nodes[node]["RAM"]
            self.SN_G.nodes[node_eq]["ROM"] -= Solution.nodes[node]["ROM"]
        for edge in Solution.edges():
            chemin = Solution[edge[0]][edge[1]]['PATH']
            for lien in chemin:
                 self.SN_G[lien[0]][lien[1]]['Bandwidth'] -= Solution[edge[0]][edge[1]]['Bandwidth']
        self.Attendre -= 1
                 
    def RetirerSolution(self, Solution):
        self.Attendre += 1
        for node in Solution.nodes():
            node_eq = Solution.nodes[node]["NODE_EQ"]
            self.SN_G.nodes[node_eq]["CPU"] += Solution.nodes[node]["CPU"]
            self.SN_G.nodes[node_eq]["RAM"] += Solution.nodes[node]["RAM"]
            self.SN_G.nodes[node_eq]["ROM"] += Solution.nodes[node]["ROM"]
        for edge in Solution.edges():
            chemin = Solution[edge[0]][edge[1]]['PATH']
            for lien in chemin:
                 self.SN_G[lien[0]][lien[1]]['Bandwidth'] += Solution[edge[0]][edge[1]]['Bandwidth']
        self.Attendre -= 1

    def CheckVLsPlacement(self, edges, BW_rq, Solution, reserve = False):
        G = deepcopy(self.SN_G)
        p = nx.shortest_path(G)
        VLsplaced = 0
        
        for i in range(len(edges)):
            s = edges[i][0]
            d = edges[i][1]
            sp = p[s][d]
            chemin = []
            for j in range(len(sp)-1):
                if not G[sp[j]][sp[j+1]]['Bandwidth'] >=  BW_rq[i]:
                    # not enough resources
                    return False, VLsplaced, self.SN_G
                else:
                    # remove requested resource
                    edge = (sp[j], sp[j+1])
                    chemin.append(edge)
                    G[sp[j]][sp[j+1]]['Bandwidth'] = G[sp[j]][sp[j+1]]['Bandwidth'] - BW_rq[i]
            VLsplaced = VLsplaced + 1
            for edge in Solution.edges():
                if Solution[edge[0]][edge[1]]['LINK_EQ'] == (s,d):
                    Solution[edge[0]][edge[1]]['PATH'] = chemin
                    break
                    
        # arriving here means enough resources for VLs
        if not reserve:
            return True, VLsplaced, self.SN_G
            #return self.SN_G
        #self.SN_G.clear()
        #self.SN_G = deepcopy(G)
        #self.checkEdgesChgt(self.SN_G.edges,self.SN_G,G)
        return True, VLsplaced, G
        #return G

    def MappingVLstoLinks(self, VNFPlacement, VRedges, Solution):
        mapVR = []
        for e in VRedges:
            
            ne = (VNFPlacement[e[0]]['id'],VNFPlacement[e[1]]['id'])
            Solution[e[0]][e[1]]['LINK_EQ'] = ne
            #print(e,ne)
            mapVR.append(ne)
        return mapVR

    ###☺ FIRSTFIT Placement
    def FirstFit_placement(self,VNRs):
        while(True):
            if self.Attendre == 0:
                break
        self.Attendre += 1
        Solution = deepcopy(VNRs.G_VNR)
        structEqNode = {}
        nodes = list(self.SN_G.nodes())
        nodes_prop = {}
        dico_res = {} # dictionnary of ressources
        for node in nodes:
             dico_res["CPU"] = self.SN_G.nodes[node]["CPU"]
             dico_res["RAM"] = self.SN_G.nodes[node]["RAM"]
             dico_res["ROM"] = self.SN_G.nodes[node]["ROM"]
             nodes_prop[node] = dico_res.copy()
             #print(nodes_prop)
        #print dico of ressources
        #print('dico of ressources :',nodes_prop)
        # VNFs placement checking
        VNFs_Placement = {}
        
        
        VNRs_failure = 0
        PlacementSol = {}
        # VNF i placement
        lnp = nodes_prop.copy()
        # check for the possibility in placing VNFs
        VNFsToPlace = len(list(VNRs.G_VNR.nodes())) #number of VNFs
        FinalSol = {'id':1,'VNFs':0,'TotVNFs':VNFsToPlace,'VLs':0,'TotVLs':0,'Placed':-1}
        #print(self.FinalSol)
        for j in range(VNFsToPlace):
            placed = False
            for k in list(lnp.keys()):
                if lnp[k]['CPU'] > VNRs.G_VNR.nodes[j]['CPU']:
                    #print("j'suis entré dans le if1")
                    #print(lnp[k]['CPU'],'?',self.VNRs.G_VNR.nodes[j]['CPU'])
                    if lnp[k]['RAM'] > VNRs.G_VNR.nodes[j]['RAM']:
                        #print("j'suis entré dans le if2")
                        if lnp[k]['ROM'] > VNRs.G_VNR.nodes[j]['ROM']:
                            PlacementSol[j] = {"id":k, "CPU_rq":VNRs.G_VNR.nodes[j]['CPU'], "RAM_rq":VNRs.G_VNR.nodes[j]['RAM'], "ROM_rq":VNRs.G_VNR.nodes[j]['ROM']}
                            placed = True
                            structEqNode[j] = k
                            VNFsToPlace = VNFsToPlace - 1
                            #print("j'suis entré dans le if3")
                            del lnp[k]
                            break
            if not placed:
                # one VNF wasn't placed -> failure of VNR placement
                VNRs_failure = VNRs_failure + 1
                break
            
        FinalSol['VNFs'] = FinalSol['TotVNFs'] - VNRs_failure
        
        #print(self.FinalSol)
        
        if VNFsToPlace == 0:
                # all VNFs were placed
                # reduce the allocated CPU
            nx.set_node_attributes(Solution,structEqNode,'NODE_EQ')
            for y in PlacementSol:
                nodes_prop[PlacementSol[y]['id']]['CPU'] = nodes_prop[PlacementSol[y]['id']]['CPU'] - PlacementSol[y]['CPU_rq']
                nodes_prop[PlacementSol[y]['id']]['RAM'] = nodes_prop[PlacementSol[y]['id']]['RAM'] - PlacementSol[y]['RAM_rq']
                nodes_prop[PlacementSol[y]['id']]['ROM'] = nodes_prop[PlacementSol[y]['id']]['ROM'] - PlacementSol[y]['ROM_rq']
            #print("node prop:",nodes_prop,end='\n')
            VNFs_Placement = PlacementSol.copy()
            #print('Successful placement of the VNFs of VNR ',i)
            
        else:
            #print('Failure in placing at least one VNF of VNR ',i)
            FinalSol['Placed'] = 0
            FinalSol['TotVLs'] = len(VNRs.G_VNR.edges())
            
        
        if VNRs_failure == 1 :#self.NumRq:
            self.Attendre -= 1
            return None
        # VLs placement
        placementVLs = False
        #print(VNFs_Placement)
        #for vr in VNFs_Placement:
        vrEdges, vrBWrq = VNRs.getEdgesDetails()
        #print(vrEdges)
        #print(vrBWrq)
        mappedVRedges = self.MappingVLstoLinks(VNFs_Placement,vrEdges,Solution)
        placementVLs, VLsplaced, G = self.CheckVLsPlacement(mappedVRedges,vrBWrq, Solution, reserve = True)
        FinalSol['TotVLs'] = len(vrEdges)
        FinalSol['VLs'] = VLsplaced
        if placementVLs:
            FinalSol['Placed'] = 1
            #SN_actu = VNE_Prob()
            #self.checkEdgesChgt(self.SN.SN_G.edges,self.SN.SN_G,G) # verify if nodes'ressources changed
            #self.SN_G = deepcopy(G)
            #self.getNodesRessourcesSN()
        else:
            FinalSol['Placed'] = 0
            Solution = None
        #print(self.FinalSol)
        
        #VNFs Placement
        """if FinalSol['Placed'] == 1 :
            for n in VNFs_Placement:
                self.SN_G.nodes[VNFs_Placement[n]['id']]['CPU']-= VNFs_Placement[n]['CPU_rq']
                #print("ok CPU")
                self.SN_G.nodes[VNFs_Placement[n]['id']]['RAM']-= VNFs_Placement[n]['RAM_rq']
                self.SN_G.nodes[VNFs_Placement[n]['id']]['ROM']-= VNFs_Placement[n]['ROM_rq']
                self.SN_G.nodes[VNFs_Placement[n]['id']]['idVNRPlaced'][VNRs.ID_] = {'CPU_rq':VNFs_Placement[n]['CPU_rq'],'RAM_rq':VNFs_Placement[n]['RAM_rq'],'ROM_rq':VNFs_Placement[n]['ROM_rq']}"""
        self.Attendre -= 1
        return Solution

    # Pas utiliser !
    def removeVNR(self,idVNRPlaced):
        noeuds = self.SN_G.nodes()
        for n in noeuds:
            if idVNRPlaced in self.SN_G.nodes[n]['idVNRPlaced'].keys() :
                self.SN_G.nodes[n]['CPU']+= self.SN_G.nodes[n]['idVNRPlaced'][idVNRPlaced]['CPU_rq']
                self.SN_G.nodes[n]['RAM']+= self.SN_G.nodes[n]['idVNRPlaced'][idVNRPlaced]['RAM_rq']
                self.SN_G.nodes[n]['ROM']+= self.SN_G.nodes[n]['idVNRPlaced'][idVNRPlaced]['ROM_rq']
                self.SN_G.nodes[n]['idVNRPlaced'].pop(idVNRPlaced,None) # remove VNF
        for edge in self.SN_G.edges():
            node_src = edge[0]
            node_dst = edge[1]
            if idVNRPlaced in self.SN_G[node_src][node_dst]['idVNRPlaced'].keys() :
                self.SN_G[node_src][node_dst]['Bandwidth'] += self.SN_G[node_src][node_dst]['idVNRPlaced'][idVNRPlaced]['Bandwidth_rq']
                self.SN_G[node_src][node_dst]['idVNRPlaced'].pop(idVNRPlaced,None) #remove VLs
