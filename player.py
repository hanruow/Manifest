import pygame,time,random
from spritesheethandler import *
from pyganim import *
from constants import *
from weapon import *

class Player(object):
    def __init__(self,playerNo):
        super(Player,self).__init__()
        self.state = 'idle'

        if playerNo == 1:
            self.x = 100 #top left of sprite
            self.dir = 'right'

        elif playerNo == 2:
            self.x = 800
            self.dir = 'left'

        self.y = 400

        self.speed = 7
        self.diagSpeed = (self.speed)*((2**0.5)/2)

        self.stateTime = 0

        self.weapon = 'fist'

    def setState(self,state):
        if self.state != state:
            self.stateTime = time.time()
            self.state = state

    def getState(self):
        dTime = time.time() - self.stateTime
        return (dTime,self.state)

    def moveHandler(self):
        if self.state == 'moveup':
            self.rect.y -= self.speed

        elif self.state == 'movedown':
            self.rect.y += self.speed

        elif self.state == 'moveleft':
            self.dir = 'left'
            self.rect.x -= self.speed

        elif self.state == 'moveright':
            self.dir = 'right'
            self.rect.x += self.speed

        elif self.state == 'moveupleft':
            self.dir = 'left'
            self.rect.x -= self.diagSpeed
            self.rect.y -= self.diagSpeed

        elif self.state == 'moveupright':
            self.dir = 'right'
            self.rect.x += self.diagSpeed
            self.rect.y -= self.diagSpeed

        elif self.state == 'movedownleft':
            self.dir = 'left'
            self.rect.x -= self.diagSpeed
            self.rect.y += self.diagSpeed

        elif self.state == 'movedownright':
            self.dir = 'right'
            self.rect.x += self.diagSpeed
            self.rect.y += self.diagSpeed

        #clamp
        if self.rect.x < 0:
            self.rect.x = 0

        if self.rect.bottom < WINDOWHEIGHT*(7.0/8):
            self.rect.bottom = WINDOWHEIGHT*(7.0/8)

        if self.rect.x + self.width > WINDOWWIDTH:
            self.rect.x = WINDOWWIDTH - self.width

        if self.rect.y + self.height > WINDOWHEIGHT:
            self.rect.y = WINDOWHEIGHT - self.height - 5

    def changeHp(self,dHp):
        self.hp += dHp

        if self.hp > 100:
            self.hp = 100

        if self.hp < 0:
            self.hp = 0

class Flonne(Player):
    def __init__(self,playerNo):
        super(Flonne,self).__init__(playerNo)
        self.name = 'Flonne'
        self.color = FLONNEBLUE
        self.spriteSheet = SpriteSheet('flonne.png', FLONNECOLORKEY)
        self.portrait = pygame.image.load(os.path.join('Visuals','flonneportrait.png')).convert_alpha()
        
        if playerNo == 1:
            self.portrait = pygame.transform.flip(self.portrait,True,False)

        self.portraitRect = self.portrait.get_rect()

        self.width = 100
        self.height = 200
        self.speed = 7
        self.diagSpeed = (self.speed)*((2**0.5)/2)
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)

        self.hp = 100
        self.atk = 0.2
        self.defn = 3
        self.range = 5

        self.idleFrameTime = 0.15
        self.walkFrameTime = 0.12
        self.flinchFrameTime = 0.1
        self.fistFrameTime = 0.15
        self.knifeFrameTime = 0.15
        self.saberFrameTime = 0.17
        self.axeFrameTime = 0.17

        self.flinchTotalTime = 0.1
        self.fistTotalTime = self.fistFrameTime*3.5
        self.knifeTotalTime = self.knifeFrameTime*3.5
        self.saberTotalTime = self.saberFrameTime*3.5
        self.axeTotalTime = self.axeFrameTime*3.5

        self.attackTotalTime = self.fistTotalTime

        self.initIdleAnim()
        self.initWalkAnim()
        self.initFlinchAnim()
        self.initFistAnim()
        self.initKnifeAnim()
        self.initSaberAnim()
        self.initAxeAnim()
        self.initWinLoseAnim()

        self.moveconductor = PygConductor([self.idleAnimL,self.idleAnimR,
                                       self.walkAnimL,self.walkAnimR])
        self.flinchconductor = PygConductor([self.flinchAnimL,self.flinchAnimR])
        self.attackconductor = PygConductor([self.fistAnimL,self.fistAnimR,
                                             self.knifeAnimL,self.knifeAnimR,
                                             self.saberAnimL,self.saberAnimR,
                                             self.axeAnimL,self.axeAnimR])
        self.winconductor = PygConductor([self.winAnimL,self.winAnimR])
        self.loseconductor = PygConductor([self.loseAnimL,self.loseAnimR])

    def initIdleAnim(self):
        s = self.idleFrameTime

        l1 = self.spriteSheet.getSprite(0,0,100,200)
        l2 = self.spriteSheet.getSprite(100,0,100,200)
        l3 = self.spriteSheet.getSprite(200,0,100,200)
        l4 = self.spriteSheet.getSprite(300,0,100,200)
        l5 = self.spriteSheet.getSprite(400,0,100,200)
        l6 = self.spriteSheet.getSprite(500,0,100,200)

        leftAnimList = [(l1,s),(l2,s),(l3,s),(l4,s),(l5,s),(l6,s),
                        (l5,s),(l4,s),(l3,s),(l2,s),(l1,s)]
        self.idleAnimL = PygAnimation(leftAnimList, loop=False)

        r1 = pygame.transform.flip(l1,True,False)
        r2 = pygame.transform.flip(l2,True,False)
        r3 = pygame.transform.flip(l3,True,False)
        r4 = pygame.transform.flip(l4,True,False)
        r5 = pygame.transform.flip(l5,True,False)
        r6 = pygame.transform.flip(l6,True,False)

        rightAnimList = [(r1,s),(r2,s),(r3,s),(r4,s),(r5,s),(r6,s),
                        (r5,s),(r4,s),(r3,s),(r2,s),(r1,s)]
        self.idleAnimR = PygAnimation(rightAnimList, loop=False)

    def initWalkAnim(self):
        s = self.walkFrameTime

        l1 = self.spriteSheet.getSprite(0,200,100,200)
        l2 = self.spriteSheet.getSprite(100,200,100,200)
        l3 = self.spriteSheet.getSprite(200,200,100,200)
        l4 = self.spriteSheet.getSprite(300,200,100,200)
        l5 = self.spriteSheet.getSprite(400,200,100,200)
        l6 = self.spriteSheet.getSprite(500,200,100,200)

        leftAnimList = [(l1,s),(l2,s),(l3,s),(l4,s),(l5,s),(l6,s)]
        self.walkAnimL = PygAnimation(leftAnimList)

        r1 = pygame.transform.flip(l1,True,False)
        r2 = pygame.transform.flip(l2,True,False)
        r3 = pygame.transform.flip(l3,True,False)
        r4 = pygame.transform.flip(l4,True,False)
        r5 = pygame.transform.flip(l5,True,False)
        r6 = pygame.transform.flip(l6,True,False)

        rightAnimList = [(r1,s),(r2,s),(r3,s),(r4,s),(r5,s),(r6,s)]
        self.walkAnimR = PygAnimation(rightAnimList)

    def initFlinchAnim(self):
        s = self.flinchFrameTime

        l1 = self.spriteSheet.getSprite(600,0,100,200)

        leftAnimList = [(l1,s)]
        self.flinchAnimL = PygAnimation(leftAnimList)

        r1 = pygame.transform.flip(l1,True,False)

        rightAnimList = [(r1,s)]
        self.flinchAnimR = PygAnimation(rightAnimList)

    def initFistAnim(self):
        s = self.fistFrameTime

        l1 = self.spriteSheet.getSprite(0,400,100,200)
        l2 = self.spriteSheet.getSprite(100,400,100,200)
        l3 = self.spriteSheet.getSprite(200,400,100,200)
        l4 = self.spriteSheet.getSprite(300,400,100,200)

        leftAnimList = [(l1,s),(l2,s),(l3,s),(l4,s)]
        self.fistAnimL = PygAnimation(leftAnimList)

        r1 = pygame.transform.flip(l1,True,False)
        r2 = pygame.transform.flip(l2,True,False)
        r3 = pygame.transform.flip(l3,True,False)
        r4 = pygame.transform.flip(l4,True,False)

        rightAnimList = [(r1,s),(r2,s),(r3,s),(r4,s)]
        self.fistAnimR = PygAnimation(rightAnimList)

    def initKnifeAnim(self):
        s = self.knifeFrameTime

        l1 = self.spriteSheet.getSprite(0,600,100,200)
        l2 = self.spriteSheet.getSprite(100,600,100,200)
        l3 = self.spriteSheet.getSprite(200,600,150,200)
        l4 = self.spriteSheet.getSprite(350,600,150,200)

        leftAnimList = [(l1,s),(l2,s),(l3,s),(l4,s)]
        self.knifeAnimL = PygAnimation(leftAnimList)

        r1 = pygame.transform.flip(l1,True,False)
        r2 = pygame.transform.flip(l2,True,False)
        r3 = pygame.transform.flip(l3,True,False)
        r4 = pygame.transform.flip(l4,True,False)

        rightAnimList = [(r1,s),(r2,s),(r3,s),(r4,s)]
        self.knifeAnimR = PygAnimation(rightAnimList)

    def initSaberAnim(self):
        s = self.saberFrameTime

        l1 = self.spriteSheet.getSprite(0,800,150,200)
        l2 = self.spriteSheet.getSprite(150,800,150,200)
        l3 = self.spriteSheet.getSprite(300,800,150,200)
        l4 = self.spriteSheet.getSprite(450,800,150,200)

        leftAnimList = [(l1,s),(l2,s),(l3,s),(l4,s)]
        self.saberAnimL = PygAnimation(leftAnimList)

        r1 = pygame.transform.flip(l1,True,False)
        r2 = pygame.transform.flip(l2,True,False)
        r3 = pygame.transform.flip(l3,True,False)
        r4 = pygame.transform.flip(l4,True,False)

        rightAnimList = [(r1,s),(r2,s),(r3,s),(r4,s)]
        self.saberAnimR = PygAnimation(rightAnimList)

    def initAxeAnim(self):
        s = self.axeFrameTime

        l1 = self.spriteSheet.getSprite(0,1400,150,200)
        l2 = self.spriteSheet.getSprite(150,1400,150,200)
        l3 = self.spriteSheet.getSprite(300,1400,200,200)
        l4 = self.spriteSheet.getSprite(500,1400,200,200)

        leftAnimList = [(l1,s),(l2,s),(l3,s),(l4,s)]
        self.axeAnimL = PygAnimation(leftAnimList)

        r1 = pygame.transform.flip(l1,True,False)
        r2 = pygame.transform.flip(l2,True,False)
        r3 = pygame.transform.flip(l3,True,False)
        r4 = pygame.transform.flip(l4,True,False)

        rightAnimList = [(r1,s),(r2,s),(r3,s),(r4,s)]
        self.axeAnimR = PygAnimation(rightAnimList)

    def initWinLoseAnim(self):
        s = self.idleFrameTime

        #win
        l1 = self.spriteSheet.getSprite(400,400,100,200)

        leftAnimList = [(l1,s)]
        self.winAnimL = PygAnimation(leftAnimList)

        r1 = pygame.transform.flip(l1,True,False)
        
        rightAnimList = [(r1,s)]
        self.winAnimR = PygAnimation(rightAnimList)

        #lose
        l1 = self.spriteSheet.getSprite(500,400,100,200)
        
        leftAnimList = [(l1,s)]
        self.loseAnimL = PygAnimation(leftAnimList)

        r1 = pygame.transform.flip(l1,True,False)
        
        rightAnimList = [(r1,s)]
        self.loseAnimR = PygAnimation(rightAnimList)

class FlonneAI(Flonne):

    @staticmethod
    def chance(chance):
        chance = chance % 101
        if random.randint(0,100) < chance:
            return True
        return False

    def __init__(self,playerNo):
        super(FlonneAI,self).__init__(playerNo)

    def getDistance(self,other):
        return (((self.rect.centerx - other.rect.centerx)**2 + 
                 (self.rect.centery - other.rect.centery)**2)**0.5)

    def attack(self,other):
        if FlonneAI.chance(25): 
            self.state = 'attack'

        elif FlonneAI.chance(5) and self.rect.x < other.rect.x:
            self.state = 'moveleft'

        elif FlonneAI.chance(5): self.state = 'moveright'

    def approach(self,other):
        dist = self.getDistance(other)
        error = 5

        if isinstance(other,Plenair):

            if dist > self.range/2 + self.rect.width/2:
                if self.rect.centerx > other.rect.centerx + error:
                    self.state = 'moveleft'

                elif self.rect.centerx < other.rect.centerx - error:
                    self.state = 'moveright'

                if self.rect.centery > other.rect.centery + error:
                    self.state = 'moveup'

                elif self.rect.centery < other.rect.centery - error:
                    self.state = 'movedown'

                return False
            return True

        else:
            (x,y) = self.rect.midbottom
            if dist > self.rect.height/2 + error:
                if x > other.rect.centerx:
                    self.state = 'moveleft'
                else: self.state = 'moveright'

                if y < other.rect.top:
                    self.state = 'movedown'

                return False
            return True
                    
class Plenair(Player):
    def __init__(self,playerNo):
        super(Plenair,self).__init__(playerNo)
        self.name = 'Plenair'
        self.color = PLENAIRRED
        self.spriteSheet = SpriteSheet('plenair.png',PLENAIRCOLORKEY)
        self.portrait = pygame.image.load(os.path.join('Visuals','plenairportrait.png')).convert_alpha()
        
        if playerNo == 1:
            self.portrait = pygame.transform.flip(self.portrait,True,False)

        self.portraitRect = self.portrait.get_rect()

        self.width = 100
        self.height = 200
        self.speed = 7
        self.diagSpeed = (self.speed)*((2**0.5)/2)
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)

        self.hp = 100
        self.atk = 0.2
        self.defn = 3
        self.range = 5

        self.idleFrameTime = 0.15
        self.walkFrameTime = 0.12
        self.flinchFrameTime = 0.1
        self.fistFrameTime = 0.15
        self.knifeFrameTime = 0.15
        self.saberFrameTime = 0.17
        self.axeFrameTime = 0.17

        self.flinchTotalTime = 0.1
        self.fistTotalTime = self.fistFrameTime*3.5
        self.knifeTotalTime = self.knifeFrameTime*3.5
        self.saberTotalTime = self.saberFrameTime*3.5
        self.axeTotalTime = self.axeFrameTime*3.5

        self.attackTotalTime = self.fistTotalTime

        self.initIdleAnim()
        self.initWalkAnim()
        self.initFlinchAnim()
        self.initFistAnim()
        self.initKnifeAnim()
        self.initSaberAnim()
        self.initAxeAnim()
        self.initWinLoseAnim()

        self.moveconductor = PygConductor([self.idleAnimL,self.idleAnimR,
                                       self.walkAnimL,self.walkAnimR])
        self.attackconductor = PygConductor([self.fistAnimL,self.fistAnimR,
                                             self.knifeAnimL,self.knifeAnimR,
                                             self.saberAnimL,self.saberAnimR,
                                             self.axeAnimL,self.axeAnimR])
        self.flinchconductor = PygConductor([self.flinchAnimL,self.flinchAnimR])
        self.winconductor = PygConductor([self.winAnimL,self.winAnimR])
        self.loseconductor = PygConductor([self.loseAnimL,self.loseAnimR])

    def initIdleAnim(self):
        s = self.idleFrameTime

        l1 = self.spriteSheet.getSprite(0,0,100,200)
        l2 = self.spriteSheet.getSprite(100,0,100,200)
        l3 = self.spriteSheet.getSprite(200,0,100,200)
        l4 = self.spriteSheet.getSprite(300,0,100,200)

        leftAnimList = [(l1,s),(l2,s),(l3,s),(l4,s),(l3,s),(l2,s),(l1,s)]
        self.idleAnimL = PygAnimation(leftAnimList, loop=False)

        r1 = pygame.transform.flip(l1,True,False)
        r2 = pygame.transform.flip(l2,True,False)
        r3 = pygame.transform.flip(l3,True,False)
        r4 = pygame.transform.flip(l4,True,False)

        rightAnimList = [(r1,s),(r2,s),(r3,s),(r4,s),(r3,s),(r2,s),(r1,s)]
        self.idleAnimR = PygAnimation(rightAnimList, loop=False)

    def initWalkAnim(self):
        s = self.walkFrameTime

        l1 = self.spriteSheet.getSprite(0,200,100,200)
        l2 = self.spriteSheet.getSprite(100,200,100,200)
        l3 = self.spriteSheet.getSprite(200,200,100,200)
        l4 = self.spriteSheet.getSprite(300,200,100,200)
        l5 = self.spriteSheet.getSprite(400,200,100,200)
        l6 = self.spriteSheet.getSprite(500,200,100,200)

        leftAnimList = [(l1,s),(l2,s),(l3,s),(l4,s),(l5,s),(l6,s)]
        self.walkAnimL = PygAnimation(leftAnimList)

        r1 = pygame.transform.flip(l1,True,False)
        r2 = pygame.transform.flip(l2,True,False)
        r3 = pygame.transform.flip(l3,True,False)
        r4 = pygame.transform.flip(l4,True,False)
        r5 = pygame.transform.flip(l5,True,False)
        r6 = pygame.transform.flip(l6,True,False)

        rightAnimList = [(r1,s),(r2,s),(r3,s),(r4,s),(r5,s),(r6,s)]
        self.walkAnimR = PygAnimation(rightAnimList)

    def initFlinchAnim(self):
        s = self.flinchFrameTime

        l1 = self.spriteSheet.getSprite(400,0,100,200)

        leftAnimList = [(l1,s)]
        self.flinchAnimL = PygAnimation(leftAnimList)

        r1 = pygame.transform.flip(l1,True,False)

        rightAnimList = [(r1,s)]
        self.flinchAnimR = PygAnimation(rightAnimList)

    def initFistAnim(self):
        s = self.fistFrameTime

        l1 = self.spriteSheet.getSprite(0,400,100,200)
        l2 = self.spriteSheet.getSprite(100,400,100,200)
        l3 = self.spriteSheet.getSprite(200,400,100,200)
        l4 = self.spriteSheet.getSprite(300,400,100,200)

        leftAnimList = [(l1,s),(l2,s),(l3,s),(l4,s)]
        self.fistAnimL = PygAnimation(leftAnimList)

        r1 = pygame.transform.flip(l1,True,False)
        r2 = pygame.transform.flip(l2,True,False)
        r3 = pygame.transform.flip(l3,True,False)
        r4 = pygame.transform.flip(l4,True,False)

        rightAnimList = [(r1,s),(r2,s),(r3,s),(r4,s)]
        self.fistAnimR = PygAnimation(rightAnimList)

    def initKnifeAnim(self):
        s = self.knifeFrameTime

        l1 = self.spriteSheet.getSprite(0,600,100,200)
        l2 = self.spriteSheet.getSprite(100,600,100,200)
        l3 = self.spriteSheet.getSprite(200,600,150,200)
        l4 = self.spriteSheet.getSprite(350,600,150,200)

        leftAnimList = [(l1,s),(l2,s),(l3,s),(l4,s)]
        self.knifeAnimL = PygAnimation(leftAnimList)

        r1 = pygame.transform.flip(l1,True,False)
        r2 = pygame.transform.flip(l2,True,False)
        r3 = pygame.transform.flip(l3,True,False)
        r4 = pygame.transform.flip(l4,True,False)

        rightAnimList = [(r1,s),(r2,s),(r3,s),(r4,s)]
        self.knifeAnimR = PygAnimation(rightAnimList)

    def initSaberAnim(self):
        s = self.saberFrameTime

        l1 = self.spriteSheet.getSprite(0,800,150,200)
        l2 = self.spriteSheet.getSprite(150,800,150,200)
        l3 = self.spriteSheet.getSprite(300,800,150,200)
        l4 = self.spriteSheet.getSprite(450,800,150,200)

        leftAnimList = [(l1,s),(l2,s),(l3,s),(l4,s)]
        self.saberAnimL = PygAnimation(leftAnimList)

        r1 = pygame.transform.flip(l1,True,False)
        r2 = pygame.transform.flip(l2,True,False)
        r3 = pygame.transform.flip(l3,True,False)
        r4 = pygame.transform.flip(l4,True,False)

        rightAnimList = [(r1,s),(r2,s),(r3,s),(r4,s)]
        self.saberAnimR = PygAnimation(rightAnimList)

    def initAxeAnim(self):
        s = self.axeFrameTime

        l1 = self.spriteSheet.getSprite(0,1400,150,200)
        l2 = self.spriteSheet.getSprite(150,1400,150,200)
        l3 = self.spriteSheet.getSprite(300,1400,150,200)
        l4 = self.spriteSheet.getSprite(450,1400,150,200)

        leftAnimList = [(l1,s),(l2,s),(l3,s),(l4,s)]
        self.axeAnimL = PygAnimation(leftAnimList)

        r1 = pygame.transform.flip(l1,True,False)
        r2 = pygame.transform.flip(l2,True,False)
        r3 = pygame.transform.flip(l3,True,False)
        r4 = pygame.transform.flip(l4,True,False)

        rightAnimList = [(r1,s),(r2,s),(r3,s),(r4,s)]
        self.axeAnimR = PygAnimation(rightAnimList)

    def initWinLoseAnim(self):
        s = self.idleFrameTime

        #win
        l1 = self.spriteSheet.getSprite(500,0,100,200)

        leftAnimList = [(l1,s)]
        self.winAnimL = PygAnimation(leftAnimList)

        r1 = pygame.transform.flip(l1,True,False)
        
        rightAnimList = [(r1,s)]
        self.winAnimR = PygAnimation(rightAnimList)

        #lose
        l1 = self.spriteSheet.getSprite(600,0,100,200)
        
        leftAnimList = [(l1,s)]
        self.loseAnimL = PygAnimation(leftAnimList)

        r1 = pygame.transform.flip(l1,True,False)
        
        rightAnimList = [(r1,s)]
        self.loseAnimR = PygAnimation(rightAnimList)
