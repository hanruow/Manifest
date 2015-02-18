import pygame,os
from constants import *

class Weapon(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.isEquipped = False

class Knife(Weapon):
    def __init__(self,x=0,y=0):
        super(Knife,self).__init__(x,y)

        pathname = os.path.join('Visuals/Weapons','knife.png')
        self.image = pygame.image.load(pathname).convert_alpha()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.range = 40
        self.dmg = 0.3

    def __str__(self):
        return 'knife'

class Saber(Weapon):
    def __init__(self,x=0,y=0):
        super(Saber,self).__init__(x,y)
        
        pathname = os.path.join('Visuals/Weapons','saber.png')
        self.image = pygame.image.load(pathname).convert_alpha()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.range = 80
        self.dmg = 0.5

    def __str__(self):
        return 'saber'

class Axe(Weapon):
    def __init__(self,x=0,y=0):
        super(Axe,self).__init__(x,y)
        
        pathname = os.path.join('Visuals/Weapons','axe.png')
        self.image = pygame.image.load(pathname).convert_alpha()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.range = 60
        self.dmg = 0.6

    def __str__(self):
        return 'axe'

