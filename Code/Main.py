#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#

'''
    Lorenz Cazaubon   G1
    Paul   Mauvoisin  G1
    Jeu python: Rogue Like
'''

##################################################################################################################

#On ajoute les fichiers du dossier code
import sys, os
PATH = sys.path[0]
sys.path.append(os.path.join(PATH,'Code'))

#On importe ces fichiers
from Settings import *
from Sprites import *
from Path_Finder import *
from Tilemap import *

#On utilise time pour connaître le temps de chargement du jeu (game.load_data())
import time
start_time = time.time()

#Création de la classe jeu
class Game:

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.level = 1
        self.load_data()

    ##################################################################################################################
    "Chargement des fichiers (Assets)"
    ##################################################################################################################

    #Charger les fichiers pour pygame
    def load_data(self):
        
        #charger les animations des mobs:
        self.ANIMATION_DICT_MOB = {}
        for mob in MOBS:
            self.ANIMATION_DICT_MOB[mob] = self.animation_dico_mob(mob,MOBS[mob]['factor'])
        
        #Police d'écriture
        self.title_font = os.path.join(FONT_FOLDER,'Jonkle.TTF')
        self.ui_font = os.path.join(FONT_FOLDER,'Ordin.TTF')
        self.start_font = os.path.join(FONT_FOLDER,'Vermin_Vibes_1989.TTF')
        self.damage_font = pg.font.SysFont('Times New Roman', 18)
        
        #Effet de réduction de luminosité en pause
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha(); self.dim_screen.fill((0, 0, 0, 180))
        
        #Image mur
        self.wall_img = pg.image.load(os.path.join(WALL_FOLDER,'Wall_2.png')).convert_alpha(); self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE,TILESIZE))

        #Image escalier
        self.stairs_img = pg.image.load(os.path.join(STAIRS_FOLDER,'Ladder.png')).convert_alpha(); self.stairs_img = pg.transform.scale(self.stairs_img, (TILESIZE,TILESIZE))

        #Image panel
        self.panel_img = pg.image.load(os.path.join(ICON_FOLDER,'panel.png')).convert_alpha(); self.panel_img = pg.transform.scale(self.panel_img, (150, HEIGHT))
        
        #Start Screen
        self.start_screen = pg.image.load(os.path.join(START_SCREEN_FOLDER,'Start_Screen.png')).convert_alpha()
        self.astuce_screen = pg.image.load(os.path.join(START_SCREEN_FOLDER, 'Astuce.png')).convert_alpha()
        self.start_background = pg.image.load(os.path.join(START_SCREEN_FOLDER,'Start_Background.png')).convert_alpha(); self.start_background = pg.transform.scale(self.start_background, (WIDTH,HEIGHT))
        self.knight_screen = pg.image.load(os.path.join(START_SCREEN_FOLDER,'Knight_Screen.png')).convert_alpha()
        self.huntress_screen = pg.image.load(os.path.join(START_SCREEN_FOLDER,'Huntress_Screen.png')).convert_alpha()
        self.thief_screen = pg.image.load(os.path.join(START_SCREEN_FOLDER,'Thief_Screen.png')).convert_alpha()

        #Help Screen
        self.help_screen = pg.image.load(os.path.join(HELP_SCREEN_FOLDER,'Help_Screen.png')).convert_alpha()

        #Inventory screen
        self.inventory_screen = pg.image.load(os.path.join(INVENTORY_SCREEN_FOLDER,'Inventory_Screen.png')); self.inventory_screen = pg.transform.scale(self.inventory_screen, (WIDTH,HEIGHT))
        self.inventory_icon = pg.image.load(os.path.join(INVENTORY_SCREEN_FOLDER,'Inventory_icon.png')); self.inventory_icon = pg.transform.scale(self.inventory_icon, (self.inventory_icon.get_width()*2.3,self.inventory_icon.get_height()*2.3))
        self.inventory_slots = pg.image.load(os.path.join(INVENTORY_SCREEN_FOLDER,'Inventory_Slots.png')); self.inventory_slots = pg.transform.scale(self.inventory_slots, (self.inventory_slots.get_width()*2,self.inventory_slots.get_height()*2))
        self.inventory_equipped = pg.image.load(os.path.join(INVENTORY_SCREEN_FOLDER,'Inventory_equipped.png')); self.inventory_equipped = pg.transform.scale(self.inventory_equipped, (self.inventory_equipped.get_width()*2,self.inventory_equipped.get_height()*2))
        self.inventory_profile = pg.image.load(os.path.join(INVENTORY_SCREEN_FOLDER,'Inventory_profile.png')); self.inventory_profile = pg.transform.scale(self.inventory_profile, (self.inventory_profile.get_width()*2,self.inventory_profile.get_height()*2))

        #Stars
        no_stars = pg.image.load(os.path.join(STARS_FOLDER, '0.png')).convert_alpha()
        gold_1 = pg.image.load(os.path.join(STARS_FOLDER, 'Gold_1.png')).convert_alpha()
        gold_2 = pg.image.load(os.path.join(STARS_FOLDER, 'Gold_2.png')).convert_alpha()
        gold_3 = pg.image.load(os.path.join(STARS_FOLDER, 'Gold_3.png')).convert_alpha()
        silver_1 = pg.image.load(os.path.join(STARS_FOLDER, 'Silver_1.png')).convert_alpha()
        silver_2 = pg.image.load(os.path.join(STARS_FOLDER, 'Silver_2.png')).convert_alpha()
        silver_3 = pg.image.load(os.path.join(STARS_FOLDER, 'Silver_3.png')).convert_alpha()
        self.stars_dict = {0: no_stars,'Gold': {1:gold_1, 2: gold_2, 3: gold_3}, 'Silver': {1: silver_1, 2: silver_2, 3: silver_3}}


        #End Screen
        self.knight_end_screen = pg.image.load(os.path.join(END_SCREEN_FOLDER,'Knight_End_Screen.png'))
        self.thief_end_screen = pg.image.load(os.path.join(END_SCREEN_FOLDER,'Thief_End_Screen.png'))
        self.huntress_end_screen = pg.image.load(os.path.join(END_SCREEN_FOLDER,'Huntress_End_Screen.png'))

        #Amures
        self.leather_armor_img = pg.image.load(os.path.join(ARMOR_FOLDER,'Leather.png')); self.leather_armor_img = pg.transform.scale(self.leather_armor_img, (20,20))
        self.iron_armor_img = pg.image.load(os.path.join(ARMOR_FOLDER,'Iron.png')); self.iron_armor_img = pg.transform.scale(self.iron_armor_img, (20,20))
        self.golden_armor_img = pg.image.load(os.path.join(ARMOR_FOLDER,'Golden.png')); self.golden_armor_img = pg.transform.scale(self.golden_armor_img, (20,20))

        #Armes
        #Epées
        self.wood_sword_img = pg.image.load(os.path.join(WEAPON_FOLDER,'Wood_sword.png')); self.wood_sword_img = pg.transform.scale(self.wood_sword_img, (20,20))
        self.iron_sword_img = pg.image.load(os.path.join(WEAPON_FOLDER,'Iron_sword.png')); self.iron_sword_img = pg.transform.scale(self.iron_sword_img, (20,20))
        self.golden_sword_img = pg.image.load(os.path.join(WEAPON_FOLDER,'Golden_sword.png')); self.golden_sword_img = pg.transform.scale(self.golden_sword_img, (20,20))
        #Lances
        self.wood_spear_img = pg.image.load(os.path.join(WEAPON_FOLDER,'Wood_spear.png')); self.wood_spear_img = pg.transform.scale(self.wood_spear_img, (20,20))
        self.iron_spear_img = pg.image.load(os.path.join(WEAPON_FOLDER,'Iron_spear.png')); self.iron_spear_img = pg.transform.scale(self.iron_spear_img, (20,20))
        self.golden_spear_img = pg.image.load(os.path.join(WEAPON_FOLDER,'Golden_spear.png')); self.golden_spear_img = pg.transform.scale(self.golden_spear_img, (20,20))
        #Arcs
        self.green_bow_img = pg.image.load(os.path.join(WEAPON_FOLDER,'Green_bow.png')); self.green_bow_img = pg.transform.scale(self.green_bow_img, (20,20))
        self.red_bow_img = pg.image.load(os.path.join(WEAPON_FOLDER,'Red_bow.png')); self.red_bow_img = pg.transform.scale(self.red_bow_img, (20,20))
        self.golden_bow_img = pg.image.load(os.path.join(WEAPON_FOLDER,'Golden_bow.png')); self.golden_bow_img = pg.transform.scale(self.golden_bow_img, (20,20))

        #Potions
        #hp
        self.hp_img_list = [] 
        for i in range(3):
            image = pg.image.load(os.path.join(POTIONS_FOLDER,f"hp_{i}.png")).convert_alpha()
            if i == 2:
                val = (13,13)
            else:
                val = (15,15)
            image = pg.transform.scale(image, val)
            self.hp_img_list.append(image)
        #mana
        self.mana_img_list = [] 
        for i in range(3):
            image = pg.image.load(os.path.join(POTIONS_FOLDER,f"mana_{i}.png")).convert_alpha()
            if i == 2:
                val = (14,14)
            else:
                val = (15,15)
            image = pg.transform.scale(image, val)
            self.mana_img_list.append(image)

        #Amulettes
        self.amulette_rouge_img = pg.image.load(os.path.join(AMULETTES_FOLDER,'amulette_rouge.png')); self.amulette_rouge_img = pg.transform.scale(self.amulette_rouge_img, (14,14))
        self.amulette_orange_img = pg.image.load(os.path.join(AMULETTES_FOLDER,'amulette_orange.png')); self.amulette_orange_img = pg.transform.scale(self.amulette_orange_img, (14,14))
        self.amulette_bleue_img = pg.image.load(os.path.join(AMULETTES_FOLDER,'amulette_bleue.png')); self.amulette_bleue_img = pg.transform.scale(self.amulette_bleue_img, (14,14))

        #Flèche
        self.arrow_img = pg.image.load(os.path.join(ARROW_FOLDER,'Arrow.png')); self.arrow_img = pg.transform.scale(self.arrow_img, (20,20))

        #Images Skull
        self.skull_img = pg.image.load(os.path.join(ICON_FOLDER,'skull.png')).convert_alpha()
        self.skull2_img = pg.image.load(os.path.join(ICON_FOLDER,'skull_2.png')).convert_alpha(); self.skull2_img = pg.transform.scale(self.skull2_img, (UI_SKULL_SIZE,UI_SKULL_SIZE))

        #Image coeur
        Empty = pg.image.load(os.path.join(ICON_FOLDER,'ui_heart_empty.png')).convert_alpha(); Empty = pg.transform.scale(Empty, (UI_HEART_SIZE,UI_HEART_SIZE))
        Half = pg.image.load(os.path.join(ICON_FOLDER,'ui_heart_half.png')).convert_alpha(); Half = pg.transform.scale(Half, (UI_HEART_SIZE,UI_HEART_SIZE))
        Full = pg.image.load(os.path.join(ICON_FOLDER,'ui_heart_full.png')).convert_alpha(); Full =pg.transform.scale(Full, (UI_HEART_SIZE,UI_HEART_SIZE))
        self.coeur_dict = {'Empty': Empty, 'Half': Half, 'Full': Full}

        #Image armure ui
        self.armor_ui = pg.image.load(os.path.join(ICON_FOLDER,'Armor_UI.png')).convert_alpha(); self.armor_ui = pg.transform.scale(self.armor_ui, (UI_ARMOR_SIZE,UI_ARMOR_SIZE))

        #Image hat ui
        self.hat_ui = pg.image.load(os.path.join(ICON_FOLDER,'Hat_UI.png')).convert_alpha(); self.hat_ui = pg.transform.scale(self.hat_ui, (UI_XP_SIZE,UI_XP_SIZE))

        #Image xp ui
        self.xp_ui = pg.image.load(os.path.join(ICON_FOLDER,'xp_orange.png')).convert_alpha(); self.xp_ui = pg.transform.scale(self.xp_ui, (UI_XP_SIZE,UI_XP_SIZE))

        #Image mp ui
        self.mp_ui = pg.image.load(os.path.join(ICON_FOLDER,'mp_bleu.png')).convert_alpha(); self.mp_ui = pg.transform.scale(self.mp_ui, (UI_MP_SIZE,UI_MP_SIZE))

        #Image gold ui
        self.gold_ui = pg.image.load(os.path.join(ICON_FOLDER,'Gold_UI.png')).convert_alpha(); self.gold_ui = pg.transform.scale(self.gold_ui, (UI_GOLD_SIZE,UI_GOLD_SIZE))

        #Status ui
        self.level_ui = pg.image.load(os.path.join(ICON_FOLDER, 'Level_UI.png')).convert_alpha(); self.level_ui = pg.transform.scale(self.level_ui, (UI_LEVEL_SIZE,UI_LEVEL_SIZE))
        self.berserk_ui = pg.image.load(os.path.join(ICON_FOLDER,'Berserk_UI.png')).convert_alpha(); self.berserk_ui = pg.transform.scale(self.berserk_ui, (UI_BERSERK_SIZE,UI_BERSERK_SIZE))
        self.vision_ui = pg.image.load(os.path.join(ICON_FOLDER,'Vision_UI.png')).convert_alpha(); self.vision_ui = pg.transform.scale(self.vision_ui, (UI_VISION_SIZE,UI_VISION_SIZE))
        self.invincible_ui = pg.image.load(os.path.join(ICON_FOLDER,'Invincible_UI.png')).convert_alpha(); self.invincible_ui = pg.transform.scale(self.invincible_ui, (UI_INVINCIBLE_SIZE,UI_INVINCIBLE_SIZE))
        self.poison_ui = pg.image.load(os.path.join(ICON_FOLDER,'Poison_UI.png')).convert_alpha(); self.poison_ui = pg.transform.scale(self.poison_ui, (UI_POISON_SIZE,UI_POISON_SIZE))
        self.invisible_ui = pg.image.load(os.path.join(ICON_FOLDER,'Invisible_UI.png')).convert_alpha(); self.invisible_ui = pg.transform.scale(self.invisible_ui, (UI_INVISIBLE_SIZE,UI_INVISIBLE_SIZE))

        #Animation Lave
        #Nombre de fichier par dossier:
        n = len(os.listdir(LAVA_FOLDER))
        self.animation_lava_list = []
        for i in range(n):
            image = pg.image.load(os.path.join(LAVA_FOLDER,f"{i}.png")).convert_alpha()
            image = pg.transform.scale(image, (TILESIZE,TILESIZE))
            self.animation_lava_list.append(image)

        #Animation Coin
        #Nombre de fichier par dossier:
        n = len(os.listdir(COIN_FOLDER))
        self.animation_coin_list = []
        for i in range(n):
            image = pg.image.load(os.path.join(COIN_FOLDER,f"{i}.png")).convert_alpha()
            image = pg.transform.scale(image, (ITEMS['Gold']['size'],ITEMS['Gold']['size']))
            self.animation_coin_list.append(image)

        #Animtaion Fireball
        n = len(os.listdir(FIREBALL_FOLDER))
        self.animation_fireball_list = []
        for i in range(n):
            image = pg.image.load(os.path.join(FIREBALL_FOLDER,f"{i}.png")).convert_alpha()
            image = pg.transform.scale(image, (40,40))
            self.animation_fireball_list.append(image)

        #Sword cursor
        self.sword_img = pg.image.load(os.path.join(ICON_FOLDER,'sword.png')).convert_alpha(); self.sword_img = pg.transform.scale(self.sword_img, (self.sword_img.get_width()*0.6,self.sword_img.get_height()*0.6))

        #Effet de brouillard (fog of war)
        self.fog = pg.Surface(self.screen.get_size())
        self.fog.fill(FOG_COLOR)
        self.light_mask = pg.image.load(os.path.join(MASK_FOLDER,'light_350_med.png')).convert_alpha()

    #Créer un dico regroupant les images des animation d'un mob
    def animation_dico_mob(self,name,factor):

        MOB_FOLDER = os.path.join(MOBS_FOLDER, name)
        output = {'Right' : {'Idle' : [], 'Attack': [], 'Death': [], 'Run': [] }, 'Left': {'Idle' : [], 'Attack': [], 'Death': [], 'Run': [] }}

        for action in output['Right']:
            MOB_ACTION = os.path.join(MOB_FOLDER, action)

            #Nombre de fichier par dossier:
            n = len(os.listdir(MOB_ACTION))

            for i in range(n):
                image = pg.image.load(os.path.join(MOB_ACTION,f"{i}.png")).convert_alpha()
                image = pg.transform.scale(image,(image.get_width()*factor,image.get_height()*factor))
                
                #Pour orientation Gauche
                output['Right'][action].append(image)

                #Pour orientation Droite
                #On inverse l'image pour avoir une image selon les deux orientations: gauche et droite
                image = pg.transform.flip(image,True,False)    
                output['Left'][action].append(image)
        return output    

    ##################################################################################################################
    "Création du premier jeu"
    ##################################################################################################################

    def new(self,info = None, preferences = None):
        
        #charger la map
        self.map = Map(filename = os.path.join(MAPS_FOLDER,'map_procedural.txt'), level = self.level, abbrv = PLAYER[self.choice]['abbrv'])

        # initialiser le jeu
        self.all_sprites = pg.sprite.Group()
        self.elements = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.player = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.damage_text_group = pg.sprite.Group()

        #action cooldown
        self.action_cooldown = 0
        self.action_wait_time = 0

        self.paused = False
        self.show_inventory = False
        self.toggle_grid = False
        self.toggle_fog = True
        self.clicked = False
        self.current_player = 'Player'
        self.rested = False
        
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '0':
                    Wall(self, col, row)
                if tile == 's': #s for stairs
                    Stairs(self, col, row)
                if tile == 'l': #l for lava
                    Lava(self, col, row, self.animation_lava_list)
      
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):        
                nom = None; ready = False; weapon = False
                
                #Mobs
                if tile == 'G':
                    nom = 'Goblin'; ready = True
                elif tile == 'B':
                    nom = 'Bat'; ready = True
                elif tile == 'I':
                    nom = 'Witch'; ready = True
                elif tile == 'W':
                    nom = 'Wolf'; ready = True
                elif tile == 'S':
                    nom = 'Squelette'; ready = True
                elif tile == 'C':
                    nom = 'Champi'; ready = True
                elif tile == 'R':
                    nom = 'Golem_Rouge'; ready = True
                elif tile == 'P':
                    nom = 'Golem_Pierre'; ready = True
                
                if ready:
                    Mob(self, col, row, name = nom, animation_dict = self.ANIMATION_DICT_MOB[nom], abbrv = MOBS[nom]['abbrv'], armor = MOBS[nom]['armor'], xp = MOBS[nom]['xp'])

                #Items
                if tile == 'g':
                    Gold(self, col, row)
                elif tile == 'o':
                    Armor(self, col, row, name = 'Golden_armor')
                elif tile == 'a':
                    Armor(self, col, row, name = 'Iron_armor')
                elif tile == 'b':
                    Armor(self, col, row, name = 'Leather_armor')
                elif tile == 'y':
                    mat = 'Wood'
                    weapon = True
                elif tile == 'u':
                    mat = 'Iron'
                    weapon = True
                elif tile == 'i':
                    mat = 'Golden'
                    weapon = True
                else:
                    mat = ''
                if self.choice == 'Huntress':
                    obj = '_spear'
                    name = mat + obj
                else:
                    obj = '_sword'
                    name = mat + obj
                
                if tile == 'd':
                    name = 'Green_bow'
                    weapon = True
                elif tile == 'f':
                    name = 'Red_bow'
                    weapon = True
                elif tile == 'h':
                    name = 'Golden_bow'
                    weapon = True
                
                if weapon:
                    Weapon(self, col, row, name)

                if tile == 'p':
                    Potion(self, col, row, 'Heal_potion')
                elif tile == 'm':
                    Potion(self, col, row, 'Mana_potion')
                elif tile == 'z':
                    Amulette(self, col, row, 'Amulette_rouge')
                elif tile == 'q':
                    Amulette(self, col, row, 'Amulette_orange')
                elif tile == 'n':
                    Amulette(self, col, row, 'Amulette_bleue')

        #Pour éviter de cacher le héro on place le héro en dernier
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile in ['H','U','K']:
                    self.player = Player(self, col, row, name = self.choice)
        
        #Changer la taille du brouillard selon la vision du joueur
        self.fog_size = self.player.vision
        self.light_mask = pg.transform.scale(self.light_mask, (int(RATIO_VISION_LIGHT*self.fog_size),int(RATIO_VISION_LIGHT*self.fog_size))); self.light_rect = self.light_mask.get_rect()
        
        #Remettre les info du joueur si il a prit un escalier
        if info != None:
            self.player.hp = info['hp']; self.player.max_hp = info['max_hp']; self.player.bonus_strength = info['bonus_strength']
            self.player.kills = info['kills']; self.player.armor = info['armor']; self.player.bonus_armor = info['bonus_armor']
            self.player.xp = info['xp']; self.player.level = info['level']; self.player.vision = info['vision']; self.player.bonus_mana_regen = info['bonus_mana_regen']
            self.player.strength_melee = info['strength_melee']; self.player.strength_distance = info['strength_distance']
            self.player.base_strength = info['base_strength']; self.player.weapon_dmg = info['weapon_dmg']; self.player.weapon_dmg_distance = info['weapon_dmg_distance']
            self.player.gold = info['gold']; self.player.inventory = info['inventory']; self.player.mp = info['mp']; self.player.equipped = info['equipped']
            self.player.invincible = info['invincible']; self.player.invincible_duration = info['invincible_duration']
            self.player.invisible = info['invisible']; self.player.invisible_duration = info['invisible_duration']
            self.player.vision_duration = info['vision_duration']; self.player.strength_duration = info['strength_duration']
            self.player.vision_boost = info['vision_boost']; self.player.berserk = info['berserk']; self.player.poisoned = info['poisoned']; self.player.poisoned_duration = info['poisoned_duration']

            self.toggle_fog = preferences['Fog']; self.toggle_grid = preferences['Grid']

    ##################################################################################################################
    "Execution du jeu (temps que le jeux tourne)"
    ##################################################################################################################

    def run(self):

        # si player.Alive  == False alors le jeu s'arrête
        while self.player.Alive:
            
            self.dt = self.clock.tick(FPS)

            self.events()
            if not self.paused and not self.show_inventory:
                self.update()
            self.draw()

    ##################################################################################################################
    "Affichage"
    ##################################################################################################################

    #Mis à jour de tout les éléments du jeu
    def update(self):
        
        if self.player.Alive:
            # Mette à jour le jeu
            self.all_sprites.update()
            self.damage_text_group.update()

            if self.fog_size != self.player.vision:
                self.fog_size = self.player.vision
                self.light_mask = pg.transform.scale(self.light_mask, (int(RATIO_VISION_LIGHT*self.fog_size),int(RATIO_VISION_LIGHT*self.fog_size))); self.light_rect = self.light_mask.get_rect()

    #Dessiner les éléments
    #Déssiner le quadrillage
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    #Fonction pour déssiner un texte sur la fenetre d'affichage
    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        elif align == "ne":
            text_rect.topright = (x, y)
        elif align == "sw":
            text_rect.bottomleft = (x, y)
        elif align == "se":
            text_rect.bottomright = (x, y)
        elif align == "n":
            text_rect.midtop = (x, y)
        elif align == "s":
            text_rect.midbottom = (x, y)
        elif align == "e":
            text_rect.midright = (x, y)
        elif align == "w":
            text_rect.midleft = (x, y)
        elif align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    #Déssiner l'interface en jeu (Affichage santé, xp, mana,..)
    def draw_panel(self):
        #Déssiner le rectangle
        self.screen.blit(self.panel_img, (1024,0))

        if self.player.Alive:
            
            #Afficher la santé du joueur
            nb_full = self.player.hp // 2
            if self.player.hp % 2 != 0:
                nb_half = 1
            else:
                nb_half = 0
            nb_empty = (self.player.max_hp //2) - (nb_full + nb_half)
            
            for i in range(nb_full):
                x,y = UI_HEART_POS
                self.screen.blit(self.coeur_dict['Full'], (x,y+(UI_HEART_SPACE*(-i))))
            
            for i in range(nb_full,nb_half+nb_full):
                x,y = UI_HEART_POS
                self.screen.blit(self.coeur_dict['Half'], (x,y+(UI_HEART_SPACE*(-i))))
            
            for i in range(nb_full+nb_half,nb_half+nb_full+nb_empty):
                x,y = UI_HEART_POS
                self.screen.blit(self.coeur_dict['Empty'], (x,y+(UI_HEART_SPACE*(-i))))

            #Afficher l'armure
            for i in range(self.player.armor//10):
                x,y = UI_ARMOR_POS
                self.screen.blit(self.armor_ui, (x,y+(UI_ARMOR_SPACE*(-i))))

            #Afficher l'xp
            for i in range(self.player.xp//10):
                x,y = UI_XP_POS
                self.screen.blit(self.xp_ui, (x,y+(UI_XP_SPACE*(-i))))

            #Afficher les mp
            for i in range(self.player.mp//10):
                x,y = UI_MP_POS
                self.screen.blit(self.mp_ui, (x,y+(UI_MP_SPACE*(-i))))

            #Afficher le nb de kills
            x, y  = UI_SKULL_POS
            dx, dy = UI_SKULL_TEXT_OFFSET
            self.screen.blit(self.skull2_img, (x,y))
            self.draw_text(str(self.player.kills),self.ui_font ,22, WHITE, x + dx , y + dy, align = "center")

            #Afficher le level
            x, y  = UI_HAT_POS
            dx, dy = UI_HAT_TEXT_OFFSET
            self.screen.blit(self.hat_ui, (x,y))
            self.draw_text(str(self.player.level),self.ui_font ,22, WHITE, x + dx , y + dy, align = "center")

            #Afficher l'or
            x, y  = UI_GOLD_POS
            dx, dy = UI_GOLD_TEXT_OFFSET
            self.screen.blit(self.gold_ui, (x,y))
            self.draw_text(str(self.player.gold),self.ui_font ,22, WHITE, x + dx , y + dy, align = "center")

            #Afficher le level du jeu
            x, y  = UI_LEVEL_POS
            dx, dy = UI_LEVEL_TEXT_OFFSET
            self.screen.blit(self.level_ui, (x,y))
            self.draw_text(str(self.level),self.ui_font ,22, WHITE, x + dx , y + dy, align = "center")

            if self.player.invisible:
                x, y  = UI_INVISIBLE_POS
                dx, dy = UI_INVISIBLE_TEXT_OFFSET
                self.screen.blit(self.invisible_ui, (x,y))
                self.draw_text(str(self.player.invisible_duration),self.ui_font ,22, WHITE, x + dx , y + dy, align = "center")
            
            if self.player.invincible:
                x, y  = UI_INVINCIBLE_POS
                dx, dy = UI_INVINCIBLE_TEXT_OFFSET
                self.screen.blit(self.invincible_ui, (x,y))
                self.draw_text(str(self.player.invincible_duration),self.ui_font ,22, WHITE, x + dx , y + dy, align = "center")

            if self.player.berserk:
                x, y  = UI_BERSERK_POS
                dx, dy = UI_BERSERK_TEXT_OFFSET
                self.screen.blit(self.berserk_ui, (x,y))
                self.draw_text(str(self.player.strength_duration),self.ui_font ,22, WHITE, x + dx , y + dy, align = "center")

            if self.player.vision_boost:
                x, y  = UI_VISION_POS
                dx, dy = UI_VISION_TEXT_OFFSET
                self.screen.blit(self.vision_ui, (x,y))
                self.draw_text(str(self.player.vision_duration),self.ui_font ,22, WHITE, x + dx , y + dy, align = "center")

            if self.player.poisoned:
                x, y  = UI_POISON_POS
                dx, dy = UI_POISON_TEXT_OFFSET
                self.screen.blit(self.poison_ui, (x,y))
                self.draw_text(str(self.player.poisoned_duration),self.ui_font ,22, WHITE, x + dx , y + dy, align = "center")
            

        else:
            for i in range(self.player.max_hp // 2):
                x,y = UI_HEART_POS
                self.screen.blit(self.coeur_dict['Empty'], (x,y+(UI_HEART_SPACE*(-i))))

    #Déssiner le brouillard de guerre
    def render_fog(self):

        #Déssiner le "Light Mask" (Gradient) par dessus le brouillard
        self.fog.fill(FOG_COLOR)
        self.light_rect.center = self.player.rect.center
        self.fog.blit(self.light_mask, self.light_rect)
        self.screen.blit(self.fog, (0,0), special_flags=pg.BLEND_MULT)

    #On appelle toutes les fonctions de dessins précédentes ici, afin de déssiner la fenetre d'affichage du jeu
    def draw(self):
        
        #fps counter
        #pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))

        if self.player.invisible and self.current_player == 'Others':
            self.current_player = 'Player'
            
        #bg
        self.screen.fill(BGCOLOR)
        
        if self.toggle_grid:
            self.draw_grid()

        self.all_sprites.draw(self.screen)
 
        for mob in self.mobs:

            #si le mob est en vie:
            if mob.Alive and mob.near:
                
                #Afficher les barres d'hp mobs
                mob.Health_Bar_draw()
                
        if self.current_player == 'Others' and self.action_cooldown >= self.action_wait_time:
            self.move_all_monsters()
            self.current_player = 'Player'
            self.action_cooldown = 0

        #Si brouillard activé
        if self.toggle_fog:
            self.render_fog()

        #Afficher les dégâts
        self.damage_text_group.draw(self.screen)

        #Panel
        self.draw_panel()

        #Transformer la souris en épée quand on survole un ennemis
        #Rendre la souris visible
        #Attaque à distance
        pg.mouse.set_visible(True)
        pos = pg.mouse.get_pos()
        if self.current_player == 'Player':
            for mob in self.mobs:
                if mob.rect.collidepoint(pos) and mob.Alive and mob.near:
                    #Cacher la souris
                    pg.mouse.set_visible(False)
                    #Place l'image de l'épée à la position de la souris
                    self.screen.blit(self.sword_img,pos)
                    
                    #Attaque boule de feu
                    if self.clicked_right == True and self.player.mp >= FIREBALL_COST:
                        self.current_player = None
                        self.player.mp -= FIREBALL_COST
                        FireBall(self,self.player,mob)
                        self.clicked_right = False
                    
                    #Attaque à l'arc
                    if self.clicked_left == True:
                        self.current_player = None
                        Arrow(self,self.player,mob)
                        self.clicked_left = False

        #Si en pause
        if self.paused:
            self.show_help_screen()
        
        #Si on doit afficher l'inventaire
        if self.show_inventory:
            self.show_inventory_screen()

        pg.display.flip()

    #Ecran de début
    def show_start_screen(self):
        stay = True
        pre_choice = None
        while stay:
            
            for event in pg.event.get():
                
                if event.type == pg.QUIT:
                    self.quit()
                
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.quit()

                    if event.key == pg.K_h:
                        pre_choice = 'Knight'
                    
                    if event.key == pg.K_u:
                        pre_choice = 'Huntress'
                    
                    if event.key == pg.K_k:
                        pre_choice = 'Thief'
                    
                    if pre_choice != None and event.key == pg.K_RETURN:
                        self.choice = pre_choice
                        stay = False
            
            self.screen.blit(self.start_background, (0, 0))
            self.screen.blit(self.dim_screen, (0,0))
            if pre_choice == None:
                self.screen.blit(self.start_screen, (0,0))
            elif pre_choice == 'Knight':
                self.screen.blit(self.knight_screen, (0,0))
            elif pre_choice == 'Huntress':
                self.screen.blit(self.huntress_screen, (0,0))
            elif pre_choice == 'Thief':
                self.screen.blit(self.thief_screen, (0,0))

            pg.display.flip()

        stay = True
        while stay:
            
            self.screen.blit(self.start_background, (0, 0))
            self.screen.blit(self.dim_screen, (0,0))
            self.screen.blit(self.astuce_screen, (0,0))
            pg.display.flip()

            for event in pg.event.get():

                if event.type == pg.QUIT:
                    self.quit()
                
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.quit()
                    else:
                        stay = False

    #Ecran d'aide
    def show_help_screen(self):
        self.screen.blit(self.dim_screen, (0,0))
        self.screen.blit(self.help_screen, (0,0))

    #Inventaire
    def show_inventory_screen(self):

        self.screen.blit(self.dim_screen, (0,0))
        self.screen.blit(self.inventory_screen, (30,0))
        self.screen.blit(self.inventory_icon, (WIDTH/2 - 30,225))
        self.screen.blit(self.inventory_slots, (410,320))
        self.screen.blit(self.inventory_equipped, (278,280))
        self.screen.blit(self.inventory_profile, (294, 225))

        for i in range(1,9):
            self.draw_text(str(i),self.start_font, 25, BLACK, 386 + i * 66, 325, align = "center")

        if self.select_inventory == None:
            self.draw_text("Select an item..",self.start_font, 40, BLACK, 580, 470, align = "center")

        else:
            image = pg.transform.scale(self.player.inventory[self.select_inventory]['img'], (64,64))
            self.screen.blit(image, (436,435))
            stars = self.player.inventory[self.select_inventory]['stars']
            stars_color = self.player.inventory[self.select_inventory]['stars_color']
            if stars == 0:
                image_star = self.stars_dict[0]
            else:
                image_star = self.stars_dict[stars_color][stars]

            image_star = pg.transform.scale(image_star, (image_star.get_width()*0.8,image_star.get_height()*0.8) )
            self.screen.blit(image_star, (496,435))
            self.draw_text("value = " + str(self.player.inventory[self.select_inventory]['val']),self.start_font, 35, BLACK, 745, 475, align = "center")
            self.draw_text("Press enter or u to use and x to delete",self.start_font, 28, BLACK, 680, 540, align = "center")

        for i, obj in enumerate(self.player.inventory): 
            image = pg.transform.scale(obj['img'], (32,32))
            self.screen.blit(image, (436 + 66 * i,352))
        
        for obj in self.player.equipped:
            if self.player.equipped[obj] != None:
                image = pg.transform.scale(self.player.equipped[obj]['img'], (32,32))
                if obj == 'armor':
                    i = 0
                elif obj == 'weapon':
                    i = 1
                elif obj == 'bow':
                    i = 2
                elif obj == 'amulette':
                    i = 3
                self.screen.blit(image, (310 ,301 + 66 * i))

    #Ecran de fin
    def show_end_screen(self):
        stay = True
        while stay:
            
            
            self.screen.blit(self.start_background, (0, 0))
            self.screen.blit(self.dim_screen, (0,0))
            if self.choice == 'Knight':
                self.screen.blit(self.knight_end_screen, (0,0))
            elif self.choice == 'Huntress':
                self.screen.blit(self.huntress_end_screen, (0,0))
            elif self.choice == 'Thief':
                self.screen.blit(self.thief_end_screen, (0,0))
            self.draw_text(str(self.level),self.start_font, 60, BLACK, 710, 230, align = "center")
            pg.display.flip()

            for event in pg.event.get():
                
                if event.type == pg.QUIT:
                    self.quit()
                
                if event.type == pg.KEYDOWN:
                    
                    if event.key == pg.K_ESCAPE or event.key == pg.K_n:
                        self.quit()
                    
                    if event.key == pg.K_y:
                        self.show_start_screen()
                        self.level = 1
                        self.map = Map(filename = os.path.join(MAPS_FOLDER,'map_procedural.txt'), level = self.level, abbrv = PLAYER[self.choice]['abbrv'])
                        while True:

                            self.new()
                            self.run()
                            self.show_end_screen()

    ##################################################################################################################
    "Actions/Evénements"
    ##################################################################################################################

    #Quitter le jeu
    def quit(self):
        pg.quit()
        sys.exit()

    #Gestion des touches clavier et boutons souris
    def events(self):

        #Cooldown action
        if self.player.Alive:
            self.action_cooldown += 1

        #Gérer les évenements (pression touche, etc)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()

            #Clavier
            if event.type == pg.KEYDOWN:
                
                #Quitter
                if not self.paused and not self.show_inventory and event.key == pg.K_ESCAPE:
                    self.quit()
                
                #Help
                if not self.show_inventory and (event.key == pg.K_h or event.key == pg.K_ESCAPE):
                    self.paused = not self.paused 
                        
                #Inventaire
                elif not self.paused:
                    if event.key == pg.K_i or event.key == pg.K_ESCAPE:
                        self.show_inventory = not self.show_inventory
                        self.select_inventory = None
                    
                    elif self.show_inventory:
                        
                        if self.select_inventory != None:

                            if event.key == pg.K_u or event.key == pg.K_RETURN:
                                fonc = self.player.inventory[self.select_inventory]['usage']
                                fonc(self.player)

                                if 'sword' in self.player.inventory[self.select_inventory]['name'] or 'spear' in self.player.inventory[self.select_inventory]['name']:
                                    self.player.equipped['weapon'] = self.player.inventory[self.select_inventory]
                                elif 'bow' in self.player.inventory[self.select_inventory]['name']:
                                    self.player.equipped['bow'] = self.player.inventory[self.select_inventory]
                                elif 'potion' in self.player.inventory[self.select_inventory]['name']:
                                    pass
                                elif 'Amulette' in self.player.inventory[self.select_inventory]['name']:
                                    self.player.equipped['amulette'] = self.player.inventory[self.select_inventory]
                                else:
                                    self.player.equipped['armor'] = self.player.inventory[self.select_inventory]

                                self.player.inventory.pop(self.select_inventory)
                                self.select_inventory = None

                            if event.key == pg.K_x:
                                self.player.inventory.pop(self.select_inventory)
                                self.select_inventory = None

                        if (event.key == pg.K_1 or event.key == pg.K_KP1) and len(self.player.inventory) > 0:
                            self.select_inventory = 0                      
                        elif (event.key == pg.K_2 or event.key == pg.K_KP2) and len(self.player.inventory) > 1:
                            self.select_inventory = 1
                        elif (event.key == pg.K_3 or event.key == pg.K_KP3) and len(self.player.inventory) > 2:
                            self.select_inventory = 2
                        elif (event.key == pg.K_4 or event.key == pg.K_KP4) and len(self.player.inventory) > 3:
                            self.select_inventory = 3
                        elif (event.key == pg.K_5 or event.key == pg.K_KP5) and len(self.player.inventory) > 4:
                            self.select_inventory = 4
                        elif (event.key == pg.K_6 or event.key == pg.K_KP6) and len(self.player.inventory) > 5:
                            self.select_inventory = 5
                        elif (event.key == pg.K_7 or event.key == pg.K_KP7) and len(self.player.inventory) > 6:
                            self.select_inventory = 6
                        elif (event.key == pg.K_8 or event.key == pg.K_KP8) and len(self.player.inventory) > 7:
                            self.select_inventory = 7

                if not self.paused and not self.show_inventory:
                    
                    #Grilles
                    if event.key == pg.K_g:
                        self.toggle_grid = not self.toggle_grid

                    #Repos
                    elif event.key == pg.K_r and self.rested == False:
                        self.rest()

                    #Magie
                    #------------------------------------------------------------#
                    #Téléportation
                    elif event.key == pg.K_1 and self.player.mp >= TP_COST:
                        self.player.teleport(self)
                        
                    #Heal
                    elif event.key == pg.K_2 and self.player.mp >= HEAL_COST:
                        self.player.heal(HEAL_VALUE)
                        self.player.mp -= HEAL_COST
                    
                    #Invisibilité
                    elif event.key == pg.K_3 and self.player.mp >= INVISIBILITY_COST and not self.player.invisible:
                        self.player.mp -= INVISIBILITY_COST
                        self.player.invisible = True
                        self.player.invisible_duration = INVISIBILITY_DURATION
                    
                    #Invincible:
                    elif event.key == pg.K_4 and self.player.mp >= INVINCIBILITY_COST and not self.player.invincible:
                        self.player.mp -= INVINCIBILITY_COST
                        self.player.invincible = not self.player.invincible
                        self.player.invincible_duration = INVINCIBILITY_DURATION

                    #Super Force
                    elif event.key == pg.K_5 and self.player.mp >= STRENGTH_COST and not self.player.berserk:
                        self.player.mp -= STRENGTH_COST
                        self.player.strength_melee += STRENGTH_BOOST
                        self.player.strength_distance += STRENGTH_BOOST
                        self.player.strength_duration = STRENGTH_DURATION
                        self.player.berserk = True
                    
                    #Boost Vision
                    elif event.key == pg.K_6 and self.player.mp >= VISION_COST and not self.player.vision_boost:
                        self.player.mp -= VISION_COST
                        self.player.vision += VISION_BOOST
                        self.player.vision_duration = VISION_DURATION
                        self.player.vision_boost = True

                    #------------------------------------------------------------#

                    #Ladder
                    elif event.key == pg.K_l:
                        self.go_down()
                    
                    #Brouillard
                    elif event.key == pg.K_n:
                        self.toggle_fog = not self.toggle_fog

                    #Heal
                    elif event.key == pg.K_m:
                        self.player.hp = self.player.max_hp
                        self.player.mp = 150
                        self.player.xp = 150

                    #Invincible:
                    elif event.key == pg.K_v:
                        self.player.invincible = not self.player.invincible
                        self.player.invincible_duration = 1000
                        
                    #Damage
                    elif event.key == pg.K_k:
                        self.hp = 0
                        self.player.Alive = False

                    #Joueur
                    elif self.player.Alive and self.current_player == 'Player' and self.action_cooldown >= self.action_wait_time:
                        if event.key in KEYS_MOVEMENT: 
                            if self.player.move(KEYS_MOVEMENT[event.key]):
                                self.current_player = 'Others'
                                self.action_cooldown = 0

            #Souris
            if event.type == pg.MOUSEBUTTONDOWN:
                if pg.mouse.get_pressed() == (True, False, False):
                    self.clicked_left = True
                elif pg.mouse.get_pressed() == (False, False, True):
                    self.clicked_right = True
            else:
                self.clicked_left = False; self.clicked_right = False

    #Déplacer tout les monstres
    def move_all_monsters(self):
        for mob in self.mobs:
            if mob.Alive:
                next_node = Find_Path_to_Player(self.map.matrix,(mob.x,mob.y),(self.player.x,self.player.y))[1]
                x, y = next_node
                mob.move((x-mob.x,y-mob.y))

    #Distance entre deux mobs
    def distance(self,mob,other):
        return math.sqrt((mob.x-other.x)**2 + (mob.y-other.y)**2)

    #Repos
    def rest(self):
        for _ in range(10):
            self.move_all_monsters()
            if not self.player.Alive:
                self.show_end_screen()
                return False
            self.update()
            self.draw()
        self.player.heal(8)
        self.rested = True

    #Le joueur descend d'un étage
    def go_down(self):
        self.level += 1
        info = {'hp': self.player.hp, 'max_hp': self.player.max_hp, 'kills': self.player.kills, 'mp': self.player.mp, 'weapon_dmg': self.player.weapon_dmg,  'weapon_dmg_distance': self.player.weapon_dmg_distance,
                'strength_melee': self.player.strength_melee, 'strength_distance': self.player.strength_distance, 'base_strength': self.player.base_strength,
                'armor': self.player.armor, 'xp': self.player.xp, 'level': self.player.level, 'gold': self.player.gold, 'inventory': self.player.inventory, 'equipped': self.player.equipped,
                'invisible': self.player.invisible, 'invisible_duration': self.player.invisible_duration, 'invincible': self.player.invincible, 'invincible_duration': self.player.invincible_duration,
                'vision_duration': self.player.vision_duration, 'strength_duration': self.player.strength_duration, 'vision': self.player.vision, 'vision_boost': self.player.vision_boost,
                'berserk': self.player.berserk, 'poisoned': self.player.poisoned, 'poisoned_duration': self.player.poisoned_duration, 'bonus_strength': self.player.bonus_strength, 'bonus_armor': self.player.bonus_armor, 'bonus_mana_regen': self.player.bonus_mana_regen
                }
        preferences = {'Grid': self.toggle_grid, 'Fog': self.toggle_fog}
        self.new(info,preferences)
        
#Lancer le jeu
def main(): 

    #Créer le jeu
    print("Chargement..")
    g = Game()
    print('Durée de chargement: ',"%s seconds" % (time.time() - start_time), sep = ' ')
    g.show_start_screen()
    while True:

        g.new()
        g.run()
        g.show_end_screen()

#Si Main.py est le fichier exécuté et non un fichier importé
if __name__ == '__main__':
    main()