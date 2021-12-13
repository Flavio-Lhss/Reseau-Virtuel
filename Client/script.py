import pygame
from pygame.locals import *

pygame.init()

#Ouverture de la fenêtre Pygame
fenetre = pygame.display.set_mode((640, 480), RESIZABLE)

#Chargement et collage du fond
fond = pygame.image.load("D1.PNG").convert()
fenetre.blit(fond, (0,0))

#Rafraîchissement de l'écran
pygame.display.flip()

#BOUCLE INFINIE
continuer = 1
while continuer:
	continuer = int(input())