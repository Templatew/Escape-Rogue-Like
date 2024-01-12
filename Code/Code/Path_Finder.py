#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#

'''
    Lorenz Cazaubon   G1
    Paul   Mauvoisin  G1
'''

##################################################################################################################

from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement
from Settings import *

def Find_Path_to_Player(matrix,debut,fin):

    #Créer la grille
    grid = Grid(matrix = matrix)

    # De où à où
    a, b = debut
    c, d = fin
    start = grid.node(a,b)
    end = grid.node(c,d)

    # Définir le style d'algo choisi
    finder = AStarFinder(diagonal_movement = DiagonalMovement.always, max_runs = PATH_MAX_RUNS)

    try:
        #Si on trouve un chemin dans le nombre de run autorisé
        path, runs = finder.find_path(start,end,grid)
    except:
        #Sinon
        path, runs = [(debut),(debut)], PATH_MAX_RUNS
    
    return path
