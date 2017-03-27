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
                

    @staticmethod
    def tupleCmp(tuphand1, tuphand2):
        """
        Using tuples (XX,XX....) to save space ==> using namelist
        Compare two hands based on their direction
        which must be the same
        """
        hand1 = PokerHandHL(namelist=list(tuphand1))
        hand2 = PokerHandHL(namelist=list(tuphand2))
        return hand1.cmp(hand2)
                

    @staticmethod
    def handGroupHighCmp(hand_cards1, hand_cards2):
        """
        Calculate a ordered integer value indicating poker high hand value
        given a list of cards.
        hand - list of cards
        """
        return PokerHandHL.cmpCards(hand_cards1, hand_cards2,
                                    direction=HIGH)
                
    @staticmethod
    def handGroupLowCmp(hand_cards1, hand_cards2):
        """
        Calculate a ordered integer value indicating poker high hand value
        given a list of cards.
        hand - list of cards
        """
        return PokerHandHL.cmpCards(hand_cards1, hand_cards2,
                                    direction=LOW)
                

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
        hands = self.getHands(player=player, sort=True)
        if nHand is None:
            nHand = 1
        count = 0    
        for hand in hands:
            count += 1
            if count > nHand:
                break
            
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
        Determine what hands are currently makbeable
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
        hand_groups = []
        for board_group in board_groups:
            deck_hand_cards = deck_cards[:]        # copy group
            deck_hand_cards.extend(board_group)      # Possibly more than 5
            if len(deck_hand_cards) >= self.deal.handSize():
                hand_comb = itertools.combinations(deck_hand_cards,
                                                    self.deal.handSize())
                hand_groups.extend(hand_comb)
        hands = self.groups2tuples(hand_groups)
        hands = sorted(hands, cmp=PokerHands.tupleCmp, reverse=True)
        return hands

            
    def getOtherHandtuples(self, player=None,
                direction=None,
                sort=True):
        """
        list of XX, tuples because of space
        Determine what hands are currently makbeable
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
        hand_groups = []
        for board_group in board_groups:
            deck_hand_cards = deck_cards[:]        # copy group
            deck_hand_cards.extend(board_group)      # Possibly more than 5
            if len(deck_hand_cards) >= self.deal.handSize():
                hand_comb = itertools.combinations(deck_hand_cards,
                                                    self.deal.handSize())
                hand_groups.extend(hand_comb)
        hands = self.groups2tuples(hand_groups)
        hands = sorted(hands, cmp=PokerHands.tupleCmp, reverse=True)
        return hands

            
    def getHands(self, player=None,
                 direction=None,
                 sort=True):
        """
        Determine what hands are currently makeable given
        the player's cards and community cards
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
        board_groups = board.getGroups()
        hand_groups = []
        for board_group in board_groups:
            hand_cards = player_cards[:]        # copy group
            hand_cards.extend(board_group)      # Possibly more than 5
            if len(hand_cards) >= self.deal.handSize():
                hand_comb = itertools.combinations(hand_cards,
                                                    self.deal.handSize())
                hand_groups.extend(hand_comb)
        hands = self.groups2hands(hand_groups)
        hands1 = sorted(hands, cmp=PokerHands.handCmp, reverse=True)
        return hands1

            
    def getHandtuples(self, player=None,
                 direction=None,
                 sort=True):
        """
        list of XX, tuples because of space
        Determine what hands are currently makeable given
        the player's cards and community cards
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
        board_groups = board.getGroups()
        hand_groups = []
        for board_group in board_groups:
            hand_cards = player_cards[:]        # copy group
            hand_cards.extend(board_group)      # Possibly more than 5
            ###self.dupCheck(hand_cards)
            if len(hand_cards) >= self.deal.handSize():
                hand_comb = itertools.combinations(hand_cards,
                                                    self.deal.handSize())
                hand_groups.extend(hand_comb)
        hands = self.groups2tuples(hand_groups)
        hands = sorted(hands, cmp=PokerHands.tupleCmp, reverse=True)
        return hands

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
    
    
    def groups2tuples(self, hand_groups):
        """
        Using XX (short name) tuples to save space
        Convert list of card groups, each of handSize, to list of hands
        """
        hands = []
        for group in hand_groups:
            short_names = []
            for card in group:
                short_names.append(card.name_string(short=True))
            ###self.dupCheck(short_names, prefix="groups2tupels hand")            
            hand_tuple = tuple(short_names)
            ###self.dupCheck(hand_tuple, prefix="groups2tupels tuple")            
            hands.append(hand_tuple)
        return hands
    
    
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
        hands = self.getHandtuples(player=player)    # list of XX, tuples because of space
        other_hands = self.getOtherHandtuples(player=player)    # list of XX, tuples because of space
        len_hands = len(hands)
        len_other = len(other_hands)
        prob = 0
        if len_hands > 0 and len_other > 0:
            best_hand = hands[0]
            nbetter, nequal, nworse = self.betEqWorse(best_hand, other_hands)   # list of XX tuples
            prob = float(nworse)/len_other
        elif len_other == 0:
            prob = .1
        if inclNumbers:
            prob_str = "{:1.2f} (better,eq,worse: {}, {}, {})".format(
                        prob, nbetter, nequal, nworse)
        else:
            prob_str = "{:1.2f}".format(prob)
        if tR('prob'):
            our_hands = self.getHands(player=player)
            our_best_hand = our_hands[0]
            card_str = our_best_hand.simpleString(short=False, full=True)
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
    from PokerTable import PokerTable
    trace_str = ""
    ###trace_str = "prob"
    PyTrace(flagStr=trace_str)
    testgame = "toy"
    ###testgame = "44"
    if testgame == "toy":
        deckMain = PokerDeck(nsuit=3, ninsuit=5)  # SHORT to reduce complexity
        table = PokerTable(nPlayer=2, deck=deckMain)
        deal = PokerDeal(table, gameName=testgame)
    elif testgame == "toy2":
        testgame = "toy"
        deckMain = PokerDeck(nsuit=4, ninsuit=8)  # SHORT to reduce complexity
        table = PokerTable(nPlayer=2, deck=deckMain)
        deal = PokerDeal(table, gameName=testgame)
    else:
        deckMain = PokerDeck()  # SHORT to reduce complexity
        table = PokerTable(deck=deckMain)
        deal = PokerDeal(table, gameName=testgame)
        
    poker_hands_high = PokerHands(deal, direction=HIGH)
    poker_hands_low = PokerHands(deal, direction=LOW, lowFlushStrait=True)
    player = table.players[0]
    while deal.hasMorePlays():
        deal.play()
        poker_hands_high.displaySimpleHands(player=player, short=False, full=True, nHand=1)
        print("\nlow hands:")
        poker_hands_low.displaySimpleHands(player=player, short=False, full=True, nHand=1)
    print("Hand is done.")