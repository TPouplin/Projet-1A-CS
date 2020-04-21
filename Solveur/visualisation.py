from Couverture_100 import *
import pygame
from pygame.locals import *
import numpy as np
import math
import pickle

def affichage(size, rail_list, l_antennes, rayon, fenetre):
    
    """Représentation de la grille avec les rails, les antennes et leur portée"""
    # rayon += math.sqrt(2) #pour que ce soit plus jolie
    w, h = pygame.display.get_surface().get_size() # dimension de la fenêtre (en pixels)
    width, height = w // size[1], h // size[0] # taille des cases (en pixels)
    
    # Placement des cercles rouges représentant la portée des antennes
    for (i,j) in l_antennes:
        left, top = (j+0.5)*width, (i+0.5)*height # On part des coordonnées du centre du rectangle
        left, top = left - width*rayon, top - height*rayon # On veut le coin supérieur gauche du rectangle
        left, top = int(left), int(top)
        pygame.draw.ellipse(fenetre, (255,0,0), Rect(left, top, int((2*width)*rayon), int((2*height)*rayon), width=0))
    
    
    # Placement des rectangles noirs représentant les rails
    for (i,j) in rail_list:
        left, top = j*width, i*height
        pygame.draw.rect(fenetre, (0,0,0), Rect(left, top, width, height))
    
    # Placement des rectangles bleus représentant les antennes
    for (i,j) in l_antennes:
        left, top = j*width, i*height
        pygame.draw.rect(fenetre, (0,0,255), Rect(left, top, width, height))        


def anim_pygame(size, rayon, num_antenna_limit):
    """Permet de placer les antennes avec la souris (clic gauche) et de visualiser le résultat (appuyer sur espace pour placer les antennes)"""
    mat = np.full(size,0)
    pygame.init()
    #Ouverture de la fenêtre Pygame
    dim_horizontale = 1000 # nombre de pixels de la fenêtre
    dim_verticale = (dim_horizontale * size[0]) // size[1] # On ajuste de manière à ce qu'on ait des carrés
    fenetre = pygame.display.set_mode((dim_horizontale, dim_verticale)) 

    #Settings
    pygame.key.set_repeat(1, 1) #Quand on garde la touche enfoncée on est en KEYDOWN

    #Initiation
    rail_list = []
    l_antennes = []
    w, h = pygame.display.get_surface().get_size()
    width, height = w // size[1], h // size[0]

    pygame.draw.rect(fenetre, (255,255,255), Rect(0, 0, w, h)) # Fond blanc
    
    
    affichage(size, rail_list, l_antennes, rayon, fenetre)
    pygame.display.flip()
    
    #BOUCLE INFINIE
    continuer = 1
    while continuer:

        # Modification de la grille
        for event in pygame.event.get():
            if event.type == QUIT: # On ferme la fenêtre
                continuer = 0
            if event.type == KEYDOWN and event.key == K_SPACE: # On appuie sur espace : calcul du placement d'antennes
                l_antennes = solveur(rail_list,rayon,size)
                print(len(l_antennes))
            if event.type == KEYDOWN and event.key == K_j:
                with open("exemple.txt", "rb") as fp:
                    rail_list = pickle.load(fp)
                    l_antennes = solveur(rail_list,rayon,size)
                    print("fichier trouvé")
            if event.type == KEYDOWN and event.key == K_s:
                with open("exemple.txt", "wb") as fp:
                    pickle.dump(rail_list,fp)
                    print("fichier save")
        mouse = pygame.mouse.get_pressed()
        x, y = pygame.mouse.get_pos()
        i, j = y // height, x // width
        if i < size[0] and j < size[1]:
            if mouse[0]: # si clic gauche
                rail_list.append((i,j)) # on ajoute un rail
            elif mouse[2]: # si clic droit
                if (i,j) in rail_list: rail_list.remove((i,j)) # on retire un rail
        
        # Affichage de la grille
        pygame.draw.rect(fenetre, (255,255,255), Rect(0, 0, w, h))
        fond = pygame.image.load("Solveur\Capture.jpg").convert()
        fenetre.blit(fond, (0,0))
        affichage(size, rail_list, l_antennes, rayon, fenetre)
        pygame.display.flip()

def main():
    anim_pygame((200,200), 10, 25)

if __name__== "__main__":
    main()
