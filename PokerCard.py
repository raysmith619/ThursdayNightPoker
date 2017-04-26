'''
Created on Mar 8, 2017

@author: raysm
'''
from __future__ import print_function
import re

from PyTrace import tR  # trace activity support
from PokerCardBase import PokerCardBase

        
class PokerCard(PokerCardBase):
    '''
    Contains card info plus attributes of community display and sharing
    '''
    """
    Static methods
    """
    
    @staticmethod
    def cards(cardstr):
        """
        Convert string of short card names into a list of cards
        Stings(case insens of the form "1S,2C,3H,10S" or "1S 2C 3H 10S" or "1s2c3h10s"
                or "1s, 2s, 3s" or "1s-2s-3s"
                Splitting regular expression is: \s*[+,:;-]\s*
        Returns only cards within deck limits (to facilitate debugging)
        """
        c_pattern = '\s*[+,:;-]\s*'        # separate card string
        cws_pattern = '\s+'             # White space separation
        card_pattern = '([aAkKqQjJ]|\d|10)[cChHdDsS]'                 
        card_strs = []
        if re.search(c_pattern, cardstr):
            card_strs = re.split(c_pattern, cardstr)
        elif re.search(cws_pattern, cardstr):
            card_strs = re.split(cws_pattern, cardstr)
        else:
            """ looking from left for matches of the form ([aAkKqQjJ]|\d|10)[cChHdDsS] """
            cs_str = cardstr
            while True:
                m = re.search(card_pattern, cs_str)
                if m:
                    cs = cs_str[m.start():m.end()]
                    card_strs.append(cs)        # Add next card
                    cs_str = cs_str[m.end():]   # search the rest of the string
                else:
                    break                       # No more cards
        
        cards = []
        for card_str in card_strs:
            cm = re.match(r'(\S+)(\S)', card_str)
            if not cm:
                raise EnvironmentError("Unrecognized card name:{}".format(card_str))
            rank_str = cm.group(1)
            suit_str = cm.group(2)
            if re.match(r'[aA]', rank_str):
                rank = 1
            elif re.match(r'[kK]', rank_str):
                rank = 13
            elif re.match(r'[qQ]', rank_str):
                rank = 12
            elif re.match(r'[jJ]', rank_str):
                rank = 12
            else:
                rank = int(rank_str)
            """0 is clubs, 1 is hearts, 2 is spades, and 3 is diamonds """    
            if re.match(r'[cC]', suit_str):
                suit = 0   
            elif re.match(r'[hH]', suit_str):
                suit = 1   
            elif re.match(r'[sS]', suit_str):
                suit = 2   
            elif re.match(r'[dD]', suit_str):
                suit = 3   
            else:
                raise EnvironmentError("Unrecognized card suit:")
            
            rank_limit = PokerCard.cardsInSuit()
            rank_limit += 1             # One more than in suit
            if rank > rank_limit:    # Allow Ace
                continue
            if suit >= PokerCard.nSuits():
                continue
            if len(cards) >= PokerCard.cardsInHand():
                continue

            card = PokerCard(name=card_str)
            cards.append(card)
        return cards  


    @staticmethod
    def getNCard():
        """
        Get number of cards in deck
        """
        return PokerCardBase.getNCard()
    
    
    """    
    Constructor
    """
    def __init__(self,
            rank=None, suit=None, index=None, name=None,
            baseCard=None,
            inBoard = False,
            hidden=True, position=None, isEmpty=False):
        self.inBoard = inBoard
        self.hidden = hidden    # hidden == face down
        self.position = position
        self.isEmpty = isEmpty
        if baseCard is not None:
            index=baseCard._index
            if index is None:
                raise ValueError("baseCard._index is None")
            if rank is not None or suit is not None or name is not None:
                rank = suit = name = None
        if tR('card'):
            print("baseCard={},index={}, rank={}, suit={}, name={}".format(baseCard, index, rank, suit, name))
        PokerCardBase.__init__(self,
                         rank=rank, suit=suit, index=index, name=name)


    def copy(self):
        return self.__class__(
            index=self.index(),
            inBoard = self.inBoard,
            hidden=self.hidden,
            position=self.position,
            isEmpty=self.isEmpty)


    def isHidden(self):
        return self.hidden


    def isInBoard(self):
        return self.inBoard
    
            
    def simpleString(self, showAll=False, showMe=True, isMe=False, short=True):
        cw = 5              # Card display width
        hidden = self.hidden
        #card = self.getBaseCard()
        if self.isEmpty:
            cardstr =     "[" + "  " + "]"
        elif hidden:
            if showAll or (isMe and showMe):
                cardstr = "[" + self.name_string(short=short) + "]"
            else:
                cardstr = "[" + "**" + "]"
        else:
            cardstr =     " " + self.name_string(short=short) + " "
        
        fmtstr = "{:<" + str(cw) + "}"
        cardstr = fmtstr.format(cardstr)
        return cardstr

    
    def getBaseCard(self):
        return self.card
    
    
    def setCard(self, card, hidden=True, empty=False):
        self.card = card
        self.empty = empty
        self.hidden = hidden
    
    def setHidden(self, hidden=True):
        self.hidden = hidden
    
    def setBoard(self, board=True):
        self.inBoard = board
        
    def setPosition(self,position):
        self.position = position 