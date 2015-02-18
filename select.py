import pygame,os
from pygame.locals import *

from constants import *
from music import *

class Select():
    def initScreenSurfaces(self):
        self.screen = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
        
    def initImages(self):
        self.bg = pygame.image.load(os.path.join('Visuals','select.png')).convert()
        self.bgRect = self.bg.get_rect()

    def __init__(self):
        pygame.init()

        self.initScreenSurfaces()
        self.initImages()

        self.select = 'normal'

        self.normalRect = Rect(0,495,200,25)
        self.AIRect = Rect(0,517,200,25)

        self.normalRect.centerx = self.bgRect.centerx
        self.AIRect.centerx = self.bgRect.centerx

        self.playMusic = True

        self.clock = pygame.time.Clock()

        self.running = True

    def eventHandle(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False

            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    CORELLI.fadeout(200)
                    DECISION.play()
                    if self.select == 'normal':
                        return 'round'
                    elif self.select == 'AI':
                        return 'roundAI'

                elif event.key == K_UP:
                    self.select = 'normal'

                elif event.key == K_DOWN:
                    self.select = 'AI'

    def drawSelect(self):
        if self.select == 'normal':
            pygame.draw.rect(self.screen,FLONNEBLUE,self.normalRect,3)

        elif self.select == 'AI':
            pygame.draw.rect(self.screen,FLONNEBLUE,self.AIRect,3)

    def run(self):
        if self.playMusic == True:
            CORELLI.play(-1)
            self.playMusic = False

        mode = self.eventHandle()
        if mode == 'round' or mode == 'roundAI':
            return mode

        self.screen.blit(self.bg,(0,0))
        self.drawSelect()

        pygame.display.update()
        self.clock.tick(FPS)
        if not self.running:
            pygame.quit()
