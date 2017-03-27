'''
Simulate player action in game
Created on Mar 8, 2017

@author: raysm
'''
from __future__ import print_function

from PokerDeal import PokerDeal
from PokerHands import PokerHands
#from pcards.PokerTable import deal

# Exceptions

class UnsupportedGameError(Exception):

    """Exception for when an unsupported game is chosen

    """

    pass


class PokerPlayer(object):
    '''
    Poker Player - player
    '''


    def __init__(self, name):
        '''
        Constructor
        playerName - player name
        '''
        self.name = name
        self.cards = []         # PokerCard
        self.cash = 100
        self.minBet = 1
        
    def displaySimple(self, showAll = False, isMe=False, showMe=True,
                      isDealer=False):
        if isMe:
            print(" ME", end="")
        else:
            print("   ", end="")
            
        if isDealer:
            print(" D", end="")
        else:
            print("  ", end="")
            
            
        print(" {0:<8}".format(self.name), end= "")
        for i in range(len(self. cards)):
            boardcard = self.cards[i]
            print(boardcard.simpleString(showAll=showAll,
                                         showMe=showMe,
                                         isMe=isMe), end=" ")
            
        print(" cash: {}".format(self.cash))                
    
    
    def addCard(self, card, pos=None, hidden=None):
        if pos == None:
            pos = len(self.cards) + 1
        card.setPosition(pos)
        if hidden != None:
            card.setHidden(hidden)
        self.cards.append(card)


    def autoPlayBet(self, amount=None, position=None):
        """
        Play the game
        amount is the "bet to you", the required amount to stay in the deal
        Initially we find the hand strength(possible) and bet on that alone
        Return None to drop, 0 to check, or bet amount
        """
        if (self.deal.direction == PokerDeal.HIGH
            or self.deal.direction == PokerDeal.HIGH_LOW):
            self.handsHigh = self.getHands(self.deal, direction=PokerDeal.HIGH, sort=True)
        
        if (self.deal.direction == PokerDeal.LOW
            or self.deal.direction == PokerDeal.HIGH_LOW):
            self.handsLow = self.getHands(self.deal, direction=PokerDeal.LOW, sort=True)
        """
        Stay in if:
            1. we have a hand(pair Jacks or better for high
                7 or lower) or
            2. no bet is required(check) or
            3. there is chance of improvement -
               2 or more cards / board to come
        """
        """ TFD - just bet if we can """
        if amount == None:
            return self.minBet
        if self.cash >= amount:
            self.cash -= amount
            return amount
        amount = self.cash
        self.cash = 0
        return amount
    
    def bet(self, doPrompt=None,
            position=0, amount=None):
        """
        Make bet on current game
        """
        if doPrompt:
            amount = self.getBet(amount=amount)
        else:
            amount = self.autoPlayBet(position=position,
                                      amount=None)
            return amount
        
        if amount == None:
            amount = self.game.minBet
            
        if amount > self.cash:
            amount = self.cash
        self.cash -= amount
        return amount


    def getCards(self):
        return self.cards[:]


    def getHands(self,
                 deal,
                 direction=None,
                 lowFlushStrait=None,
                 sort=True):
        poker_hands = PokerHands(deal, direction=direction, lowFlushStrait=lowFlushStrait)
        return poker_hands.getHands(player=self, sort=sort)
    
    
    
    def joinDeal(self, deal):
        """
        Join deal
        May have ante, position here
        """
        self.deal = deal
        self.handsHigh = []
        self.handsLow = []
        

     