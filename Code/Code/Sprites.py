#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#

'''
    Lorenz Cazaubon   G1
    Paul   Mauvoisin  G1
'''

##################################################################################################################

import pygame as pg
from Settings import *
import os, random
import math


##################################################################################################################
"Creatures"
##################################################################################################################

class Creature(pg.sprite.Sprite):

    def __init__(self,group, game, x, y, name, abbrv, armor, max_hp, hp, strength_melee=6, xp=0):
        pg.sprite.Sprite.__init__(self, group)
        self.game = game
        self.x = x ; self.y = y
        self.name = name ; self.abbrv = abbrv; self.Alive = True
        self.max_hp = max_hp ; self.hp = hp
        self.strength_melee = strength_melee
        self.armor = armor
        self.xp = xp

    def idle(self):
        #change to Idle animation
        self.action = 'Idle'
        self.frame_index = 0
        self.update_time = pg.time.get_ticks()

    def hurt(self):
        #change to hurt animation
        self.action = 'Hurt'
        self.frame_index = 0
        self.update_time = pg.time.get_ticks()

    def death(self):

        self.Alive = False

        #change to death animation
        self.action = 'Death'
        self.frame_index = 0
        self.update_time = pg.time.get_ticks()

    def move(self, coord):

        dx, dy = coord
        if dx == -1:
            self.orientation = 'Left'
        elif dx == 1:
            self.orientation = 'Right'

        if self.collide_with_walls(coord):
            return False
        
        if type(self) == Player:
            self.status_update()

        if self.collide_with_mobs(coord):
            return True

        if self.collide_with_stairs(coord):
            return False

        self.collide_with_item(coord)
        self.action = 'Run'
        self.x += dx ; self.y += dy
        return True

    def collide_with_walls(self, coord=(0,0)):
        dx, dy = coord
        for element in self.game.elements:
            if type(element) == Wall:
                if element.x == self.x + dx and element.y == self.y + dy:
                    return True
        return False

    def collide_with_mobs(self, coord=(0,0)):
        dx, dy = coord
        if self.name in PLAYER:
            for mob in self.game.mobs:
                if mob.Alive and mob.x == self.x + dx and mob.y == self.y + dy:
                    self.attack(mob)
                    self.game.action_cooldown = 0
                    return True
        else:
            if self.game.player.Alive and self.game.player.x == self.x + dx and self.game.player.y == self.y + dy:
                self.attack(self.game.player)
                return True
            else:
                for mob in self.game.mobs:
                    if mob.Alive and mob.x == self.x + dx and mob.y == self.y + dy:
                        return True
        return False

    def collide_with_stairs(self, coord=(0,0)):
        dx, dy = coord
        if type(self) == Player:
            for element in self.game.elements:
                if type(element) == Stairs:
                    if element.x == self.x + dx and element.y == self.y + dy:
                        self.game.go_down()
                        return True
        return False

    def collide_with_item(self, coord=(0,0)):
        dx, dy = coord
        if type(self) == Mob:
            return False
        for item in self.game.items:
            if item.x == self.x + dx and item.y == self.y + dy:
                
                if type(item) == Gold:
                    item.kill()    
                    self.use(item)
                    return True
                else:
                    if self.to_inventory(item):
                        return True
        return False        

    def update(self):
        
        if type(self) == Player:
            GROUP = PLAYER
        else:
            GROUP = MOBS
        
        #L'image n'est pas forcément bien placée par rapport aux coo
        dx, dy = GROUP[self.name]['offset']
        self.rect.center = ((self.x) * TILESIZE + dx,(self.y) * TILESIZE + dy)

        if GROUP == MOBS:
            #Si le mob est proche du héro:
            if self.game.distance(self.game.player,self) <= PLAYER[self.game.choice]['vision']:
                self.near = True
            else:
                self.near = False
        
        #Vérifier si suffisament de temps s'est écoulé depuis la dernière MAJ
        #Si oui, alors on passe à la prochaine image dans l'animations
        if pg.time.get_ticks() - self.update_time > self.animation_cooldown:
            self.update_time = pg.time.get_ticks()
            self.frame_index += 1
        
        #Si on arrive au bout de l'animation on l'a recommence
        #ou on garde l'image skull
        skull = False
        if self.frame_index >= len(self.animation_dict[self.orientation][self.action]):               
            if self.Alive == False:
                skull = True
                #Mettre à jour l'image
                self.image = self.game.skull_img
                dx, dy = MOBS[self.name]['skull_offset']
                self.rect.center = ((self.x)) * TILESIZE + dx,((self.y) * TILESIZE + dy)
            else:
                self.idle()
        if not skull:
            #Animation
            #Mettre à jour l'image
            self.image = self.animation_dict[self.orientation][self.action][self.frame_index]

        if type(self) == Player:
            
            if self.invisible:
                self.image = self.image.copy()
                # this works on images with per pixel alpha too
                alpha = 100
                self.image.fill((255, 255, 255, alpha), None, pg.BLEND_RGBA_MULT)

class Player(Creature):
    
    def __init__(self, game, x, y, name):
        self.groups = game.all_sprites, game.player
        abbrv = PLAYER[name]['abbrv']; max_hp = hp = PLAYER[name]['max_hp']
        armor = PLAYER[name]['armor']; vision = PLAYER[name]['vision']; self.mp = PLAYER[name]['mp']
        strength_melee = PLAYER[name]['strength_melee']; strength_distance = PLAYER[name]['strength_distance']
        Creature.__init__(self, self.groups, game, x, y, name, abbrv = abbrv, max_hp=max_hp, hp=hp , strength_melee=strength_melee, armor=armor, xp=0)
        
        if strength_distance == None:
            self.strength_distance = PLAYER[self.name]['strength_distance']
        else:
            self.strength_distance = strength_distance
        
        self.invincible = False
        self.kills = self.level = self.gold = self.bonus_armor = self.bonus_strength = self.bonus_mana_regen = self.xp = self.base_strength = self.invisible_duration = self.invincible_duration = self.vision_duration = self.weapon_dmg_distance = self.strength_duration = self.weapon_dmg = self.poisoned_duration = 0
        self.invisible = False
        self.vision = vision
        self.berserk = False; self.vision_boost = False; self.poisoned = False
        if name == 'Huntress':
            arme_cac = game.wood_spear_img
        else:
            arme_cac = game.wood_sword_img

        self.inventory = []; self.equipped = {'armor': {'img': game.leather_armor_img}, 'weapon': {'img': arme_cac}, 'bow': {'img': game.green_bow_img}, 'amulette': None}
        
        #animation:
        self.animation_dict = {'Right' : {'Idle' : [], 'Attack': [], 'Run': [] }, 'Left': {'Idle' : [], 'Attack': [], 'Run': []}}
        self.animation_cooldown = PLAYER[self.name]['animation_cooldown']
        self.frame_index = 0 ; self.action = 'Idle'
        self.update_time = pg.time.get_ticks() 
        self.orientation = random.choice(['Left','Right'])
        self.vision = PLAYER[self.name]['vision']

        HERO_FOLDER = os.path.join(PLAYER_FOLDER, self.name)
        factor = PLAYER[self.name]['factor']

        for action in self.animation_dict['Right']:
            HERO_ACTION = os.path.join(HERO_FOLDER, action)

            #Nombre de fichier par dossier:
            n = len(os.listdir(HERO_ACTION))
            
            for i in range(n):
                image = pg.image.load(os.path.join(HERO_ACTION,f"{i}.png")).convert_alpha()
                image = pg.transform.scale(image,(image.get_width()*factor,image.get_height()*factor))
                
                #Pour orientation Droite
                self.animation_dict['Right'][action].append(image)

                #Pour orientation Gauche
                #On inverse l'image pour avoir une image selon les deux orientations: gauche et droite
                image = pg.transform.flip(image,True,False)         
                self.animation_dict['Left'][action].append(image)

        self.image = self.animation_dict[self.orientation][self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def attack(self, mob):

        if self.invisible:
            self.invisible = False

        self.action = 'Attack'
        self.frame_index = 0
        self.update_time = pg.time.get_ticks()

        damage = (self.strength_melee + self.base_strength + self.weapon_dmg + self.bonus_strength) * (1-((mob.armor)//150))
        mob.hp -= damage

        #si le mob est mort
        if mob.hp <= 0:
            self.kills += 1; self.mp += 10 + self.bonus_mana_regen
            if self.mp > 150:
                self.mp = 150
            self.gold += MOBS[mob.name]['gold']
            mob.death()
            
            #xp
            self.xp += mob.xp
            if self.xp > XP_TO_LEVEL_UP:
                self.xp = 0; self.level += 1
                self.hp = self.max_hp
                self.base_strength += 1
            

        #Afficher dégâts au dessus du mob
        damage_text = DamageText(self.game,mob.rect.centerx, mob.rect.y + 10, str(damage),BRIGHTRED)
        self.game.damage_text_group.add(damage_text)

    def attack_distance(self,mob,dmg=0):
        
        if self.invisible:
            self.invisible = False

        damage = (self.strength_distance + self.base_strength + dmg + self.weapon_dmg_distance + self.bonus_strength) * (1-(mob.armor//150))

        mob.hp -= damage

        #si le mob est mort
        if mob.hp <= 0:
            mob.death()
            self.kills += 1;self.mp += 10 + self.bonus_mana_regen
            if self.mp > 150:
                self.mp = 150

            #xp
            self.xp += mob.xp
            if self.xp > 150:
                self.xp = 0; self.level += 1
                self.hp = self.max_hp
                self.base_strength += 1

        #Afficher dégâts au dessus du mob
        damage_text = DamageText(self.game,mob.rect.centerx, mob.rect.y, str(damage),BRIGHTRED)
        self.game.damage_text_group.add(damage_text)

        self.game.current_player = 'Others'
    
    def use(self,item):
        if item.usage != None:
            item.usage(self)
            return True
        return False

    def heal(self,ammount):
        if self.max_hp - self.hp > ammount:
            heal_amount = ammount
        else:
            heal_amount = self.max_hp - self.hp
        self.hp += heal_amount
        self.poisoned = False

    def mana(self,ammount):
        if 150 - self.mp > ammount:
            mana_amount = ammount
        else:
            mana_amount = 150 - self.mp
        self.mp += mana_amount

    def teleport(self,game):
        cell = random.choice(list(game.map.cells.values()))
        coo = random.choice(cell.room)
        self.x, self.y = coo
        self.mp -= TP_COST
        return True

    def status_update(self):
        
        if self.invisible:
            self.invisible_duration -= 1
            if self.invisible_duration <= 0:
                self.invisible = False

        if self.invincible:
            self.invincible_duration -= 1
            if self.invincible_duration <= 0:
                self.invincible = False

        if self.vision_boost:
            self.vision_duration -=1
            if self.vision_duration <= 0:
                self.vision = PLAYER[self.name]['vision']
                self.vision_boost = False
        
        if self.berserk:
            self.strength_duration -= 1
            if self.strength_duration <= 0:
                self.strength_melee = PLAYER[self.name]['strength_melee']
                self.strength_distance = PLAYER[self.name]['strength_distance']
                self.berserk = False

        if self.poisoned:
            self.poisoned_duration -= 1; self.hp -= POISON_STRENGTH
            if self.poisoned_duration <= 0:
                self.poisoned = False

    def to_inventory(self,obj):
        if len(self.inventory) < INVENTORY_SIZE:
            self.inventory.append({'name': obj.name, 'stars': obj.stars, 'stars_color': obj.stars_color, 'img': obj.image, 'usage': obj.usage, 'val': obj.val})
            obj.kill()
            return True
        return False

class Mob(Creature):

    def __init__(self, game, x, y, name, animation_dict, abbrv, armor, xp=0):
        self.groups = game.all_sprites, game.mobs
        max_hp = hp = int(MOBS[name]['max_hp'] * (math.exp(game.level/15)))
        strength_melee = int(MOBS[name]['strength_melee'] * (math.exp(game.level/15)))
        abbrv = MOBS[name]['abbrv']
        Creature.__init__(self, self.groups, game, x, y, name, abbrv = abbrv,armor = armor, strength_melee=strength_melee, max_hp=max_hp, hp=hp, xp=xp)
        
        self.near = False

        #animation:
        self.animation_dict = animation_dict
        self.animation_cooldown = MOBS[self.name]['animation_cooldown']
        self.action = 'Idle'

        #Pour éviter que les mobs est une animation synchronisé on utilise le module random
        self.orientation = random.choice(['Left','Right'])
        self.frame_index = random.randint(0, len(self.animation_dict[self.orientation][self.action])-1)
        self.update_time = pg.time.get_ticks() + random.randint(0,self.animation_cooldown)

        self.image = self.animation_dict[self.orientation][self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        self.hitbox = pg.Rect(0,0,16,16)
        self.hitbox.center = (self.x * TILESIZE + (TILESIZE/2), self.y * TILESIZE + (TILESIZE/2))
    
    def Health_Bar_draw(self):

        #Calcul du ratio
        ratio = self.hp / self.max_hp
        dx, dy = MOBS[self.name]['Health_Bar_offset']
        x, y = self.rect.centerx + dx, self.rect.centery + dy  # -5 et -20 test
        longueur, largeur = MOBS[self.name]['Health_Bar_size']
        pg.draw.rect(self.game.screen, RED, (x, y, longueur, largeur)) # test: 12, 2.2
        pg.draw.rect(self.game.screen, GREEN, (x, y, longueur*ratio, largeur))

    def attack(self, mob):
        
        self.action = 'Attack'
        self.frame_index = 0
        self.update_time = pg.time.get_ticks()

        damage = self.strength_melee * (1-((mob.armor+mob.bonus_armor)//150))

        if mob.invincible == False:
            mob.hp -= damage
            if self.name == 'Champi':
                mob.poisoned = True
                mob.poisoned_duration = POISON_DURATION

        #si le mob est mort
        if mob.hp <= 0:
            mob.death()

##################################################################################################################
"Elements"
##################################################################################################################

class Elements(pg.sprite.Sprite):
    def __init__(self, game, x, y, img = None, animated = False, animation_list = None, animation_cooldown = None):
        self.groups = game.all_sprites, game.elements
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game; self.x = x; self.y = y; self.animated = animated
        
        if animated:
            
            #Animation
            self.frame_index = 0
            self.animation_cooldown = animation_cooldown
            self.update_time = pg.time.get_ticks()
            self.animation_list = animation_list
            self.image = self.animation_list[self.frame_index]
            
        else:
            self.image = img
        
        self.rect = pg.Rect(0,0,TILESIZE,TILESIZE)
        self.rect.topleft = (x * TILESIZE, y * TILESIZE)

    def update(self):
        
        if self.animated:
            
            #Animation
            #Mettre à jour l'image
            self.image = self.animation_list[self.frame_index]
                
            #Vérifier si suffisament de temps s'est écoulé depuis la dernière MAJ
            #Si oui, alors on passe à la prochaine image dans l'animations
            if pg.time.get_ticks() - self.update_time > self.animation_cooldown:
                self.update_time = pg.time.get_ticks()
                self.frame_index += 1
                
            #Si on arrive au bout de l'animation on l'a recommence
            if self.frame_index >= len(self.animation_list)-1:
                self.frame_index = 0

class Wall(Elements):
    def __init__(self, game, x, y):
        img = game.wall_img
        Elements.__init__(self, game, x, y, img)
    
class Stairs(Elements):
    def __init__(self, game, x, y):
        img = game.stairs_img
        Elements.__init__(self, game, x, y, img)

class Lava(Elements): 
    def __init__(self, game, x, y,animation_list, animation_cooldown = 130):
        Elements.__init__(self, game, x, y, animated = True,animation_list=animation_list, animation_cooldown = animation_cooldown)

##################################################################################################################
"Items"
##################################################################################################################

class Items(pg.sprite.Sprite):
    def __init__(self, game, x, y, img = None, animated = False, animation_list = None, usage = None, animation_cooldown = 0, name = None):
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game; self.x = x; self.y = y; self.animated = animated; self.name = name; self.usage = usage; self.reverse = False

        if animated:
            
            #Animation
            self.frame_index = 0
            self.animation_cooldown = animation_cooldown
            self.update_time = pg.time.get_ticks()
            self.animation_list = animation_list
            self.image = self.animation_list[self.frame_index]
            
        else:
            self.image = img
            self.update_time = pg.time.get_ticks()
            self.frame_index = random.randint(0,ITEM_MAX_MOV)
        
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def update(self):
        
        if self.animated:
            
            #Animation
            
                
            #Vérifier si suffisament de temps s'est écoulé depuis la dernière MAJ
            #Si oui, alors on passe à la prochaine image dans l'animations
            if pg.time.get_ticks() - self.update_time > self.animation_cooldown:
                self.update_time = pg.time.get_ticks()
                self.frame_index += 1
                
            #Si on arrive au bout de l'animation on l'a recommence
            if self.frame_index >= len(self.animation_list)-1:
                self.frame_index = 0

            #L'image n'est pas forcément bien placée par rapport aux coo
            dx, dy = ITEMS[self.name]['offset']
            self.rect.center = ((self.x) * TILESIZE + dx,(self.y) * TILESIZE + dy)

            #Mettre à jour l'image
            self.image = self.animation_list[self.frame_index]
        
        else: 
            
            if pg.time.get_ticks() - self.update_time > ITEM_REFRESH_TIME:
                self.update_time = pg.time.get_ticks()
                if not self.reverse:
                    self.frame_index += 1
                else:
                    self.frame_index -= 1
            if self.frame_index == 0:
                self.reverse = False
            elif self.frame_index == ITEM_MAX_MOV:
                self.reverse = True
            dx, dy = ITEMS[self.name]['offset']
            self.rect.center = ((self.x) * TILESIZE + dx,(self.y) * TILESIZE + dy - self.frame_index)

class Gold(Items):
    def __init__(self, game, x, y, animation_cooldown = ITEMS['Gold']['animation_cooldown']):
        animation_list = game.animation_coin_list
        Items.__init__(self, game, x, y, animated = True, animation_list = animation_list, animation_cooldown = animation_cooldown, name = 'Gold', usage =  lambda hero: hero.__setattr__('gold', hero.gold + 3))

class Armor(Items):

    def __init__(self, game, x, y, name = None):
        val = ITEMS[name]['val']
        if name == 'Leather_armor':
            image = game.leather_armor_img
        elif name == 'Iron_armor':
            image = game.iron_armor_img
        else:
            image = game.golden_armor_img
        k = random.expovariate(1/game.level)
        if k >= 3:
            k = 3
        elif 2<=k<3:
            k = 2
        elif 1<=k<2:
            k = 1
        else:
            k = 0
        self.stars = k
        n = random.randint(1,10)
        if n <= 3:
            self.stars_color = 'Gold'
            bonus = 0.15
        else:
            self.stars_color = 'Silver'
            bonus = 0.1
        self.armor = int(val * (1 + (self.stars * bonus)))
        self.val = self.armor
        Items.__init__(self, game, x, y, img = image, usage = lambda hero: hero.__setattr__('armor',self.armor), name = name)

class Weapon(Items):
    def __init__(self, game, x, y, name = None):
        val = ITEMS[name]['val']
        if name == 'Wood_sword':
            image = game.wood_sword_img
        elif name == 'Iron_sword':
            image = game.iron_sword_img
        elif name == 'Golden_sword':
            image = game.golden_sword_img
        elif name == 'Wood_spear':
            image = game.wood_spear_img
        elif name == 'Iron_spear':
            image = game.iron_spear_img
        elif name == 'Gold_spear':
            image = game.golden_spear_img
        elif name == 'Green_bow':
            image = game.green_bow_img
        elif name == 'Red_bow':
            image = game.red_bow_img
        else:
            image = game.golden_bow_img
        k = random.expovariate(1/game.level)
        if k >= 3:
            k = 3
        elif 2<=k<3:
            k = 2
        elif 1<=k<2:
            k = 1
        else:
            k = 0
        self.stars = k
        n = random.randint(1,10)
        if n <= 3:
            self.stars_color = 'Gold'
            bonus = 0.15
        else:
            self.stars_color = 'Silver'
            bonus = 0.1
        self.dmg = int(val * (1 + (self.stars * bonus)))
        self.val = self.dmg
        if 'bow' in name:
            usage = lambda hero: hero.__setattr__('weapon_dmg_distance',self.dmg)
        else:
            usage = lambda hero: hero.__setattr__('weapon_dmg',self.dmg)
        Items.__init__(self, game, x, y, img = image, usage = usage , name = name)

class Potion(Items):

    def __init__(self, game, x, y, name = None):
        
        k = random.expovariate(1/game.level)
        if k >= 3:
            k = 3
        elif 2<=k<3:
            k = 2
        elif 1<=k<2:
            k = 1
        else:
            k = 0
        self.stars = k
        n = random.randint(1,10)
        if n <= 3:
            self.stars_color = 'Gold'
            bonus = 0.2
        else:
            self.stars_color = 'Silver'
            bonus = 0.15
        
        val = ITEMS[name]['val']
        self.val = int(val * (1 + (self.stars * bonus)))
        if 'Mana' in name:
            usage = lambda hero: hero.mana(val)
            if self.stars == 0:
                image = game.mana_img_list[self.stars]
            else:
                image = game.mana_img_list[self.stars-1]
            
        else:
            usage = lambda hero: hero.heal(val)
            if self.stars == 0:
                image = game.hp_img_list[self.stars]
            else:
                image = game.hp_img_list[self.stars-1]

        Items.__init__(self, game, x, y, img = image, usage = usage, name = name)

class Amulette(Items):

    def __init__(self, game, x, y, name = None):
        
        k = random.expovariate(1/game.level)
        if k >= 3:
            k = 3
        elif 2<=k<3:
            k = 2
        elif 1<=k<2:
            k = 1
        else:
            k = 0
        self.stars = k
        n = random.randint(1,10)
        if n <= 3:
            self.stars_color = 'Gold'
            bonus = 0.2
        else:
            self.stars_color = 'Silver'
            bonus = 0.15
        
        val = ITEMS[name]['val']
        self.val = int(val * (1 + (self.stars * bonus)))

        if 'rouge' in name:
            image = game.amulette_rouge_img
            usage = lambda hero: hero.__setattr__('bonus_strength',val)
        elif 'orange' in name:
            image = game.amulette_orange_img
            usage = lambda hero: hero.__setattr__('bonus_armor',val)
        else:
            image = game.amulette_bleue_img
            usage = lambda hero: hero.__setattr__('bonus_mana_regen',val)
        Items.__init__(self, game, x, y, img = image, usage = usage, name = name)

##################################################################################################################
"Magic and Projectiles"
##################################################################################################################

class Projectile(pg.sprite.Sprite):

    def __init__(self, game, player, mob, speed, dmg, animated = False, animation_list = None, img = None, offset = (0,0)):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game; self.dmg = dmg; self.animated = animated
        self.distance = self.game.distance(player,mob)
        self.target = pg.Rect(0,0,20,20)
        self.target.center = (mob.x * TILESIZE + (TILESIZE / 2), mob.y * TILESIZE + (TILESIZE / 2))
        self.x = player.x; self.y = player.y
        self.player = player
        self.mob = mob
        x1, y1 = player.x, player.y
        x2, y2 = mob.x, mob.y
        #Pas pour chaque refresh
        self.dx = (x2 - x1) / (self.distance * speed); self.dy = (y2 - y1) / (self.distance * speed)

        #Angle pour avoir le projectile orienté vers la cible
        if self.dx == 0:
            if y1 > y2:
                angle = 90
            else:
                angle = -90
        elif self.dy == 0:
            if x1 > x2:
                angle = 180
            else: angle = 0
        else:
            if x1 > x2:
                val = 180
            else:
                val = 0
            angle = -1 * math.degrees(math.atan(self.dy/self.dx)) + val
        self.angle = angle

        if animated:
            #Animation
            self.frame_index = 0
            self.animation_cooldown = 5
            self.update_time = pg.time.get_ticks()
            self.spawn_time = pg.time.get_ticks()
            self.animation_list = animation_list
            self.image = pg.transform.rotozoom(self.animation_list[self.frame_index],angle,1)
        else:
            self.image = pg.transform.rotozoom(img,angle,1)

        self.rect = self.image.get_rect()
        x1, y1 = offset
        self.rect.x = self.x * TILESIZE + x1
        self.rect.y = self.y * TILESIZE + x2
        self.hitbox = Hitbox(4,self.x * TILESIZE, self.y * TILESIZE)

    def update(self):
        
        self.x += self.dx
        self.y += self.dy
        self.rect.center = (self.x * TILESIZE + (TILESIZE/2), self.y * TILESIZE + (TILESIZE/2))
        self.hitbox.rect.center = (self.x * TILESIZE + (TILESIZE/2), self.y * TILESIZE + (TILESIZE/2))

        #Rencontre avec un mur par exemple
        if pg.sprite.spritecollideany(self.hitbox, self.game.elements):
            self.game.current_player = 'Others'
            self.player.status_update()
            self.kill()

        #Un autre mob est sur le chemin
        obj = pg.sprite.spritecollideany(self.hitbox, self.game.mobs)
        if obj != None and obj != self.mob and obj.Alive:
            self.player.attack_distance(obj, dmg = self.dmg)
            self.player.status_update()
            self.kill()

        #On atteint la cible
        if collision(self.hitbox.rect,self.target):
            self.player.attack_distance(self.mob, dmg = self.dmg)
            self.player.status_update()
            self.kill()

        if self.animated:
            
            #Animation    
            #Vérifier si suffisament de temps s'est écoulé depuis la dernière MAJ
            #Si oui, alors on passe à la prochaine image dans l'animations
            if pg.time.get_ticks() - self.update_time > self.animation_cooldown:
                self.update_time = pg.time.get_ticks()
                self.frame_index += 1
                    
            #Si on arrive au bout de l'animation on l'a recommence
            if self.frame_index >= len(self.animation_list)-1:
                self.frame_index = 0

            #Mettre à jour l'image
            self.image = pg.transform.rotozoom(self.animation_list[self.frame_index],self.angle,1)

class FireBall(Projectile):
    
    def __init__(self, game, player, mob):
        Projectile.__init__(self, game, player, mob, speed = FIREBALL_SPEED, dmg = FIREBALL_DAMAGE, animated = True, animation_list = game.animation_fireball_list)

class Arrow(Projectile):

    def __init__(self, game, player, mob):
        Projectile.__init__(self, game, player, mob, speed = ARROW_SPEED, dmg = ARROW_DAMAGE, animated = False, img = game.arrow_img)

##################################################################################################################
"Others"
##################################################################################################################
class DamageText(pg.sprite.Sprite):
    
    def __init__(self, game, x, y, damage, color):
        self.groups = game.damage_text_group
        pg.sprite.Sprite.__init__(self,self.groups)
        self.image = game.damage_font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):

        #Bouger le texte vers le haut
        self.rect.y -= 0.01

        #Le supprimer après un certain temps
        self.counter += 1
        if self.counter > 20:
            self.kill()

class Hitbox(pg.sprite.Sprite):
    def __init__(self,size,x,y):
        pg.sprite.Sprite.__init__(self)
        self.rect = pg.Rect(0,0,size,size); self.x = x; self.y = y
        self.rect.center = (self.x * TILESIZE + (TILESIZE/2), self.y * TILESIZE + (TILESIZE/2))

def collision(rectA, rectB):

    if rectB.right < rectA.left:
        return False
    if rectB.bottom < rectA.top:
        return False
    if rectB.left > rectA.right:
        return False
    if rectB.top > rectA.bottom:
        return False
    return True