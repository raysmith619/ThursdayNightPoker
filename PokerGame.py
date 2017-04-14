'''
Poker rules for one game

@author: raysm
'''
from __future__ import print_function
from PokerHandDirection import PokerHandDirection
from PokerCardBase import PokerCardBase

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
                nPlayerCards=4, # Number of cards to each player
                nUp=0,          # Number of up cards
                nBoard=8,       # Number of board cards
                nBoardUp = 0,   # Number of up board cards
                boardSelections = None,
                direction=PokerHandDirection.HIGH_LOW,    # Direction for win
                lowFlushStrait = True,       # disregard flush,strait in low 
                plays = [],     # Plays in deal

                nsuit=None,     # Basic Poker Settings
                ninsuit=None,
                ncard=None,
                nCardInHand=None,
                nCardInStrait=None,
                nCardInFlush=None,
                ):
        '''
        Constructor
        Game rules
        '''
        self.name = name
        self.savePokerSettings(
            nsuit=nsuit,
            ninsuit=ninsuit,
            ncard=ncard,
            nCardInHand=nCardInHand,
            nCardInStrait=nCardInStrait,
            nCardInFlush=nCardInFlush
            )
        self.nPlayerCards = nPlayerCards
        self.nUp = nUp
        self.nBoard = nBoard
        self.nBoardUp = nBoardUp
        self.boardSelections = boardSelections
        self.direction = direction
        self.lowFlushStrait = lowFlushStrait
        self.plays = plays
        
    
    def savePokerSettings(self,**kwargs):
        """
        Save settings to be set when playting
        this game
        """
        self.pokerSettings = kwargs
        
        
    def setPokerSettings(self):
        """
        Setup poker settings saved at game definition
        """
        PokerCardBase.setPokerSettings(**self.pokerSettings)
        
            