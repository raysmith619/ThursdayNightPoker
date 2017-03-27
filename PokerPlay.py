'''
Poker Play - current round of play

@author: raysm
'''
from __future__ import print_function


class PokerPlay(object):
    '''
    Poker deal - current hand
    '''
    def __init__(self,
                 nBoard=0,      # Number exposed board cards on this play
                 nBurn = 0,     # Number of deck cards burned
                 nDeal = 0,     # Number of deck cards delt to player
                 nExchange = 0, # Number of player cards exchanged for deck cards
                 hasBet = False,    # Is there a bet on this play
                 ):   # Direction: 1 - high, 2 - low, 3 - high-low
        '''
        Constructor
        play
        '''
        self.nBoard = nBoard
        self.nBurn = nBurn
        self.nDeal = nDeal
        self.nExchange = nExchange
        self.hasBet = hasBet

    
    def hasBoardShow(self):
        if self.nBoard > 0:
            return True
        return False


    def showBoard(self):
        game = self.game
    
    def hasDeal(self):
        if self.nDeal > 0:
            return True    
        return False

    def burn(self):
        if self.nBurn > 0:
            for i in range(self.nBurn):
                self.burnOne()
                
    
    def hasBet(self):
        if self.hasBet:
            return True
        return False
                