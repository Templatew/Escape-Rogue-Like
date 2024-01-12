#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#

'''
    Lorenz Cazaubon   G1
    Paul   Mauvoisin  G1
'''

##################################################################################################################

from Settings import *
from Generation_map import *
import copy

#Class carte
class Map():
    
    def __init__(self, filename, level, abbrv, new = True):
        
        #Si on demande la création d'une nouvelle carte (Utile si on veut implémenter des cartes spéciales plus tard)
        if new:
            self.cells = generate(4,3,8, level, abbrv)
        
        #La data contient toutes les positions de départs des monstres, murs, lave, joueurs, items,.. (Valeur de chaque objet)
        #On lit les données dans un fichier .txt, toujours pratique si on veut implémenter des cartes spéciales (Il nous suffit de charger le bon .txt)
        data = []*GRIDHEIGHT
        with open(filename, 'rt') as f:
            for ligne in f:
                ligne = ligne[:-1]
                data.append([val for val in ligne])

        #La matrice contient la valeur de toutes les cases mais pas la valeur de l'objet qui est sur la case mais si un monstre peut marcher dessus ou non
        #C'est utile pour la fonction Find_Path_to_Player() dans le fichier Path_Finder.py
        matrix = copy.deepcopy(data)
        for i, ligne in enumerate(matrix):
            for j, val in enumerate(ligne):
                if val in ALPHABET_LOWERCASE:
                    val = -1
                elif val in ALPHABET_UPPERCASE:
                    val = 1
                matrix[i][j] = int(val)
        
        self.data = data ; self.matrix = matrix

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

    #Si on veut print la carte
    def __repr__(self):
        output = ""
        for lignes in self.data:
            for colonnes in lignes:
                output += str(colonnes)
            output += "\n"
        return output