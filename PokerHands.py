'''
Construct, Manipulate, and Evaluate poker hands
Created on Mar 14, 2017

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
from PokerComb import PokerComb

HIGH = PokerHandDirection.HIGH
LOW = PokerHandDirection.LOW
HIGH_LOW = PokerHandDirection.HIGH_LOW

class PokerHands(object):
    '''
    Poker Hand evaluation - player
    Embeds direction
    '''

    @staticmethod
    def handCmp(hand1, hand2):
        """
        Compare two hands based on their direction
        which must be the same
        """
        return hand1.cmp(hand2)
                

    def __init__(self, deal, direction=HIGH, lowFlushStrait=None):
        '''
        Constructor
        playerHands
        '''
        self.deal = deal
        self.deck = deal.deck
        if lowFlushStrait is None:
            if direction==LOW:
                lowFlushStrait = True
            else:
                lowFlushStrait = False
        self.direction = direction
        self.lowFlushStrait = lowFlushStrait

    
    def displaySimpleHands(self, player=None,
                        showCards=False,
                        short=None, full=None,
                        nHand=None
                        ):
        """
        Simple, textual display of player's
        hand(s) possible, given the player's
        cards and the visible board cards
        """
        if player is None:
            raise NotImplementedError("player=None not supported yet")
        hand_combs = self.getHands(player=player)
        if nHand is None:
            nHand = 1
        count = 0    
        for i in xrange(hand_combs.nHands()):
            count += 1
            if count > nHand:
                break
            hand = hand_combs.getHand(1)
            hand_str = hand.show_value(short=short, full=full)
            hs = "\t{}".format(hand_str)
                        # Separate player cards and board cards
            player_str = ""
            board_str = ""
            cards = hand._cards
            for card in cards:
                if card.inBoard:
                    if board_str != "":
                        board_str += " "
                    board_str += card.simpleString(showMe=True, isMe=True, short=True)
                else:
                    if player_str != "":
                        player_str += " "
                    player_str += card.simpleString(showMe=True, isMe=True, short=True)
                       
            hs += " " + player_str + " Board: " + board_str
            prob = self.winProb(player=player,inclNumbers=True)
            hs += " {}".format(prob)
            print(hs)

            
    def getOtherHands(self, player=None,
                direction=None,
                sort=True):
        """
        Determine what hands are currently makeable
        by any other player than the given player
        given the player's cards and community cards
        player - current player
        direction - High, Low, High_Low
        sorted - True == sort hands from most valued to least
        """
        if direction is None:
            direction = self.direction
        if direction is None:
            direction = self.direction = self.deal.direction
            
        player_cards = player.getCards()
        board = self.deal.getBoard()
        board_cards = board.getCards()
        known_cards = player_cards
        known_cards.extend(board_cards)
        deck_cards = self.subCards(known_cards)  # get possible in deck
        board_groups = board.getGroups()
        hand_comb = PokerComb(direction=direction,
                              lowFlushStrait=self.lowFlushStrait)
        for board_group in board_groups:
            hand_comb.addCombGroup(deck_cards, board_group, self.deal.handSize())
        hand_comb.sortCombIf()
        return hand_comb

            
    def getHands(self, player=None,
                 direction=None):
        return self.deal.getHands(player=player, direction=direction)


    def dupCheck(self, hand_cards, prefix=None):
        """ Looks for duplicate cards in hand
            if hand_cards is a tuple, it will be converted to a list of cards for the check
        """
        if prefix is None:
            prefix="dupCheck"
                                    # Check if tuple and convert to cards
        if isinstance(hand_cards, tuple):
            new_cards = []
            names = list(hand_cards) 
            for name in names:
                new_cards.append(PokerCard(name=name))
            hand_cards = new_cards
            card_count = Counter()
            for card in hand_cards:
                if card in card_count:
                    print("{}:getHandTupels: Duplicate card {}".format(prefix, card))
                    print("Problem")
                card_count[card] += 1


    def subCards(self, cards, base=None):
        """
        Return a list of cards equal to the base
        list with the cards removed
        cards - list of cards not to return
        base - cards from which to select
           None - use whole 52 card list
        """
        if base is None:
            base_hash = self.deal.deck._deckHash
        else:
            base_hash = Counter()
            for card in base:
                base_hash[card.index()] = card
                
        cards_hash = Counter()
        for card in cards:
            cards_hash[card.index()] = card
            
        diff_cards = []
        for card_index in base_hash:
            base_card = base_hash[card_index]
            if card_index not in cards_hash:
                diff_cards.append(base_card)
                
        return diff_cards
    
    
    def groups2hands(self, hand_groups):
        """
        Convert list of card groups, each of handSize, to list of hands
        """
        hands = []
        for group in hand_groups:
            hand = PokerHandHL(cardlist=list(group), direction=self.direction, lowFlushStrait=self.lowFlushStrait)
            hands.append(hand)            
        return hands

    def winProb(self, player=None, inclNumbers=True, direction=None):
        """
        Winning probablity, given player's knwlege
        inclNumbers - include (beats of other_hands)
        """
        if direction is None:
            direction = self.direction
        if direction is None:
            direction.PokerHandDirection.HIGH
        hands_comb = self.getHands(player=player)
        other_hands_comb = self.getOtherHands(player=player)
        best_hand = hands_comb.bestHand()
        nbetter, nequal, nworse = other_hands_comb.betEqWorse(
                best_hand)   # list of XX tuples
        
        prob = float(nworse)/(nbetter+nequal+nworse)
        prob_tie = float(nequal)/(nbetter+nequal+nworse)
        prob_str = "{:.3f}({:.3f})".format(prob,prob_tie)

        if inclNumbers:
            prob_str += " (>,==,<: {}, {}, {})".format(
                        nbetter, nequal, nworse)
        if tR('prob'):
            card_str = best_hand.simpleString(short=False, full=True)
            print("{} win prob: {}".format(card_str, prob_str))
        return prob_str

    def firstLessEqual(self, hand, other_hands):
        """
        Using tuples of short names to save space
        Give index of first hand less than or equal
        to hand.  Entries less than index beat hand
        """
        for i, other in enumerate(other_hands):
            if other <= hand:
                return i
            
        return None
    
"""
Stanalone test / exercise:
"""
if __name__ == "__main__":
    from PyTrace import PyTrace
    from PokerTable import PokerTable
    trace_str = ""
    ###trace_str = "prob"
    PyTrace(flagStr=trace_str)
    testgame = "44"
    testgame = "toy"
    if testgame == "toy":
        deal = PokerDeal(gameName=testgame)
    elif testgame == "toy2":
        testgame = "toy"
        table = PokerTable(nPlayer=2)
        deal = PokerDeal(table, gameName=testgame)
    else:
        deckMain = PokerDeck()  # SHORT to reduce complexity
        table = PokerTable(deck=deckMain)
        deal = PokerDeal(table, gameName=testgame)
        
    poker_hands_high = PokerHands(deal, direction=HIGH)
    poker_hands_low = PokerHands(deal, direction=LOW, lowFlushStrait=True)
    player = deal.getPlayer(1)
    while deal.hasMorePlays():
        deal.play()
        poker_hands_high.displaySimpleHands(player=player, short=False, full=True, nHand=1)
        print("\nlow hands:")
        poker_hands_low.displaySimpleHands(player=player, short=False, full=True, nHand=1)
    print("Hand is done.")