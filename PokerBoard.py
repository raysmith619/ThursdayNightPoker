'''
Created on Mar 8, 2017

@author: raysm
'''
from __future__ import print_function
import random
import itertools

from PyTrace import tR

from PokerDeck import PokerDeck
from PokerCard import PokerCard
from PokerHandDirection import PokerHandDirection
# Exceptions

class UnsupportedGameError(Exception):

    """Exception for when an unsupported game is chosen

    """

    pass


class PokerBoard(object):
    '''
    Poker board - holding community cards
    Of which, zero or more cards may be used, in combination with
    zero or more of each player's cards, to complete one or more hands
    '''


    def __init__(self, table, deck, game=None, direction=None):
        '''
        Constructor
        table our link to tracing
        
        deck is the card deck, from which cards are obtained
        
        game is the poker game name which determines the type of game
        and the board display and players' access to the board cards
        
        direction: 1 - high, 2 - low, 3 - high-low

        toy - toy version of "44" as 22
                x1 x2
                x3 x4
                
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
        self.table = table
        self.deck = deck
        
        if game == None:
            game = "44"
        self.game = game
        
        if direction == None:
            direction = PokerHandDirection.HIGH_LOW
        self.direction = direction
        
        self.setBoard()
    
    
    def setBoard(self):
        """
        Setup board, including populating with cards from deck and displaying
        """
        if self.game == "44":
            self.ncard = 8
            self.nrow = 2
            self.minChoice = 1
            self.maxChoice = 2
            self.selections = [(1,5), (2,6), (3,7), (4,8)]
        elif self.game == "Adjacent":
            self.ncard = 8
            self.minChoice = 1
            self.maxChoice = 2
            self.selections = [(1,2), (2,3), (3,4), (4,5),
                               (5,6), (6,7), (7,8), (8,1)]
        elif self.game == "toy":
            self.ncard = 4
            self.nrow = 2
            self.minChoice = 1
            self.maxChoice = 2
            self.selections = [(1,3), (2,4)]
             
        else:
            raise UnsupportedGameError("Don't yet support game {}".format(self.game))
        self.populate()


    def getCard(self, pos):
        """
        Get card from position in board
        """
        return self.cards[pos-1]


    def getCards(self, hidden=False):
        """
        get cards from board
        hidden - True ==> include hidden cards
                 False ==> just exposed cards
        """
        ret_cards = []
        for card in self.cards:
            if hidden or not card.isHidden():
                ret_cards.append(card)
        return ret_cards

    
    def getGroups(self):
        """
        Returns list of card selections possible
        based on visible cards and selections choices
            i.e. if selection is AC(visible), KC(hidden), JC(visible)
            return (AC), (JC), (AC,JC) 
                
        """
        groups = []
        for selection in self.selections:
            group = []
            for pos in selection:
                card = self.getCard(pos)
                if not card.isHidden():
                    group.append(card)
            if len(group) > 0:
                for glen in range(self.minChoice, self.maxChoice+1):
                    subgroups = itertools.combinations(group, glen)
                    groups.extend(subgroups)
                    
        return groups
    
            
    def getNextShowPos(self):
        """
        Get next position to show in board 0 if none
        """
        hidden_cards = []
        for card in self.cards:
            if card.isHidden():
                hidden_cards.append(card)
        if len(hidden_cards) == 0:
            return 0        
        card = random.choice(hidden_cards)    
        return card.position
    
    def populate(self):
        """
        populate the board with cards
        """
        self.cards = []
        for i in range(self.ncard):
            pos = i + 1
            card = self.deck.draw(1)[0]
            if tR('board'):
                print("draw:{} populate".format(card))
            boardCard = PokerCard(self.table,
                                  inBoard = True,
                                  baseCard=card, position=pos)
            self.cards.append(boardCard)


    def displaySimple(self, showAll=False):
        print("\nBoard:", end="")
        if self.nrow is not None:
            i = 0
            ncol = self.ncard/self.nrow
            for irow in range(self.nrow):
                if irow > 0:
                    print(" " * 6, end="")
                for icol in range(ncol):
                    pokerCard = self.cards[i]
                    print(" {}".format(
                        pokerCard.simpleString(showAll=showAll))
                      , end="")
                    i += 1
                print("")
            print("")
            return
        
        for pokerCard in self.cards:
            print(" {}".format(
                    pokerCard.simpleString(showAll=showAll))
                  , end="")
        print("")


    def showCard(self, pos=None):
        """
        Show next card at pos.  If pos is None choose pos at random
        within game's rules
        """
        if pos == None:
            pos = self.getNextShowPos()
        if (pos > 0):
            ##print("showCard(pos={})".format(pos))
            self.setHidden(pos=pos, hidden=False)

    
    def setHidden(self,pos=None, hidden=True):
        if pos == None:
            raise AssertionError("pos must be set")
        i = pos-1
        self.cards[i].setHidden(hidden=hidden)
        
        

"""
Stanalone test / exercise
"""
if __name__ == "__main__":
    from PokerTable import PokerTable
    table = PokerTable()
    deck = PokerDeck()
    deck.shuffle()
    board = PokerBoard(table, game="44")
     