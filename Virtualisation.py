# -*- coding: utf-8 -*-
"""
Created on Sat May  1 16:38:52 2021

@author: Flavio_Loess
"""

import SubstrateNet as sn
import VirtualNetReq as vnr
import networkx as nx
import numpy as np
from Tools import Tools
import matplotlib.pyplot as plt
from copy import deepcopy

class Virtualisation:
    
    def __init__(self):
        self.SN = sn.SubstrateNetwork()
        self.SN_COPY = deepcopy(self.SN)
        print("--> Affichage du graphe substrat")
        Tools.PrintInfoGraphe(self.SN.SN_G)
        nx.draw(self.SN.SN_G, with_labels=True)
        plt.show()
        self.VNRs = []
        
    def run(self):
        running = True
        print("--> Initialisation")
        while(running):
            cmd = input("Enter Command : ")
            if cmd == "QUIT":
                running = False
                print("--> Fin du programme")
            elif cmd == "RESET SN":
                print("--> Reinitialisation du graphe substrat")
                self.SN = deepcopy(self.SN_COPY)
                print("--> Affichage du graphe substrat")
                Tools.PrintInfoGraphe(self.SN.SN_G)
            elif cmd == "VN REQ":
                print("--> Creation de service")
                VNR = vnr.VirtualNetworkRequest()
                print("--> Affichage du service")
                Tools.PrintInfoGraphe(VNR.G_VNR)
                nx.draw(VNR.G_VNR, with_labels=True)
                plt.show()
                Solution = self.SN.GetSolutionDePlacement(VNR.G_VNR)
                if Solution == None:
                    print("WARNING : PAS DE RESSOURCE DISPONIBLE POUR CE SERVICE")
                else:
                    print("--> Ressources disponibles / Affichage de la solution")
                    Tools.PrintSolution(Solution)
                    print("--> Placement du service")
                    self.VNRs.insert(0, Solution)
                    self.SN.PlacerSolution(Solution)
                    print("--> Affichage du graphe substrat mis à jour")
                    Tools.PrintInfoGraphe(self.SN.SN_G)
            elif cmd == "REMOVE LAST VNR":
                if len(self.VNRs) >= 1:
                    self.SN.RetirerSolution(self.VNRs.pop())
                    print("--> Affichage du graphe substrat mis à jour")
                    Tools.PrintInfoGraphe(self.SN.SN_G)
                else:
                    print("ERROR : AUCUN SERVICE EXISTANT")
            elif cmd == "REMOVE ALL VNR":
                if len(self.VNRs) >= 1:
                    for Sol in self.VNRs:
                        self.SN.RetirerSolution(Sol)
                    print("--> Affichage du graphe substrat mis à jour")
                    Tools.PrintInfoGraphe(self.SN.SN_G)
                else:
                    print("ERROR : AUCUN SERVICE EXISTANT")
            else:
                print("ERROR : COMMANDE INCONNUE")
    
            
if __name__ == "__main__": 
    VT = Virtualisation()
    VT.run()