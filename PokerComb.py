'''
Poker Combinations / Odds
Uses numpy to reduced space / time usage in combinations
Created on Mar 27, 2017

@author: Ray Smith
'''
from __future__ import print_function
import itertools
from collections import Counter


from PyTrace import tR
from PokerDeck import PokerDeck
from PokerCard import PokerCard
from PokerDeal import PokerDeal
from PokerHandHL import PokerHandHL
from PokerHandDirection import PokerHandDirection

HIGH = PokerHandDirection.HIGH
LOW = PokerHandDirection.LOW
HIGH_LOW = PokerHandDirection.HIGH_LOW

class PokerComb(object):
    '''
    Poker combinations
    Embeds direction
    '''

    def __init__(self, direction=HIGH, lowFlushStrait=None):
        '''
        Constructor
        playerHands
        '''
        if lowFlushStrait is None:
            if direction==LOW:
                lowFlushStrait = True
            else:
                lowFlushStrait = False
        self.direction = direction
        self.lowFlushStrait = lowFlushStrait

    def betEqWorse(self, hand_tup, other_hand_tups):
        """
        Using tuples of short names to save space
        Returns (better, equal, less) numbers of other hands
        """
        nbetter = 0
        nequal = 0
        hand = PokerHandHL(namelist=list(hand_tup))
        for other_hand_tup in other_hand_tups:
            other = PokerHandHL(namelist=list(other_hand_tup))
            if other > hand:
                nbetter += 1
            elif other == hand:
                nequal += 1
            else:
                break
        nworse = len(other_hand_tups) - nbetter - nequal
        return (nbetter, nequal, nworse)
            
        return None
    
"""
Stanalone test / exercise:
"""
if __name__ == "__main__":
    from PyTrace import PyTrace
    trace_str = ""
    ###trace_str = "prob"
    PyTrace(flagStr=trace_str)
    print("Hand is done.")