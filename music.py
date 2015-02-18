import pygame, os

pygame.mixer.init()

def loadMusic(fileName):
    pathname = os.path.join('Audio',fileName)
    return pygame.mixer.Sound(pathname)

LILIUM = loadMusic("Lilium.wav")

DECISION = loadMusic("decision.wav")
DECISION.set_volume(0.3)

CORELLI = loadMusic('Corelli La Folia.wav')
CORELLI.set_volume(0.5)

GREATWILD = loadMusic("The Great Wild.wav")
GREATWILD.set_volume(0.7)

ADACHI = loadMusic("Adachi's Theme.wav")

ONEWITHSTARS = loadMusic("One With The Stars.wav")

KNIFE = loadMusic("knife.wav")
KNIFE.set_volume(2)

SABER = loadMusic("saber.wav")
AXE = loadMusic("axe.wav")
