from pyomo.environ import *
import numpy as np
from pyomo.gdp import * 


def solveur(rails_liste,rayon,size):
    
    model = ConcreteModel()
    
    #Définition des paramètres du modèle
    nb_rails = len(rails_liste)
    taille_x = size[0] #longueur selon l'axe des abcisses de la carte
    taille_y = size[1] #longueur selon l'axe des ordonnées de la carte
    model.X = RangeSet(taille_x)
    model.Y = RangeSet(taille_y)
    M = 10000 #Majorant
    m = 1000 #Majorant
    
    # Initialisation du paramètre rails qui contient la liste des coordonnées des rails
    ini_rails = {}
    for i,x in enumerate(rails_liste):
        ini_rails[i+1] = x
   
    model.set_rails = RangeSet(nb_rails)
    model.rails = Param(model.set_rails, domain = model.X * model.Y, default = ini_rails )



    # Initialisation de la variable antennes représentée par un dictionnaire. Les clés sont les coordonnées de la matrice carte, les valeurs sont 0 (pas d'antenne) ou 1 (une antenne)
    # Les valeurs sont initialisées à 0
    model.set_antennes = Set(initialize=model.X * model.Y, ordered = True) 
    initialisation = {}
    initialisation_var_bin = {}
    for x in range(1,taille_x+1):
        for y in range(1,taille_y+1):
            initialisation[(x,y)] = 0
            for z in range(1,nb_rails+1):
                initialisation_var_bin[z,x,y] = 0

    model.antennes = Var(model.set_antennes, domain=Binary, initialize= initialisation)
    
    #Initialisition de variables binaires supplémentaires utilisées pour implémenter la disjonction de contraintes.
    model.var_bin = Var(model.set_rails * model.set_antennes, domain = Binary, initialize = initialisation_var_bin)
    

    #Définition de l'objectif d'optimisation : minimiser le nombre d'antennes
    def obj_expression(model):
        return sum(model.antennes[i] for i in model.X * model.Y)

    model.obj = Objective(rule=obj_expression)

    #Définition des contraintes 
    def exp_contrainte(model,k,i,j):
        return (model.rails[k][0]-i)**2 + (model.rails[k][1]-j)**2 - rayon**2 + M*(1-model.antennes[(i,j)]) <= m*M*(1-model.var_bin[k,i,j])


    def exp_contrainte_var_bin(model, k):
        return sum(model.var_bin[k,i[0],i[1]] for i in model.X * model.Y) >= 1

    model.contraintes = Constraint(model.set_rails * model.set_antennes, rule =exp_contrainte )
    model.contraintes_var_bin = Constraint(model.set_rails, rule = exp_contrainte_var_bin )

    # Résolution par le solveur
    opt = SolverFactory('glpk')
    opt.solve(model).write()

    # Renvoi de la liste des coordonnées des antennes
    antennes_liste = []
    for x in model.set_antennes:
        if model.antennes[x]() == 1:
            antennes_liste.append(x)
    
    return antennes_liste





