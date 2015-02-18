import pygame,sys,pyganim,string,os,random
from pygame.locals import *

from constants import *
from player import *
from weapon import *
from shiritori import *
from music import *

class Round(object):
    def initScreenSurfaces(self):
        self.screen = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
        self.P1SURFACE = pygame.Surface((WINDOWWIDTH,WINDOWHEIGHT)).convert()
        self.P2SURFACE = pygame.Surface((WINDOWWIDTH,WINDOWHEIGHT)).convert()

    def initBackground(self):
        bg1 = pygame.image.load(os.path.join('Visuals','background.jpg')).convert()
        bg2 = pygame.image.load(os.path.join('Visuals','background2.jpg')).convert()
        bg3 = pygame.image.load(os.path.join('Visuals','background3.jpg')).convert()
        return random.choice([bg1,bg2,bg3])

    def initImages(self):
        self.bg = self.initBackground()
        self.bgRect = self.bg.get_rect()

        self.entryField = pygame.image.load(os.path.join('Visuals','entryField4.jpg'))
        self.entryFieldRect = self.entryField.get_rect()
        self.entryFieldRect.center = self.bgRect.center

        self.plenairwin = pygame.image.load(os.path.join('Visuals','plenairwin.png')).convert()
        self.flonnewin = pygame.image.load(os.path.join('Visuals','flonnewin.png')).convert()
        self.winRect = self.plenairwin.get_rect()
        self.winRect.center = self.bgRect.center

    def initFont(self):
        self.turnTimeLeftFont = pygame.font.SysFont('chalkboard',40)
        self.playerTurnFont = pygame.font.SysFont('chalkboard',30)
        self.entryFont = pygame.font.SysFont('chalkboard',30)
        self.prevWordFont = pygame.font.SysFont('chalkboard',40)

    def initPlayers(self,mode):
        self.p1 = Plenair(1)
        if mode == 'normal':
            self.p2 = Flonne(2)
        elif mode == 'AI':
            self.p2 = FlonneAI(2)

    def initShiritori(self):
        self.shiritori = Shiritori()
        self.entryMode = False
        self.entry = ""

    def initSounds(self):
        self.playMusic = True
        playlist = [GREATWILD,ADACHI,ONEWITHSTARS]

        self.music = random.choice(playlist)

    def __init__(self,mode):
        pygame.init()
        pygame.display.set_caption('Manifest')

        self.initScreenSurfaces()
        self.initImages()
        self.initFont()
        self.initPlayers(mode)
        self.initShiritori()
        self.initSounds()
        self.weapons = []

        self.roundEnd = False

        #init timer event
        pygame.time.set_timer(USEREVENT+1,1000)

        self.clock = pygame.time.Clock()

        self.running = True

    def terminateCommittedStates(self,stateTime1,state1,stateTime2,state2):
        #p1
        if state1 == 'attack' and stateTime1 >= self.p1.attackTotalTime:
            self.p1.setState('idle')

        elif state1 == 'flinch' and stateTime1 >= self.p1.flinchTotalTime:
            self.p1.setState('idle')

        #p2
        if state2 == 'attack' and stateTime2 >= self.p2.attackTotalTime:
            self.p2.setState('idle')

        elif state2 == 'flinch' and stateTime2 >= self.p2.flinchTotalTime:
            self.p2.setState('idle')

    def entryModeHandle(self,event):
        if event.type == KEYDOWN:
            if event.unicode in string.ascii_lowercase + string.ascii_uppercase:
                self.entry += event.unicode

            if event.key == K_RETURN:
                (isValidEntry, weapon) = self.shiritori.processEntry(self.entry)

                if isValidEntry:
                    hpBonus = self.shiritori.calculateHeal(self.entry)

                    if self.shiritori.turn == "Player 1":
                        self.p1.changeHp(hpBonus)
                    elif self.shiritori.turn == "Player 2": 
                        self.p2.changeHp(hpBonus)

                else:
                    if self.shiritori.turn == "Player 1":
                        self.p1.changeHp(-self.shiritori.hpPenalty)

                    elif self.shiritori.turn == "Player 2": 
                        self.p2.changeHp(-self.shiritori.hpPenalty)

                if weapon != None:
                    self.summonWeapon(weapon)

                self.entry = ""
                self.shiritori.changePlayerTurn()
                self.entryMode = False
                self.shiritori.turnTimeLeft = self.shiritori.turnTime

            elif event.key == K_BACKSPACE:
                self.entry = self.entry[:-1]

    def weaponAvailable(self):
        for weapon in self.weapons:
            if weapon.isEquipped == False:
                return True
        return False

    def eventHandle(self,stateTime1,state1,stateTime2,state2):
        if self.entryMode and not self.roundEnd:
            self.p1.state = 'idle'
            self.p2.state = 'idle'

        elif isinstance(self.p2,FlonneAI):
            if self.p2.weapon == 'fist' and self.weaponAvailable():
                for weapon in self.weapons:
                    if weapon.isEquipped == False:
                        if self.p2.approach(weapon):
                            self.equipWeapon(2)
                            break

            elif self.p2.approach(self.p1): self.p2.attack(self.p1)

        for event in pygame.event.get():
            #quit game
            if event.type == QUIT:
                self.running = False

            #timer event
            elif event.type == USEREVENT+1:
                self.shiritori.turnCountdown()

                if self.shiritori.turnTimeLeft <= 0:
                    self.entryMode = False
                    self.entry = ""

                    if self.shiritori.turn == 'Player 1':
                        self.p1.changeHp(-self.shiritori.hpPenalty)

                    elif self.shiritori.turn == 'Player 2':
                        self.p2.changeHp(-self.shiritori.hpPenalty)

                if self.p1.hp == 0 or self.p2.hp == 0:
                    self.roundEnd = True

                    if self.p1.hp == 0:
                        self.p1.state = 'lose'
                        self.p2.state = 'win'

                    elif self.p2.hp == 0:
                        self.p2.state = 'lose'
                        self.p1.state = 'win'

                    break

            else:
                #shiritori entry mode
                if self.entryMode == True:
                    self.entryModeHandle(event)

                #battle mode part 1
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE: 
                        return 'select'
                    elif event.key == K_RETURN: self.entryMode = True

                elif event.type == KEYUP:
                    #p1
                    if event.key == K_UP:
                        self.p1.setState('idle')
                    elif event.key == K_DOWN:
                        self.p1.setState('idle')
                    elif event.key == K_LEFT:
                        self.p1.setState ('idle')
                    elif event.key == K_RIGHT:
                        self.p1.setState('idle')

                    ##p2
                    if event.key == K_w:
                        self.p2.setState('idle')
                    elif event.key == K_s:
                        self.p2.setState('idle')
                    elif event.key == K_a:
                        self.p2.setState ('idle')
                    elif event.key == K_d:
                        self.p2.setState('idle')

                #battle mode part 2
                if not self.entryMode:
                    keys = pygame.key.get_pressed()

                    #p1 controls
                    if state1 != 'attack' and state1 != 'flinch':
                        #UDLR movement
                        if keys[K_UP]: self.p1.setState('moveup')
                        if keys[K_DOWN]: self.p1.setState('movedown')
                        if keys[K_LEFT]: self.p1.setState('moveleft')
                        if keys[K_RIGHT]: self.p1.setState('moveright')

                        #diagonal movement
                        if keys[K_UP] and keys[K_LEFT]: self.p1.setState('moveupleft')
                        if keys[K_UP] and keys[K_RIGHT]: self.p1.setState('moveupright')
                        if keys[K_DOWN] and keys[K_LEFT]: self.p1.setState('movedownleft')
                        if keys[K_DOWN] and keys[K_RIGHT]: self.p1.setState('movedownright')

                        #attack
                        if keys[K_COMMA]: 
                            self.p1.setState('attack')
                            
                            if self.p1.weapon == 'knife':
                                KNIFE.play()
                            elif self.p1.weapon == 'saber':
                                SABER.play()
                            elif self.p1.weapon == 'axe':
                                AXE.play()

                        #pickup/equip
                        if keys[K_SLASH]: self.equipWeapon(1)

                    #p2 controls
                    if state2 != 'attack' and state2 != 'flinch':
                        #UDLR movement
                        if keys[K_w]: self.p2.setState('moveup')
                        if keys[K_s]: self.p2.setState('movedown')
                        if keys[K_a]: self.p2.setState('moveleft')
                        if keys[K_d]: self.p2.setState('moveright')

                        #diagonal movement
                        if keys[K_w] and keys[K_a]: self.p2.setState('moveupleft')
                        if keys[K_w] and keys[K_d]: self.p2.setState('moveupright')
                        if keys[K_s] and keys[K_a]: self.p2.setState('movedownleft')
                        if keys[K_s] and keys[K_d]: self.p2.setState('movedownright')

                        #attack
                        if keys[K_z]: 
                            self.p2.setState('attack')

                            if self.p2.weapon == 'knife':
                                KNIFE.play()
                            elif self.p2.weapon == 'saber':
                                SABER.play()
                            elif self.p2.weapon == 'axe':
                                AXE.play()

                        #pickup/equip
                        if keys[K_c]: self.equipWeapon(2)

    def summonWeapon(self,weapon):
        if weapon == 'knife':
            if self.shiritori.turn == 'Player 1': (x,y) = self.p1.rect.midbottom
            else: (x,y) = self.p2.rect.midbottom
            self.weapons.append(Knife(x,y))

        elif weapon == 'saber':
            if self.shiritori.turn == 'Player 1': (x,y) = self.p1.rect.midbottom
            else: (x,y) = self.p2.rect.midbottom
            self.weapons.append(Saber(x,y))

        elif weapon == 'axe':
            if self.shiritori.turn == 'Player 1': (x,y) = self.p1.rect.midbottom
            else: (x,y) = self.p2.rect.midbottom
            self.weapons.append(Axe(x,y))

    def equipWeapon(self,player):
        for weapon in self.weapons:
            if weapon.isEquipped == False:
                weaponRect = Rect(weapon.x,weapon.y,weapon.rect.width,weapon.rect.height)

                if player == 1:
                    feetRect = Rect(self.p1.rect.midleft,self.p1.rect.bottomright)

                    if weaponRect.colliderect(feetRect):
                        self.p1.weapon = str(weapon)
                        self.p1.range = weapon.range
                        weapon.isEquipped = True
                        break

                elif player == 2:
                    feetRect = Rect(self.p2.rect.midleft,self.p2.rect.bottomright)

                    if weaponRect.colliderect(feetRect):
                        self.p2.weapon = str(weapon)
                        self.p2.range = weapon.range
                        weapon.isEquipped = True
                        break

    def hitBoxCollision(self,attackingPlayer):
        if attackingPlayer == 1:
            if self.p1.dir == 'left': weaponRect = Rect(self.p1.rect.midleft,(-self.p1.range,1))
            else: weaponRect = Rect(self.p1.rect.midright,(self.p1.range,1))
            hitBoxRect = self.p2.rect.inflate(-self.p2.rect.width*0.5,-self.p2.rect.height*0.5)

        elif attackingPlayer == 2:
            if self.p2.dir == 'left': weaponRect = Rect(self.p2.rect.midleft,(-self.p2.range,1))
            else: weaponRect = Rect(self.p2.rect.midright,(self.p2.range,1))
            hitBoxRect = self.p1.rect.inflate(-self.p2.rect.width*0.5,-self.p2.rect.height*0.5)

        return weaponRect.colliderect(hitBoxRect)

    def attackAnimHandle(self,player):
        if player == 1:
            self.p1.attackconductor.play()

            if self.p1.dir == 'left':
                if self.p1.weapon == 'fist':
                    self.p1.fistAnimL.blit(self.P1SURFACE,(self.p1.rect.x,self.p1.rect.y))
                elif self.p1.weapon == 'knife':
                    self.p1.knifeAnimL.blit(self.P1SURFACE,(self.p1.rect.x,self.p1.rect.y))
                elif self.p1.weapon == 'saber':
                    self.p1.saberAnimL.blit(self.P1SURFACE,(self.p1.rect.x,self.p1.rect.y))
                elif self.p1.weapon == 'axe':
                    self.p1.axeAnimL.blit(self.P1SURFACE,(self.p1.rect.x,self.p1.rect.y))

            elif self.p1.dir == 'right':
                if self.p1.weapon == 'fist':
                    self.p1.fistAnimR.blit(self.P1SURFACE,(self.p1.rect.x,self.p1.rect.y))
                elif self.p1.weapon == 'knife':
                    self.p1.knifeAnimR.blit(self.P1SURFACE,(self.p1.rect.x,self.p1.rect.y))
                elif self.p1.weapon == 'saber':
                    self.p1.saberAnimR.blit(self.P1SURFACE,(self.p1.rect.x,self.p1.rect.y))
                elif self.p1.weapon == 'axe':
                    self.p1.axeAnimR.blit(self.P1SURFACE,(self.p1.rect.x,self.p1.rect.y))

            if self.hitBoxCollision(1):
                self.p2.setState('flinch')
                self.p2.changeHp(-self.p1.atk)

        elif player == 2:
            self.p2.attackconductor.play()

            if self.p2.dir == 'left':
                if self.p2.weapon == 'fist':
                    self.p2.fistAnimL.blit(self.P2SURFACE,(self.p2.rect.x,self.p2.rect.y))
                elif self.p2.weapon == 'knife':
                    self.p2.knifeAnimL.blit(self.P2SURFACE,(self.p2.rect.x,self.p2.rect.y))
                elif self.p2.weapon == 'saber':
                    self.p2.saberAnimL.blit(self.P2SURFACE,(self.p2.rect.x,self.p2.rect.y))
                elif self.p2.weapon == 'axe':
                    self.p2.axeAnimL.blit(self.P2SURFACE,(self.p2.rect.x,self.p2.rect.y))

            elif self.p2.dir == 'right':
                if self.p2.weapon == 'fist':
                    self.p2.fistAnimR.blit(self.P2SURFACE,(self.p2.rect.x,self.p2.rect.y))
                elif self.p2.weapon == 'knife':
                    self.p2.knifeAnimR.blit(self.P2SURFACE,(self.p2.rect.x,self.p2.rect.y))
                elif self.p2.weapon == 'saber':
                    self.p2.saberAnimR.blit(self.P2SURFACE,(self.p2.rect.x,self.p2.rect.y))
                elif self.p2.weapon == 'axe':
                    self.p2.axeAnimR.blit(self.P2SURFACE,(self.p2.rect.x,self.p2.rect.y))

            if self.hitBoxCollision(2):
                self.p1.setState('flinch')
                self.p1.changeHp(-self.p2.atk)

    def idleMoveAnimHandle(self,stateTime1,state1,stateTime2,state2):
        #p1
        if state1 == 'idle':
            if self.p1.dir == 'left':
                self.p1.idleAnimL.blit(self.P1SURFACE,(self.p1.rect.x,self.p1.rect.y))

            elif self.p1.dir == 'right':
                self.p1.idleAnimR.blit(self.P1SURFACE,(self.p1.rect.x,self.p1.rect.y))

        elif (state1 == 'moveleft' or
              state1 == 'moveupleft' or
              state1 == 'movedownleft' or
              (state1 == 'moveup' and self.p1.dir == 'left') or
              (state1 == 'movedown' and self.p1.dir == 'left')):

            self.p1.walkAnimL.blit(self.P1SURFACE,(self.p1.rect.x,self.p1.rect.y))

        elif (state1 == 'moveright' or
              state1 == 'moveupright' or
              state1 == 'movedownright' or
              (state1 == 'moveup' and self.p1.dir == 'right') or
              (state1 == 'movedown' and self.p1.dir == 'right')):
        
            self.p1.walkAnimR.blit(self.P1SURFACE,(self.p1.rect.x,self.p1.rect.y))

        elif state1 == 'attack':
            self.attackAnimHandle(1)

        elif state1 == 'flinch':
            self.p1.flinchconductor.play()
            if self.p1.dir == 'left':
                self.p1.flinchAnimL.blit(self.P1SURFACE,(self.p1.rect.x,self.p1.rect.y))

            elif self.p1.dir == 'right':
                self.p1.flinchAnimR.blit(self.P1SURFACE,(self.p1.rect.x,self.p1.rect.y))

        #p2
        if state2 == 'idle':
            if self.p2.dir == 'left':
                self.p2.idleAnimL.blit(self.P2SURFACE,(self.p2.rect.x,self.p2.rect.y))

            elif self.p2.dir == 'right':
                self.p2.idleAnimR.blit(self.P2SURFACE,(self.p2.rect.x,self.p2.rect.y))

        elif (state2 == 'moveleft' or
              state2 == 'moveupleft' or
              state2 == 'movedownleft' or
              (state2 == 'moveup' and self.p2.dir == 'left') or
              (state2 == 'movedown' and self.p2.dir == 'left')):

            self.p2.walkAnimL.blit(self.P2SURFACE,(self.p2.rect.x,self.p2.rect.y))

        elif (state2 == 'moveright' or
              state2 == 'moveupright' or
              state2 == 'movedownright' or
              (state2 == 'moveup' and self.p2.dir == 'right') or
              (state2 == 'movedown' and self.p2.dir == 'right')):
        
            self.p2.walkAnimR.blit(self.P2SURFACE,(self.p2.rect.x,self.p2.rect.y))

        elif state2 == 'attack':
            self.attackAnimHandle(2)
              
        elif state2 == 'flinch':
            self.p2.flinchconductor.play()
            if self.p2.dir == 'left':
                self.p2.flinchAnimL.blit(self.P2SURFACE,(self.p2.rect.x,self.p2.rect.y))

            elif self.p2.dir == 'right':
                self.p2.flinchAnimR.blit(self.P2SURFACE,(self.p2.rect.x,self.p2.rect.y))

    def drawHUD(self):
        ##p1 hp
        pygame.draw.rect(self.screen,BLACK,(self.p1.portraitRect.right,50,300,10))
        pygame.draw.rect(self.screen,self.p1.color,(self.p1.portraitRect.right,50,self.p1.hp*3,10))

        ##p2 hp
        pygame.draw.rect(self.screen,BLACK,(self.p2.portraitRect.left-300,50,300,10))
        pygame.draw.rect(self.screen,self.p2.color,(self.p2.portraitRect.left,50,-self.p2.hp*3,10))

        ##define text
        prevWordText = self.prevWordFont.render(self.shiritori.prevWord,True,BLACK)

        if self.shiritori.turn == 'Player 1':
            turnTimeLeftText = self.turnTimeLeftFont.render(str(self.shiritori.turnTimeLeft),True,self.p1.color)
            playerTurnText = self.playerTurnFont.render(self.p1.name,True,self.p1.color)

        elif self.shiritori.turn == 'Player 2': 
            turnTimeLeftText = self.turnTimeLeftFont.render(str(self.shiritori.turnTimeLeft),True,self.p2.color)
            playerTurnText = self.playerTurnFont.render(self.p2.name,True,self.p2.color)

        prevWordTextRect = prevWordText.get_rect()
        prevWordTextRect.centerx = self.bgRect.centerx
        prevWordTextRect.centery = 120

        turnTimeLeftTextRect = turnTimeLeftText.get_rect()
        turnTimeLeftTextRect.centerx = self.bgRect.centerx
        turnTimeLeftTextRect.centery = 80

        playerTurnTextRect = playerTurnText.get_rect()
        playerTurnTextRect.centerx = self.bgRect.centerx
        playerTurnTextRect.centery = 50

        #blitting
        self.screen.blit(turnTimeLeftText,turnTimeLeftTextRect)
        self.screen.blit(playerTurnText,playerTurnTextRect)
        self.screen.blit(prevWordText,prevWordTextRect)

    def drawEntryMode(self):
        #draw entry field
        self.screen.blit(self.entryField,self.entryFieldRect)

        #draw entry text
        if self.shiritori.turn == 'Player 1':
            entryText = self.entryFont.render(self.entry,True,self.p1.color)
        elif self.shiritori.turn == 'Player 2':
            entryText = self.entryFont.render(self.entry,True,self.p2.color)

        entryTextRect = entryText.get_rect()
        entryTextRect.center = self.bgRect.center

        self.screen.blit(entryText,entryTextRect)

    def drawWeapons(self):
        for weapon in self.weapons:
            if weapon.isEquipped == False:
                self.screen.blit(weapon.image,weapon.rect)

    def drawPortraits(self):
        self.p1.portraitRect.topleft = self.bgRect.topleft
        self.p2.portraitRect.topright = self.bgRect.topright

        self.screen.blit(self.p1.portrait,self.p1.portraitRect)
        self.screen.blit(self.p2.portrait,self.p2.portraitRect)

        weapon1 = self.p1.weapon
        weapon2 = self.p2.weapon

        if weapon1 == 'knife':
            image1 = Knife().image

        elif weapon1 == 'saber':
            image1 = Saber().image

        elif weapon1 == 'axe':
            image1 = Axe().image

        if weapon2 == 'knife':
            image2 = Knife().image

        elif weapon2 == 'saber':
            image2 = Saber().image

        elif weapon2 == 'axe':
            image2 = Axe().image
        
        if weapon1 != 'fist':
            imageRect1 = image1.get_rect()
            imageRect1.left = self.p1.portraitRect.right
            imageRect1.top = self.p1.portraitRect.centery + 5
            self.screen.blit(image1,imageRect1)

        if weapon2 != 'fist':
            imageRect2 = image2.get_rect()
            imageRect2.right = self.p2.portraitRect.left
            imageRect2.top = self.p2.portraitRect.centery + 5
            self.screen.blit(image2,imageRect2)

    def drawRoundEnd(self):
        self.screen.blit(self.bg,(0,0))
        self.P1SURFACE.fill(WHITE)
        self.P2SURFACE.fill(WHITE)

        if self.p1.state == 'win':
            if self.p1.name == 'Plenair':
                self.screen.blit(self.plenairwin,self.winRect)
            elif self.p1.name == 'Flonne':
                self.screen.blit(self.flonnewin,self.winRect)

            self.p1.winconductor.play()
            if self.p1.dir == 'left':
                self.p1.winAnimL.blit(self.P1SURFACE,(self.p1.rect.x,self.p1.rect.y))

            elif self.p1.dir == 'right':
                self.p1.winAnimR.blit(self.P1SURFACE,(self.p1.rect.x,self.p1.rect.y))

        elif self.p1.state == 'lose':
            self.p1.loseconductor.play()
            if self.p1.dir == 'left':
                self.p1.loseAnimL.blit(self.P1SURFACE,(self.p1.rect.x,self.p1.rect.y))

            elif self.p1.dir == 'right':
                self.p1.loseAnimR.blit(self.P1SURFACE,(self.p1.rect.x,self.p1.rect.y))

        if self.p2.state == 'win':
            if self.p2.name == 'Plenair':
                self.screen.blit(self.plenairwin,self.winRect)
            elif self.p2.name == 'Flonne':
                self.screen.blit(self.flonnewin,self.winRect)

            self.p2.winconductor.play()
            if self.p2.dir == 'left':
                self.p2.winAnimL.blit(self.P2SURFACE,(self.p2.rect.x,self.p2.rect.y))

            elif self.p1.dir == 'right':
                self.p2.winAnimR.blit(self.P2SURFACE,(self.p2.rect.x,self.p2.rect.y))

        elif self.p2.state == 'lose':
            self.p2.loseconductor.play()
            if self.p2.dir == 'left':
                self.p2.loseAnimL.blit(self.P2SURFACE,(self.p2.rect.x,self.p2.rect.y))

            elif self.p2.dir == 'right':
                self.p2.loseAnimR.blit(self.P2SURFACE,(self.p2.rect.x,self.p2.rect.y))           

        if self.p1.rect.y < self.p2.rect.y:
            self.screen.blit(self.P1SURFACE,(0,0))
            self.screen.blit(self.P2SURFACE,(0,0))

        else:
            self.screen.blit(self.P2SURFACE,(0,0))
            self.screen.blit(self.P1SURFACE,(0,0))

    def loopEnd(self):
        pygame.display.update()
        self.clock.tick(FPS)
        if not self.running:
            pygame.quit()

    def run(self):
        if self.playMusic == True:
            self.music.play(-1)
            self.playMusic = False

        (stateTime1,state1) = self.p1.getState() #p1 state info
        (stateTime2,state2) = self.p2.getState() #p2 state info

        self.terminateCommittedStates(stateTime1,state1,stateTime2,state2)
        if self.eventHandle(stateTime1,state1,stateTime2,state2) != None:
            self.music.fadeout(200)
            return 'select'

        #process events
        self.p1.moveHandler()
        self.p2.moveHandler()

        #background, clear surface
        self.screen.blit(self.bg,(0,0))
        self.P1SURFACE.fill(WHITE)
        self.P2SURFACE.fill(WHITE)

        #animation handle
        self.p1.moveconductor.play()
        self.p2.moveconductor.play()

        #player anim
        self.idleMoveAnimHandle(stateTime1,state1,stateTime2,state2)

        #blit players
        self.P1SURFACE.set_colorkey(WHITE)
        self.P2SURFACE.set_colorkey(WHITE)

        if self.p1.rect.y < self.p2.rect.y:
            self.screen.blit(self.P1SURFACE,(0,0))
            self.screen.blit(self.P2SURFACE,(0,0))

        else:
            self.screen.blit(self.P2SURFACE,(0,0))
            self.screen.blit(self.P1SURFACE,(0,0))

        #blit entryMode
        if self.entryMode == True:
            entryText = self.entryFont.render(self.entry,True,BLACK)
            self.drawEntryMode()

        #draw
        self.drawHUD()
        self.drawWeapons()
        self.drawPortraits()

        #roundEnd
        if self.roundEnd == True:
            self.drawRoundEnd()

            self.loopEnd()
            pygame.time.delay(3000)
            self.music.fadeout(200)
            return 'select'

        self.loopEnd()
