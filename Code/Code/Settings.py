#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#

'''
    Lorenz Cazaubon   G1
    Paul   Mauvoisin  G1
'''

##################################################################################################################


import sys, os
import pygame as pg

# Couleurs (R, V, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
VERYLIGHTGREY = (224,224,224)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BRIGHTRED = (255,50,50)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
FOG_COLOR = (3,2,1)

# Parametres jeu
WIDTH = 1174  #1024
HEIGHT = 768  #768
FPS = 60
TITLE = "ESCAPE"
BGCOLOR = DARKGREY
#ratio to go from vision to light radius
RATIO_VISION_LIGHT = 87.5
PATH_MAX_RUNS = 13
TILESIZE = 32
GRIDWIDTH = WIDTH // TILESIZE
GRIDHEIGHT = HEIGHT // TILESIZE
XP_TO_LEVEL_UP = 150
INVENTORY_SIZE = 8

#Status Effects
POISON_DURATION = 30; POISON_STRENGTH = 1

#Magie
FIREBALL_COST = 50; FIREBALL_DAMAGE = 4; FIREBALL_SPEED = 10  #Inversement proportionel
TP_COST = 30
HEAL_COST = 50; HEAL_VALUE = 8
INVISIBILITY_COST = 75; INVISIBILITY_DURATION = 10 #Turn
INVINCIBILITY_COST = 75; INVINCIBILITY_DURATION = 7
VISION_BOOST = 3; VISION_COST = 25; VISION_DURATION = 5
STRENGTH_BOOST = 4; STRENGTH_COST = 45; STRENGTH_DURATION = 8

#Projectiles
ARROW_SPEED = 7 #Inversement proportionel
ARROW_DAMAGE = 1 #En plus de l'attaque de base et arc

#UI
UI_HEART_SIZE = 22; UI_HEART_POS = (1046,340); UI_HEART_SPACE = 21
UI_ARMOR_SIZE = 22; UI_ARMOR_POS = (1086,340); UI_ARMOR_SPACE = 21
UI_XP_SIZE = 28; UI_XP_POS = (1126,337); UI_XP_SPACE = 21
UI_MP_SIZE = 28; UI_MP_POS = (1126,720); UI_MP_SPACE = 21
UI_SKULL_SIZE = 36; UI_SKULL_POS = (1040,400); UI_SKULL_TEXT_OFFSET = (57,17)
UI_HAT_SIZE = 38; UI_HAT_POS = (1043,440); UI_HAT_TEXT_OFFSET = (54,15)
UI_GOLD_SIZE = 42; UI_GOLD_POS = (1037,473); UI_GOLD_TEXT_OFFSET = (60,22)
UI_LEVEL_SIZE = 26; UI_LEVEL_POS = (1046,520); UI_LEVEL_TEXT_OFFSET = (51,15)
UI_BERSERK_SIZE = 25; UI_BERSERK_POS = (1046,560); UI_BERSERK_TEXT_OFFSET = (51,15)
UI_VISION_SIZE = 25; UI_VISION_POS = (1046,600); UI_VISION_TEXT_OFFSET = (51,15)
UI_INVINCIBLE_SIZE = 25; UI_INVINCIBLE_POS = (1046,640); UI_INVINCIBLE_TEXT_OFFSET = (51,15)
UI_INVISIBLE_SIZE = 28; UI_INVISIBLE_POS = (1043,680); UI_INVISIBLE_TEXT_OFFSET = (54,15)
UI_POISON_SIZE = 25; UI_POISON_POS = (1046,720); UI_POISON_TEXT_OFFSET = (51,15)

#Items
ITEM_REFRESH_TIME = 90
ITEM_MAX_MOV = 6


#----
ALPHABET_UPPERCASE = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
ALPHABET_LOWERCASE = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
ALPHABET = ALPHABET_UPPERCASE + ALPHABET_LOWERCASE

#Touches
KEYS_MOVEMENT = {pg.K_KP4: (-1, 0),     #KeyPad
                pg.K_KP6: (1, 0), 
                pg.K_KP8: (0, -1), 
                pg.K_KP2: (0, 1), 
                pg.K_KP7: (-1,-1), 
                pg.K_KP9: (1,-1), 
                pg.K_KP1: (-1,1), 
                pg.K_KP3: (1,1),

                pg.K_z: (0,-1),         #ZQSD
                pg.K_q: (-1,0),
                pg.K_d: (1,0),
                pg.K_s: (0,1),
                pg.K_a: (-1,-1),
                pg.K_e: (1,-1),
                pg.K_w: (-1,1),
                pg.K_c: (1,1),
                
                pg.K_UP: (0,-1),        #Arrow Keys
                pg.K_DOWN: (0,1),
                pg.K_LEFT: (-1,0),
                pg.K_RIGHT: (1,0)}        


# Fichiers
GAME_FOLDER = sys.path[0]
MAPS_FOLDER = os.path.join(GAME_FOLDER,'Maps')
ASSETS_FOLDER = os.path.join(GAME_FOLDER,"Assets")

MOBS_FOLDER = os.path.join(ASSETS_FOLDER,"Mobs")
PLAYER_FOLDER = os.path.join(ASSETS_FOLDER,"Player")
FONT_FOLDER = os.path.join(ASSETS_FOLDER,'Font')
MASK_FOLDER = os.path.join(ASSETS_FOLDER,'Mask')
ICON_FOLDER = os.path.join(ASSETS_FOLDER,"Icons")
START_SCREEN_FOLDER = os.path.join(ASSETS_FOLDER,"Start_screen")
END_SCREEN_FOLDER = os.path.join(ASSETS_FOLDER,'End_screen')
HELP_SCREEN_FOLDER = os.path.join(ASSETS_FOLDER,'Help_screen')

INVENTORY_SCREEN_FOLDER = os.path.join(ASSETS_FOLDER,'Inventory_screen')
STARS_FOLDER = os.path.join(INVENTORY_SCREEN_FOLDER,'Stars')

ELEMENTS_FOLDER = os.path.join(ASSETS_FOLDER,"Elements")
WALL_FOLDER = os.path.join(ELEMENTS_FOLDER,"Walls")
STAIRS_FOLDER = os.path.join(ELEMENTS_FOLDER,'Stairs')
LAVA_FOLDER = os.path.join(ELEMENTS_FOLDER,"Lava")

ITEMS_FOLDER = os.path.join(ASSETS_FOLDER,'Items')
COIN_FOLDER = os.path.join(ITEMS_FOLDER,'Coin')
ARMOR_FOLDER = os.path.join(ITEMS_FOLDER,'Armor')
WEAPON_FOLDER = os.path.join(ITEMS_FOLDER,'Weapons')
POTIONS_FOLDER = os.path.join(ITEMS_FOLDER,'Potions')
AMULETTES_FOLDER = os.path.join(ITEMS_FOLDER,'Amulettes')

PROJECTILE_FOLDER = os.path.join(ASSETS_FOLDER,'Projectiles')
FIREBALL_FOLDER = os.path.join(PROJECTILE_FOLDER,'Fireball')
ARROW_FOLDER = os.path.join(PROJECTILE_FOLDER,'Arrow')


#Creatures
PLAYER = {'Knight' : {'factor': 0.75, 'offset': (16,8), 'animation_cooldown': 65, 'abbrv': 'H', 'max_hp': 30, 'strength_melee': 8, 'strength_distance': 2, 'weapon_dmg': 0, 'armor': 50, 'vision': 4, 'mp': 150},   #Armure pas en % mais /150, donc 100% de réduction de dégât reçu --> armor = 150
         'Huntress' : {'factor': 1, 'offset': (16,6), 'animation_cooldown': 70, 'abbrv': 'U', 'max_hp': 24, 'strength_melee': 7, 'strength_distance': 3, 'weapon_dmg': 0, 'armor': 30, 'vision': 6, 'mp': 150},
         'Thief' : {'factor': 1.2, 'offset': (16,8), 'animation_cooldown': 80, 'abbrv': 'K', 'max_hp': 20, 'strength_melee': 9, 'strength_distance': 1, 'weapon_dmg': 0, 'armor': 35, 'vision': 5, 'mp': 150},
         }

MOBS = {
        #Bat
       'Bat': {'factor': 1,  #Taille png * factor
            'offset': (16,15),  #x, y
            'Health_Bar_offset': (-5,-20), #x, yd
            'Health_Bar_size': (12,2), #longueur, largeur
            'skull_offset': (45,45),
            'animation_cooldown': 70, 'abbrv': 'B', 'max_hp': 7, 'strength_melee': 2,'armor': 0,'xp':15, 'gold': 1},
        
        #Goblin
        'Goblin' : {'factor': 0.8,
            'offset': (16,10),
            'Health_Bar_offset': (-5,-20),
            'Health_Bar_size': (12,2), #longueur, largeur
            'skull_offset': (45,45),
            'animation_cooldown': 90, 'abbrv': 'G', 'max_hp': 9, 'strength_melee': 4,'armor': 0,'xp':25, 'gold': 2},

        #Champi
       'Champi': {'factor': 1,
            'offset': (16,15),
            'Health_Bar_offset': (-5,-18),
            'Health_Bar_size': (12,2), #longueur, largeur
            'skull_offset': (35,35),
            'animation_cooldown': 80, 'abbrv': 'C', 'max_hp': 15, 'strength_melee': 3, 'armor': 0, 'xp':30, 'gold': 2},

        #Wolf
       'Wolf': {'factor': 1,
            'offset': (16,15),
            'Health_Bar_offset': (-5,-30),
            'Health_Bar_size': (12,2), #longueur, largeur
            'skull_offset': (60,60),
            'animation_cooldown': 70, 'abbrv': 'W', 'max_hp': 13, 'strength_melee': 3,'armor': 0, 'xp':25, 'gold': 3},
       
        #Witch
       'Witch': {'factor': 1,
            'offset': (16,12),
            'Health_Bar_offset': (-5,-20),
            'Health_Bar_size': (12,2), #longueur, largeur
            'skull_offset': (60,60),
            'animation_cooldown': 80, 'abbrv': 'I', 'max_hp': 12, 'strength_melee': 4, 'armor': 0, 'xp':50, 'gold': 3},

        #Squelette
       'Squelette': {'factor': 0.74,
            'offset': (16,9),
            'Health_Bar_offset': (-5,-20),
            'Health_Bar_size': (12,2), #longueur, largeur
            'skull_offset': (45,45),
            'animation_cooldown': 80, 'abbrv': 'S', 'max_hp': 15, 'strength_melee': 4, 'armor': 2, 'xp':60, 'gold': 4},

        #Golem Rouge
       'Golem_Rouge': {'factor': 1,
            'offset': (16,6),
            'Health_Bar_offset': (-5,-20),
            'Health_Bar_size': (12,2), #longueur, largeur
            'skull_offset': (60,60),
            'animation_cooldown': 65, 'abbrv': 'R', 'max_hp': 24, 'strength_melee': 6, 'armor': 15, 'xp':90, 'gold': 8},

        #Golem Pierre
       'Golem_Pierre': {'factor': 1,
            'offset': (16,6),
            'Health_Bar_offset': (-5,-20),
            'Health_Bar_size': (12,2), #longueur, largeur
            'skull_offset': (60,60),
            'animation_cooldown': 80, 'abbrv': 'P', 'max_hp': 30, 'strength_melee': 6, 'armor': 30, 'xp':150, 'gold': 10}
       }

MOBS_BY_RARITY = {1: ['Bat'],
                  2: ['Goblin', 'Wolf'],
                  4: ['Champi','Witch'],
                  7: ['Squelette'],
                  10: ['Golem_Rouge'],
                  20: ['Golem_Pierre']
                }
#Equipements
ITEMS = {'Gold':{'abbrv': 'g','size': 8,'offset': (16,15), 'animation_cooldown': 150},
        'Leather_armor': {'val': 30, 'abbrv': 'b','offset': (16,19)}, 'Iron_armor': {'val': 60, 'abbrv': 'a','offset': (16,19)}, 'Golden_armor': {'val': 90, 'abbrv': 'o','offset': (16,19)},
        'Wood_sword':  {'val': 3, 'abbrv': 'y','offset': (16,19)}, 'Iron_sword':  {'val': 5, 'abbrv': 'u','offset': (16,19)}, 'Golden_sword':  {'val': 7, 'abbrv': 'i','offset': (16,19)},
        'Wood_spear': {'val': 3, 'abbrv': 'y','offset': (16,19)}, 'Iron_spear':  {'val': 5, 'abbrv': 'u','offset': (16,19)}, 'Golden_spear':  {'val': 7, 'abbrv': 'i','offset': (16,19)},
        'Green_bow': {'val': 2, 'abbrv': 'd','offset': (16,19)}, 'Red_bow': {'val': 3, 'abbrv': 'f','offset': (16,19)}, 'Golden_bow': {'val': 4, 'abbrv': 'h','offset': (16,19)},
        'Heal_potion': {'val': 6, 'abbrv': 'p', 'offset': (16,19)}, 'Mana_potion': {'val': 50, 'abbrv': 'm', 'offset': (16,19)},
        'Amulette_rouge': {'val': 4, 'abbrv': 'z', 'offset': (16,19)}, 'Amulette_orange' : {'val': 12, 'abbrv': 'q', 'offset': (16,19)}, 'Amulette_bleue' : {'val': 10, 'abbrv': 'n', 'offset': (16,19)}
}

ITEMS_BY_RARITY =  {1: ['Gold','Leather_armor'],
                    2: ['Green_bow','Heal_potion'],
                    3: ['Wood_sword'],
                    6: ['Iron_armor','Mana_potion'],
                    8: ['Red_bow', 'Amulette_bleue'],
                    10:['Iron_sword','Heal_potion'],
                    12:['Golden_armor','Amulette_rouge'],
                    13:['Golden_bow','Mana_potion'],
                    15:['Golden_sword','Amulette_orange']
}