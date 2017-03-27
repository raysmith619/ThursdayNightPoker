'''
Created on Mar 8, 2017

@author: raysm
'''
from __future__ import print_function

from PyTrace import tR
from PokerDeal import PokerDeal
from PokerGame import PokerGame
from PokerPlayer import PokerPlayer
from PokerGames import Games
# Exceptions

class UnsupportedGameError(Exception):

    """Exception for when an unsupported game is chosen

    """

    pass


class PokerTable(object):
    '''
    Poker board - holding community cards
    Of which, zero or more cards may be used, in combination with
    zero or more of each player's cards, to complete one or more hands
    '''


    def __init__(self,
                 deck=None,
                 gameName=None,     # Table defaults
                 direction=None,
                 playerNames=None,
                 nPlayer=None,
                 dealerPos=1,
                 mePos=1):
        '''
        Constructor
        
        deck is the card deck, from which cards are obtained
        
        game is the poker game name which determines the type of game
        and the board display and players' access to the board cards
        
        direction: 1 - high, 2 - low, 3 - high-low
        
        playerNames is a list of player names
            default is ray, arlene, jen, leanne, rob
        nplayer is number of players
            default is len(playerNames)
            
        44 (Forty-Four) - 4 cards to each player. A board of two rows of
        4 cards each, of which the play may use 1 or 2 cards from one
        column for each hand (high and low)
        board in the form:
            x1 x2 x3 x4
            x5 x6 x7 x8
        A player may use 1 or 2 of one column: x1,x5, x2,x6, x3,x7, x4,x8
        
        33 (Thirty-Three) - 4 cards to each player. A board of ...???
        
        Adjacent(???) - 4 cards to each player
            board in the form:
                 x1 x2
               x8     x3
               x7     x4
                 x6 x5
                 
        A player may use 1 or 2 of adjacent board cards (e.g x1,x2,
             x2,x3, ... , x7,x8, x8,x1 to augment 3 or 4 of the player's
             cards.  
        '''
        self.players = []   # Tables players
        self.deck = deck
        
        if gameName is None:
            gameName = "44"
        self.gameName = gameName
        self.game = Games[gameName]
        
        if direction is None:
            direction = 3
        self.direction = direction
        
        if playerNames is None:
            playerNames = ["ray", "arlene", "jen", "leanne", "rob"]

        if nPlayer is not None:
            if nPlayer > len(playerNames):
                raise AssertionError(
                "nPlayer({}) is not <= len(playerNames)".format(nPlayer))
            playerNames = playerNames[:nPlayer]
        self.playerNames = playerNames
        
        self.setTable()
        self.setDealer(dealerPos)
        self.setMe(mePos)

        
    def setTable(self):
        """
        Setup table
        """
        ### Do stuff in deal ### self.board = PokerBoard(game=self.game)
        
        self.populate()
                
    def populate(self):
        """
        populate table with the initial players
        """
        
        for name in self.playerNames:
            self.players.append(PokerPlayer(name))
            

    def displaySimple(self, showAll=False, showMe=True):
        self.thisDeal.displaySimple(showAll=showAll, showMe=showMe)


    def setDealer(self, dealerPos=1):
        """
        Set dealer position in table
        """
        self.dealerPos = dealerPos
        
    def setMe(self, mePos=1):
        """
        Set principle player's position in table
        """
        self.mePos = mePos

    def isMe(self, player):
        name = player.name
        posName = self.playerNames[self.mePos-1]
        if name == posName:
            return True
        return False

    def deal(self,
            newGame=True,
            shuff=True,
            gameName = None,
            direction = None,   # direction overrides game defaule
            deck=None):
        if newGame:
            thisDeal = self.thisDeal = PokerDeal(self,
                                         shuff=shuff,
                                         gameName=gameName,
                                         direction=direction,
                                         deck=deck)
        return self.thisDeal    
"""
Stanalone test / exercise
"""
if __name__ == "__main__":
    traceAll = False
    table = PokerTable()
    deal = table.deal(gameName="44")
    table.displaySimple(showMe=True)
    if traceAll:
        table.displaySimple(showAll=True)
    while deal.hasMorePlays():
        deal.play()
    print("End of Hand")
     
     