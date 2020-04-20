from math import sqrt

def distance(p,I):
    """ Calcul la distance du point p à un ensemble de point I"""
    k = float("inf")
    for x in I:
        if sqrt((x[0]-p[0])**2+(x[1]-p[1])**2) < k:
            k = sqrt((x[0]-p[0])**2+(x[1]-p[1])**2)
    return k 


def UnitDiskCover(rails,rayon):
    """ Renvoie une liste d'antennes qui couvre l'ensemble des rails"""
    liste_antenne = []
    I = []
    liste_rails = sorted(rails, key=lambda tup: tup[1])
    while liste_rails != []:
        p = liste_rails.pop(0)
        if distance(p,I) > 2*rayon and distance(p,liste_antenne) > rayon: # on vérifie que le rails n'est pas déjà couvert 
            liste_antenne += [p]
            if distance((p[0]-1.5*rayon,p[1]+0.86*rayon),liste_rails) < rayon: # on vérifie qu'une rail existe directement en bas à droite du point p
                liste_antenne += [(p[0]-1.5*rayon,p[1]+0.86*rayon)]
            if distance((p[0]+1.5*rayon,p[1]+0.86*rayon),liste_rails) < rayon: # on vérifie qu'une rail existe directement en haut à droite du point p
                liste_antenne += [(p[0]+1.5*rayon,p[1]+0.86*rayon)]
            if distance((p[0],p[1]+1.73*rayon),liste_rails) < rayon: # on vérifie qu'une rail existe directement à droite du point p
                liste_antenne += [(p[0],p[1]+1.73*rayon)]            

            I += [p]           
            
    return liste_antenne