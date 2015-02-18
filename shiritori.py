from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import words

from weaponDict import *

wordset = words.words()
instance = WordNetLemmatizer()

class Shiritori(object):

    def __init__(self):
        self.used = set()
        self.prevWord = None
        self.turn = "Player 1"

        self.p1score = 0
        self.p2score = 0

        self.turnTime = 30
        self.turnTimeLeft = self.turnTime

        self.hpPenalty = 5
    
    def isUnusedWord(self,word): 
        if word in self.used:
            return False
        return True

    def isValidWord(self,word):
        if word in wordset: return True
        return False

    def followsRules(self,word):
        if self.prevWord == None:
            return True

        if word[0] == self.prevWord[-1]:
            return True

        return False

    def isLegalEntry(self,word):
        if (self.isUnusedWord(word) and 
            self.isValidWord(word) and 
            self.followsRules(word)):
            return True

        return False

    def turnCountdown(self):
        if self.turnTimeLeft > -1:
            self.turnTimeLeft -= 1

        if self.turnTimeLeft == -1:
            self.turnTimeLeft = self.turnTime
            self.changeTurn()

    def changeTurn(self):
        if self.turn == 'Player 1':
            self.turn = 'Player 2'

        elif self.turn == 'Player 2':
            self.turn = 'Player 1'

    def isWeapon(self,entry):
        for wepclass in weapons:
            for i in xrange(len(wepclass)):
                if wepclass[i] == entry:
                    return wepclass[0]
        return None

    def calculateHeal(self,entry):
        heal = 0

        if not self.isWeapon(entry):
            points = len(entry) - 4
            if points > 0:
                heal += points

        return heal

    def processEntry(self,entry):
        entry = entry.lower().strip()
        word = instance.lemmatize(entry)

        if self.isLegalEntry(word):
            self.used.add(word)
            self.prevWord = entry

            weapon = self.isWeapon(entry)

            return (True, weapon)
        return (False, None)

    def changePlayerTurn(self):
        if self.turn == "Player 1": self.turn = "Player 2"
        else: self.turn = "Player 1"

#allows first (and subsequent) lemmatization in-game to run faster
instance.lemmatize('manifest')
