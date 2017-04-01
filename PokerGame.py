'''
Poker rules for one game

@author: raysm
'''
from __future__ import print_function
from PokerHandDirection import PokerHandDirection
# Exceptions

class UnsupportedGameError(Exception):

    """Exception for when an unsupported game is chosen

    """

    pass


class PokerGame(object):
    '''
    Poker board - holding community cards
    Of which, zero or more cards may be used, in combination with
    zero or more of each player's cards, to complete one or more hands
    '''


    def __init__(self,
                name,           # Game name
                handSize = 5,   # Hand size (number of cards making a hand)
                nPlayerCards=4, # Number of cards to each player
                nUp=0,          # Number of up cards
                nBoard=8,       # Number of board cards
                nBoardUp = 0,   # Number of up board cards
                nStraitCards=None, # Length of strait, default: handSize
                nFlushCards=None,  # Length of flush, default: handSize
                direction=PokerHandDirection.HIGH_LOW,    # Direction for win
                lowFlushStrait = True,       # disregard flush,strait in low 
                plays = []):    # Plays in deal
        '''
        Constructor
        Game rules
        '''
        self.name = name
        self.handSize = handSize
        self.nPlayerCards = nPlayerCards
        self.nUp = nUp
        self.nBoard = nBoard
        self.nBoardUp = nBoardUp
        if nStraitCards is None:
            nStraitCards = self.handSize
        self.nStraitCards = nStraitCards
        if nFlushCards is None:
            nFlushCards = self.handSize
        self.nFlushCards = nFlushCards
        self.direction = direction
        self.lowFlushStrait = lowFlushStrait
        self.plays = plays
        
        