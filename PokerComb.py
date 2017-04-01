'''
Poker Combinations / Odds
Uses numpy to reduced space / time usage in combinations
Created on Mar 27, 2017

@author: Ray Smith
'''
from __future__ import print_function
import itertools

from numpy import fromiter
from numpy import ones,empty,zeros,sum
import numpy as np

from PyTrace import tR
from PokerCardBase import PokerCardBase
from PokerHandHL import PokerHandHL
from PokerHandDirection import PokerHandDirection
from PokerCard import PokerCard

HIGH = PokerHandDirection.HIGH
LOW = PokerHandDirection.LOW
HIGH_LOW = PokerHandDirection.HIGH_LOW

class PokerComb(object):
    '''
    Poker combinations
    Embeds direction
    '''

    def __init__(self, hands=None, direction=HIGH, lowFlushStrait=None, nCardsInHand = 5):
        '''
        Constructor
        hands -  hands(PokerHandHL) to start with
        direction - game direction HIGH, LOW, HIGH_LOW
        lowFlushStrait - consider flush/strait low
        nCardsInHand - how many cards in hand
        '''
        if lowFlushStrait is None:
            if direction==LOW:
                lowFlushStrait = True
            else:
                lowFlushStrait = False
        self.direction = direction
        self.lowFlushStrait = lowFlushStrait
        self.nCardsInHand = nCardsInHand
        self.nPrimes = 1                 # Number of primary (4bit)
        self.nTiebreaks = 5              # Number of tiebreaks (4bit)
        self.nScoreBytes = (self.nPrimes+self.nTiebreaks)/2
        self.cardStart = self.nScoreBytes        # Index of first card index
        self.nHDesc = self.nScoreBytes + self.nCardsInHand          # Number of description bytes
        if hands:
            self.hands = self.hands2descs(hands)
        else:
            self.hands = np.zeros((0, self.nHDesc), np.uint8)
    
    

    def addComb(self, cards, n_in_hand):
        """
        Add all hands created from cards taken
        n_in_hand at a time
        
        cards - list of cards
        n_in_hand - length of hand
        """
        ncomb = self.nComb(len(cards), n_in_hand)
        old_number = len(self.hands)
        new_number = old_number + ncomb
        newHands = np.empty((new_number, self.nHDesc), dtype=np.uint8)
        for i in xrange(old_number):
            newHands[i] = self.hands[i]     # row == card
 
        # Generate new combination hands
        new_combs = self.combs(cards, n_in_hand)
        new_combs_len = len(new_combs)
        item_size = len(new_combs[0])
        
        for i in xrange(new_combs_len):
            cc = new_combs[i]
            newHands[i+old_number] = cc
                   
        # Add in new cards,
        self.hands = newHands
        return self.hands
    
    def descCmp(self, desc1, desc2, direction = None, lowFlushStrait=None):
        """
        return >,<,== zero if desc1 >,<,== desc2
        reversed if direction == LOW
        """
        if direction is None:
            direction = self.direction
        if lowFlushStrait is None:
            lowFlushStrait = self.lowFlushStrait
        res = 0
        for i,byte1 in enumerate(desc1):
            byte2 = desc2[i]
            if i == 0 and direction == LOW and self.lowFlushStrait:
                nib1 = byte1 >> 4
                if nib1 == 4 or nib1 == 5:
                    byte1 &= 0xFF
                nib2 = byte2 >> 4
                if nib2 == 4 or nib2 == 5:
                    byte2 &= 0xFF
                
            if byte1 != byte2:
                if self.direction == LOW:
                    res =  int(byte2)-int(byte1)
                else:
                    res =  int(byte1)-int(byte2)
                break
        return res
            
            
    def bestHand(self):
        if len(self.hands) == 0:
            raise AssertionError("No hands available")
        best_hand_desc = self.hands[0]
        for other_desc in list(self.hands):
            if self.descCmp(other_desc, best_hand_desc) > 0:
                best_hand_desc = other_desc
        best_hand = self.desc2hand(best_hand_desc)
        return best_hand
    
    def cards2desc(self, cards):
        """
        Convert card group to hand description
        numpy array
        [0]: 4bits - hand primary 1-9 nothing-royal flush
             4bits - first tie breaker e.g. rank  for 4,3of,
             See PokerHandHL._set_score.
        [1]: 4bits second tie breaker, if one
             4bits third tie breaker, if one
        [2-6]: card index + 64*(1 if hoard) + 128*(1 if hidden)
        """
        hand = PokerHandHL(cardlist=cards,
                           direction=self.direction,
                           lowFlushStrait=self.lowFlushStrait
                           )
        hand_desc = self.hand2desc(hand)
        return hand_desc
    
    
    def hand2desc(self, hand):
        """
        Convert card to card description
        """
        hand_score = hand.getScore()

        hand_desc = empty((self.nHDesc), dtype=np.uint8)
        prime_score = hand_score[0]
        tiebreaks = [0] * self.nTiebreaks
        if prime_score == 0:
            for i,hs in enumerate(hand_score[1]):       # nothing
                tiebreaks[i] = hs     
        elif prime_score == 1:                          # 1 pair    
            tiebreaks[0] = hand_score[1]
            for i,hs in enumerate(hand_score[2]):
                tiebreaks[i+1] = hs     
        elif prime_score == 2:                          # 2 pair    
            tiebreaks[0] = hand_score[1]
            tiebreaks[1] = hand_score[2]
            for i,hs in enumerate(hand_score[3]):
                tiebreaks[i+2] = hs     
        elif prime_score == 3:                          # 3 of akind                              
            tiebreaks[0] = hand_score[1]
            for i,hs in enumerate(hand_score[2]):
                tiebreaks[i+1] = hs     
        elif prime_score == 4:                          # stait   
            tiebreaks[0] = hand_score[1]
        elif prime_score == 5:                          # flush    
            for i,hs in enumerate(hand_score[1]):
                tiebreaks[i] = hs     
        elif prime_score == 6:                          # full house    
            tiebreaks[0] = hand_score[1]
            tiebreaks[1] = hand_score[2]
        elif prime_score == 7:                          # 4 of a kind
            tiebreaks[0] = hand_score[1]
            for i,hs in enumerate(hand_score[2]):
                tiebreaks[i+1] = hs     
        elif prime_score == 8:              # strait flush   
            tiebreaks[0] = hand_score[1]
        elif prime_score == 9:              # royal flush
            pass
        else:
            raise AssertionError("Unrecognized prime score({})".format(prime_score))    

        # Create list of nibbles
        hand_desc_nibs = [prime_score]
        hand_desc_nibs += tiebreaks
        
        desc_idx = 0
        for i,nib in enumerate(hand_desc_nibs):
            if i % 2 == 0:
                desc_byte = nib << 4        # First of two
            else:
                desc_byte += nib            # Add second of two
                hand_desc[desc_idx] = desc_byte
                desc_idx += 1               # Go to next output byte

        cards = hand._cards
        for i, card in enumerate(cards):
            hand_desc[i+self.cardStart] = card.index()

        return hand_desc


    def hands2descs(self, hands):
        """
        Convert list of hands to np.ndarray of descriptions
        """
        nds = np.empty((len(hands), self.nHDesc), np.uint8)
        for i,hand in enumerate(hands):
            hand_desc = self.hand2desc(hand)
            nds[i] = hand_desc
        return nds    

    def nibs(self, desc):
        """
        Return list of 4bit nibbles (half byte) for the hand score
        Used mostly for debugging and diagnostics
        """
        nibs = []
        for i in xrange(self.nScoreBytes):
            byte = desc[i]
            nib1 = byte >> 4
            nib2 = byte & 0xF
            nibs.append(nib1)
            nibs.append(nib2)
        return nibs
        
    
    def desc2hand(self, desc):
        """
        Returns: PokerHandHL, given numpy description array
        """
        cards = []
        for i in range(PokerCardBase.cardsInHand()):
            cidbyte = desc[self.cardStart+i]
            is_hidden = cidbyte & 0x80
            is_board = cidbyte & 0x40 
            index = cidbyte & 0x3F
            card = PokerCard(index=index)
            if is_hidden != 0:
                card.setHidden()
            if is_board != 0:
                card.setBoard()
            cards.append(card)
            
        hand = PokerHandHL(cardlist=cards,
                           direction=self.direction,
                           lowFlushStrait=self.lowFlushStrait)
        return hand
    
        
        
    def getHand(self, npos):
        """
        Returns: nth hand, starting at 1
        """
        if npos > len(self.hands):
            raise AssertionError(
                "npos({} > number of hands({}".format(
                    npos, len(self.hands)))
             
        hand_desc = self.hands[npos-1]
        hand = self.desc2hand(hand_desc)
        return hand
    
        
    def combs(self, cards, n_in_hand):
        """
        create compact set of hand descriptions of combinations
        of cards taken n__in_hand at a time
        Returns numpy arrays of hand description arrays
        """
        """ TBD self made combinations to minimize storage """
        if len(cards) == n_in_hand:
            hand_combs_list = [cards]        # Workaround for combination issue
        else:
            hand_combs = itertools.combinations(cards, n_in_hand)
            hand_combs_list = list(hand_combs)
        
        nhands = len(hand_combs_list)
        hands_desc = np.empty((nhands, self.nHDesc), dtype=np.uint8)
        i = 0
        print("list(hand_combs):{}".format(hand_combs_list))
        for cs in list(hand_combs_list):
            hands_desc[i] = self.cards2desc(cs)
            i += 1
        return hands_desc
    
    
    def nComb(self, n, k):
        """
        Number of subgroups of nitem taken k at a time
        From dheerosaur
        """
        import operator as op
        k = min(k, n-k)
        if k == 0: return 1
        numer = reduce(op.mul, xrange(n, n-k, -1))
        denom = reduce(op.mul, xrange(1, k+1))
        return numer//denom
            
                
    def betEqWorse(self, hand):
        """
        Using tuples of short names to save space
        Returns (better, equal, less) numbers of other hands
        """
        nbetter = 0
        nequal = 0
        hand_desc = self.hand2desc(hand)
        for i, other_desc in enumerate(self.hands):
            cmpval = self.descCmp(other_desc, hand_desc)
            if cmpval > 0:
                nbetter += 1
            elif cmpval == 0:
                nequal += 1
            else:
                break
        nworse = len(self.hands) - nbetter - nequal
        return (nbetter, nequal, nworse)
            
        return None


    def nHands(self):
        return len(self.hands)
    
    
"""
Stanalone test / exercise:
"""
if __name__ == "__main__":
    from PyTrace import PyTrace
    trace_str = ""
    ###trace_str = "prob"
    PyTrace(flagStr=trace_str)
    all_hands = []      # Store all hands
    def testit(cardstr):
        cards = PokerCard.cards(cardstr)
        
        hand_comb = PokerComb(direction=HIGH, lowFlushStrait=None)
        hand_desc = hand_comb.cards2desc(cards)
        hand_desc_nibs = hand_comb.nibs(hand_desc)
        hand = hand_comb.desc2hand(hand_desc)
        all_hands.append(hand)          # Store for cumulative tests
        hand_str = hand.showCards()
        print("card str: {}  cards:{}  desc_nibs: {} desc_str: {} ".format(cardstr, hand_str, hand_desc_nibs, hand_desc))

    def test_end():
        hand_comb = PokerComb(hands=all_hands, direction=HIGH)
        best_hand = hand_comb.bestHand()
        print("best_hand={}({})".format(best_hand.show_value(full=True), best_hand.showCards()))
        nbetter, neq, nworse = hand_comb.betEqWorse(best_hand)
        print("\tbetter={}, equal={}, worse={}".format(nbetter, neq, nworse))
        print("Low hands")
        hand_comb_low = PokerComb(hands=all_hands, direction=LOW)
        best_hand_low = hand_comb_low.bestHand()
        print("best_hand={}({})".format(best_hand_low.show_value(full=True), best_hand_low.showCards()))
        nbetter, neq, nworse = hand_comb_low.betEqWorse(best_hand)
        print("\tbetter={}, equal={}, worse={}".format(nbetter, neq, nworse))
        
    """ """       
    testit("2c 3h 4s 5d 7c")
    testit("2c 3h 4s 5d 8c")
    testit("2c 2h 4s 5d 7c")
    testit("2c 2h 4s 5d 8c")
    testit("2c 2h 4s 4s 7c")
    testit("2c 2h 4s 4s 8c")
    testit("2c 2h 2s 4s 7c")
    testit("2c 2h 2s 5s 7c")
    testit("2c 3h 4s 5d 6c")
    testit("3h 4s 5d 6c 7c")
    testit("2c 3c 4c 5c 7c")
    testit("2c 3c 4c 5c 8c")
    testit("4c 4h 4s 5d 5c")
    testit("4c 4h 4s 6d 6c")
    testit("2c 2h 2s 2d 7c")
    testit("2c 2h 2s 2d 8c")
    """ """
    testit("2s 3s 4s 5s 6s")
    testit("3s 4s 5s 6s 7s")
    testit("As Ks Qs Js 10s")
    
    test_end()
    
    
    """ Deck based testing
    from PokerDeck import PokerDeck
    deck = PokerDeck()
    nhands = 5
    nperhand = 5
    for i in range(nhands):
        cards = []
        for j in range(5):
            cards.append(deck.draw())
        hands_comb = PokerComb(cards, nperhand)
        best_hand = hands_comb.bestHand()
        print("best_hand:{}".format(best_hand))
    
    
    print("Test is done.")
    """