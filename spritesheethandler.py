import pygame,os

from constants import *

class SpriteSheet(object):
    def __init__(self,fileName,colorKey): 
        pathname = os.path.join('Visuals',fileName)
        self.spriteSheet = pygame.image.load(pathname).convert()
        self.colorKey = colorKey

    def getSprite(self,x,y,width,height,flip=False):
        sprite = pygame.Surface((width,height))
        sprite.blit(self.spriteSheet,(0,0),(x,y,width,height))
        sprite.set_colorkey(self.colorKey)

        if flip == True:
            return pygame.transform.flip(sprite,True,False)

        return sprite