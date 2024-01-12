#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#

'''
    Lorenz Cazaubon   G1
    Paul   Mauvoisin  G1
'''

##################################################################################################################

import random
import itertools
from Settings import *

#Style d'algo pour la génération de la carte
def _AStar(start, goal):
    def heuristic(a, b):
        ax, ay = a
        bx, by = b
        return abs(ax - bx) + abs(ay - by)

    def reconstructPath(n):
        if n == start:
            return [n]
        return reconstructPath(cameFrom[n]) + [n]

    def neighbors(n):
        x, y = n
        return (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)

    closed = set()
    open = set()
    open.add(start)
    cameFrom = {}
    gScore = {start: 0}
    fScore = {start: heuristic(start, goal)}

    while open:
        current = None
        for i in open:
            if current is None or fScore[i] < fScore[current]:
                current = i

        if current == goal:
            return reconstructPath(goal)

        open.remove(current)
        closed.add(current)

        for neighbor in neighbors(current):
            if neighbor in closed:
                continue
            g = gScore[current] + 1

            if neighbor not in open or g < gScore[neighbor]:
                cameFrom[neighbor] = current
                gScore[neighbor] = g
                fScore[neighbor] = gScore[neighbor] + heuristic(neighbor, goal)
                if neighbor not in open:
                    open.add(neighbor)
    return ()

#Fonction qui va générer un .txt qui sera une représentation de la map
#Ce .txt sera ensuite lu par la class map dans Tilemap.py
def generate(cellsX, cellsY, cellSize=5, level=1, abbrv = 'P'):
    
    # 1. Diviser la carte en une grille de cellule de même taille
    class Cell(object):
        def __init__(self, x, y, id):
            self.x = x
            self.y = y
            self.id = id
            self.connected = False
            self.connectedTo = []
            self.room = None

        def connect(self, other):
            self.connectedTo.append(other)
            other.connectedTo.append(self)
            self.connected = True
            other.connected = True

    cells = {}
    for y in range(cellsY):
        for x in range(cellsX):
            c = Cell(x, y, len(cells))
            cells[(c.x, c.y)] = c

    # 2. Choisir une cellule de façon aléatoire, en faire d'elle la cellule courante, la marquer connectée:
    current = lastCell = firstCell = random.choice(list(cells.values()))
    current.connected = True

    # 3. Temps que la cellule courante a des cellules voisines non connectées:
    def getNeighborCells(cell):
        for x, y in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            try:
                yield cells[(cell.x + x, cell.y + y)]
            except KeyError:
                continue

    while True:
        unconnected = [x for x in getNeighborCells(current) if not x.connected]
        if not unconnected:
            break

        # 3a. Connexion à l'une d'entre elles
        neighbor = random.choice(unconnected)
        current.connect(neighbor)

        # 3b. Faire de cette cellule la cellule courante
        current = lastCell = neighbor

    # 4. Temps qu'il y a des cellules non connectées:
    while [x for x in list(cells.values()) if not x.connected]:
        # 4a. Choisir de façon aléatoire une cellule connectée et une cellule voisine non connectée et les relier:
        candidates = []
        for cell in [x for x in list(cells.values()) if x.connected]:
            neighbors = [x for x in getNeighborCells(cell) if not x.connected]
            if not neighbors:
                continue
            candidates.append((cell, neighbors))
        cell, neighbors = random.choice(candidates)
        cell.connect(random.choice(neighbors))

    # 5. Choisir 0 ou plusieurs paires de cellules adjacentes qui ne sont pas connectées, et les relier:
    extraConnections = random.randint((cellsX + cellsY) // 4, int((cellsX + cellsY) // 1.2))
    maxRetries = 10
    while extraConnections > 0 and maxRetries > 0:
        cell = random.choice(list(cells.values()))
        neighbor = random.choice(list(getNeighborCells(cell)))
        if cell in neighbor.connectedTo:
            maxRetries -= 1
            continue
        cell.connect(neighbor)
        extraConnections -= 1

    # 6. Au sein de chaque cellule créer une salle de taille aléatoire:
    rooms = []
    for cell in list(cells.values()):
        width = random.randint(3, cellSize - 2)
        height = random.randint(3, cellSize - 2)
        x = (cell.x * cellSize) + random.randint(1, cellSize - width - 1)
        y = (cell.y * cellSize) + random.randint(1, cellSize - height - 1)
        floorTiles = []
        for i in range(width):
            for j in range(height):
                floorTiles.append((x + i, y + j))
        cell.room = floorTiles
        rooms.append(floorTiles)

    # 7. Pour chaque connexion entre 2 cellules:
    connections = {}
    for c in list(cells.values()):
        for other in c.connectedTo:
            connections[tuple(sorted((c.id, other.id)))] = (c.room, other.room)
    for a, b in list(connections.values()):
        # 7a. Créer un couloir aléatoire entre les salles dans une cellule
        start = random.choice(a)
        end = random.choice(b)

        corridor = []
        for tile in _AStar(start, end):
            if tile not in a and not tile in b:
                corridor.append(tile)
        rooms.append(corridor)

    # 8. Placer le héro et l'escalier.
    Hero = firstCell.room[(len(firstCell.room)-1)//2]
    stairsDown = lastCell.room[(len(lastCell.room)-1)//2]

    # créer les "tuiles"
    tiles = {}
    tilesX = cellsX * cellSize
    tilesY = cellsY * cellSize
    for x in range(tilesX):
        for y in range(tilesY):
            tiles[(x, y)] = "l"
    for xy in itertools.chain.from_iterable(rooms):
        tiles[xy] = "1"

    # toutes les tuiles adjacentes à du sol sont des murs
    def getNeighborTiles(xy):
        tx, ty = xy
        for x, y in ((-1, -1), (0, -1), (1, -1),
                     (-1, 0), (1, 0),
                     (-1, 1), (0, 1), (1, 1)):
            try:
                yield tiles[(tx + x, ty + y)]
            except KeyError:
                continue
    
    for xy, tile in tiles.items():
        if not tile == "1" and "1" in getNeighborTiles(xy):
            tiles[xy] = "0"
    
    # CHoisir un element aléaoirement selon un para, ici ça sera le level
    def randElement(level,collection):
        k = random.expovariate(1/level)
        n=1
        for i in range(max(collection)+1):
            if i<k and i>n and i in collection:
                n=i
        return random.choice(collection[n])

    # Placer les monstes
    for cell in list(cells.values()):
        tile = random.choice(cell.room)
        val = randElement(level,MOBS_BY_RARITY)
        tiles[tile] = MOBS[val]['abbrv']
    
    # Placer l'équipement
    for cell in list(cells.values()):
        tile = random.choice(cell.room)
        val = randElement(level,ITEMS_BY_RARITY)            
        tiles[tile] = ITEMS[val]['abbrv']

    # Placer le héro et l'escalier
    tiles[Hero] = abbrv
    tiles[stairsDown] = "s"
    
    output = ""
    for y in range(tilesY):
        for x in range(tilesX):
            output += (tiles[(x, y)])
        output +="\n"

    #On enregistre les données dans un .txt
    with open(os.path.join(MAPS_FOLDER,'map_procedural.txt'), 'w') as f:
        f.write(output)
    return cells