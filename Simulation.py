# -*- coding: utf-8 -*-
"""
Created on Fri May 14 23:45:32 2021

@author: Flavio_Loess
@source: yhadjadj
"""

import matplotlib.pyplot as plt
import simpy
import random
import SubstrateNet as sn
import VirtualNetReq as vn
from Tools import Tools
from copy import deepcopy
import Stat as stat # on importe le module permettant de donner les statistique du réseau Substrat sous forme de graphe

seed = 12345
lambdaMTBA = 1/2
lambdaMST = 1/9
SimDuration = 100
Processing = 1
listeService = []
listePlacer = []
listeDAttente = []
listeDExecution = []
listeRejet = []
modes = ["FIRSTFIT", "Evolutionary"]
mode = modes[1]
tabAbscisse = []
tabOrdonneeCPU = []
tabOrdonneeRAM = []
tabOrdonneeROM = []
tabOrdonneeBW = []
tabOrdonneeServices = []

# cette classe represente le service du point de vue Orchestrateur.
class Service:
    def __init__(self):
        self.VNR = vn.VirtualNetworkRequest() # attribu definissant le serice proprement dit
        self.Solution = None # la solution de placement du serice dans le substrat
        self.duree = 0 # la durée de vie du service
        self.ID = 0 # le numero du service par ordre d'arrivé
        
# fonction permettant d'afficher les courbes representant l'evolution des ressource en fonction du temps.
def affiche():
    g1, = plt.plot(tabAbscisse, tabOrdonneeCPU,'red')
    g2, = plt.plot(tabAbscisse, tabOrdonneeRAM, 'blue')
    g3, = plt.plot(tabAbscisse, tabOrdonneeROM, 'green')
    plt.legend([g1,g2,g3],['CPU','RAM','ROM'])
    plt.figure()
    g5, = plt.plot(tabAbscisse, tabOrdonneeServices, 'red')
    plt.legend([g5],['Nombre de services'])
    
# Fonction affichant un graphiquement un graphe afin de voir les statistiques du réseau substrat en fonction du temps
"""def AfficheGraphe(env, SN, ST):
    while True:
        ST.AfficherGraphe(SN.SN_G, "CPU", "ROM")
        yield env.timeout(Processing)
    return"""

# Ici on recueille les valeurs qui seront utilisées par la fonction : def affiche()
def TableauDeValeurs(t):
    tabAbscisse.append(t)
    tabOrdonneeServices.append(len(listeDExecution))
    sommeCPU = 0
    sommeRAM = 0
    sommeROM = 0
    for serv in listeDExecution:
        for node in serv.Solution.nodes():
            sommeCPU += serv.Solution.nodes[node]["CPU"]
            sommeRAM += serv.Solution.nodes[node]["RAM"]
            sommeROM += serv.Solution.nodes[node]["ROM"]
    tabOrdonneeCPU.append(sommeCPU)
    tabOrdonneeRAM.append(sommeRAM)
    tabOrdonneeROM.append(sommeROM)
    return

# Permettant de generer les service dont l'explication est donnée dans le ficher PDF
def Generateur(env):
    Counter = 0
    while True:
        t = int(random.expovariate(lambdaMTBA)) + 1 # on met +1 pour se rassurer que t n'est pas nul
        yield env.timeout(t)
        Counter += 1
        service = Service()
        Tools.Afficher(service.VNR.G_VNR) # On affiche graphiquement le service creer
        t = int(random.expovariate(lambdaMST)) + 1
        service.duree = t
        service.ID = Counter
        print("Service {} created ({})".format(service.ID,env.now))
        listeDAttente.append(service)
        listeService.append(service)
    return

# La fonction de placement FirstFit dont l'orgranigrame est dans le PDF
def Placement_FIRSTFIT(env, SN, ST):
    while(True):
        yield env.timeout(Processing)
        if len(listeDAttente) > 0:
            service = listeDAttente[0]
            Solution = SN.FirstFit_placement(service.VNR) # Ici on cherche une solution de placement
            if Solution != None: # si la fonction retour un None c'est parce que on n'a pas pu placer
                service.Solution = Solution
                SN.PlacerSolution(service.Solution)
                print("VNR {} placed ({})".format(service.ID,env.now))
                env.process(TraitementDesServices(env, SN, service, ST)) # on mlance la vie du service
                listePlacer.append(listeDAttente.pop(0))
            elif len(listeDExecution) == 0:
                listeRejet.append(listeDAttente.pop(0))
                
    return

# Meme explication que le precedant
def Placement_Evolutionary(env, SN, ST):
    while(True):
        yield env.timeout(Processing)
        if len(listeDAttente) > 0:
            service = listeDAttente[0]
            Solution = SN.GetSolutionDePlacement(service.VNR)
            if Solution != None:
                service.Solution = Solution
                SN.PlacerSolution(service.Solution)
                print("VNR {} placed ({})".format(service.ID,env.now))
                env.process(TraitementDesServices(env, SN, service, ST))
                listePlacer.append(listeDAttente.pop(0))
            elif len(listeDExecution) == 0:
                listeRejet.append(listeDAttente.pop(0))
                
    return

# La vie du service
def TraitementDesServices(env, SN, service, ST):
    print("VNR {} starts living {}".format(service.ID,env.now))
    ST.AfficherGraphe(SN.SN_G, "CPU", "ROM")
    listeDExecution.append(service)
    TableauDeValeurs(env.now)
    yield env.timeout(service.duree)
    SN.RetirerSolution(service.Solution)
    ST.AfficherGraphe(SN.SN_G, "CPU", "ROM")
    print("VNR {} left ({})".format(service.ID,env.now))
    listeDExecution.remove(service)
    return


if __name__ == "__main__":
    env = simpy.Environment()
    SN = sn.SubstrateNetwork()
    ST = stat.Statistique(SN.SN_G, "CPU", "ROM") # On instantie un objet nous permettant de faire le graphe pour mlontrer les statistiques du reseau
    ST.AfficherGraphe(SN.SN_G, "CPU", "ROM")
    G = deepcopy(SN.SN_G) # pas important
    #env.process(AfficheGraphe(env, SN, ST)) # Il s'agit un processus permettant d'afficher continuellemnt les statistiques du reseau
    env.process(Generateur(env)) # On lance le generateur de service qui s'execute indefiniment
    if mode == "Evolutionary":
        env.process(Placement_Evolutionary(env, SN, ST))
    elif mode == "FIRSTFIT":
        env.process(Placement_FIRSTFIT(env, SN, ST))
    env.run(until=SimDuration)
    affiche()
    print("********************************************")
    print("Services : ", len(listeService))
    print("En file d'attente : ", len(listeDAttente))
    print("Placés : ", len(listePlacer))
    print("Rejets : ", len(listeRejet))
    print("En cours : ", len(listeDExecution))
    print("********************************************")