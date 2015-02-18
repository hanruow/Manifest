import pygame,os
from pygame.locals import *

from constants import *
from music import *

class Splash():
    def initScreenSurfaces(self):
        self.screen = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
        
    def initImages(self):
        self.bg = pygame.image.load(os.path.join('Visuals','splash2.jpg')).convert()

    def initFont(self):
        self.introFont = pygame.font.SysFont('arial',20)

    def __init__(self):
        pygame.init()

        self.initScreenSurfaces()
        self.initImages()
        self.initFont()

        self.bgRect = self.bg.get_rect()

        self.introText = self.introFont.render("Press Enter to begin",True,WHITE)
        self.introTextRect = self.introText.get_rect()
        self.introTextRect.centerx = self.bgRect.centerx
        self.introTextRect.y = WINDOWHEIGHT*(5.0/6)


        self.playMusic = True
        self.clock = pygame.time.Clock()

        self.running = True

    def eventHandle(self):
        if self.playMusic == True:
            LILIUM.play(-1)
            self.playMusic = False

        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False

            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    DECISION.play()
                    LILIUM.fadeout(200)
                    return 'select'

    def run(self):
        mode = self.eventHandle()
        if mode == 'select':
            return mode

        self.screen.blit(self.bg,(0,0))
        self.screen.blit(self.introText,self.introTextRect)

        pygame.display.update()
        self.clock.tick(FPS)
        if not self.running:
            pygame.quit()
