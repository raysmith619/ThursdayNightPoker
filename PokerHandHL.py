'''
Created on Mar 14, 2017

@author: raysmith

Library Release 0.1

Based on work by Paul Griffiths

Distributed under the terms of the GNU General Public License.
http://www.gnu.org/licenses/

'''
from __future__ import print_function
from collections import namedtuple

from PyTrace import tR

from PokerCardBase import rank_string
from PokerCardBase import PokerCardBase
from PokerHandBase import PokerHandBase
from PokerHandDirection import PokerHandDirection

# Non-public named tuples

_HSLF = namedtuple("HSLF", ["fstr", "fargs"])

# pylint raises a convention warning for _HandInfo
# rather than _HANDINFO, but we use named tuples
# in a similar way to classes, so we follow that
# naming convention instead and disable the message.
#
# pylint: disable=C0103

_HandInfo = namedtuple("HandInfo", ["high_card", "low_pair", "high_pair",
                                    "three", "four", "flush", "straight",
                                    "straight_flush", "royal_flush"])

# pylint: enable=C0103

# Puplic Constants

# Non-public constants

_HIGH_CARD = 0
_LOW_PAIR = 1
_HIGH_PAIR = 2
_THREE = 3
_FOUR = 4
_FLUSH = 5
_STRAIGHT = 6
_STRAIGHTFLUSH = 7
_ROYALFLUSH = 8

_HAND_STRINGS_SHORT = [
    "HI", "PR", "TP", "TK", "ST",
    "FL", "FH", "FK", "SF", "RF"
]
_HAND_STRINGS_NORMAL = [
    "High card", "Pair", "Two pair", "Three of a kind",
    "Straight", "Flush", "Full House", "Four of a kind",
    "Straight flush", "Royal flush"
]
_HAND_STRINGS_LONG = [
    _HSLF("{0} high", (_HIGH_CARD,)),
    _HSLF("Pair of {0}s", (_LOW_PAIR,)),
    _HSLF("Two pair, {0}s over {1}s", (_HIGH_PAIR, _LOW_PAIR)),
    _HSLF("Three of a kind", None),
    _HSLF("Straight", None),
    _HSLF("Flush", None),
    _HSLF("Full house, {0}s full of {1}s", (_THREE, _LOW_PAIR)),
    _HSLF("Four of a kind", None),
    _HSLF("Straight flush", None),
    _HSLF("Royal flush", None)
]


# Class

class PokerHandHL(PokerHandBase):

    """Implements a five card regular poker hand class.

    Public methods:
    __init__(numcards, namelist)
    show_value(short, full)
    video_winnings(bet, easy)

    """
    """ class constants """
    HIGH = PokerHandDirection.HIGH
    LOW = PokerHandDirection.LOW

    """ class functions """
    @staticmethod
    def cmpCards(cards1, cards2, direction=HIGH, lowFlushStrait=True):
        h1 = PokerHandBase(cards1, direction=direction, lowFlushStrait=lowFlushStrait)
        h2 = PokerHandBase(cards2, direction=direction, lowFlushStrait=lowFlushStrait)
        return h1.cmp(h2)
        
    _vp_returns_normal = [0, 1, 2, 3, 4, 6, 9, 25, 50, 800]
    _vp_returns_easy = [0, 2, 3, 4, 15, 20, 50, 100, 250, 2500]

    def __init__(self, numcards=PokerCardBase.cardsInHand(), namelist=None, cardlist=None,
                direction=HIGH, lowFlushStrait=None):

        """Initializes a PokerHandBase instance.


        Arguments:
        direction - HIGH, LOW, HIGH_LOW => HIGH
        lowFlushStrait - don't consider flushes, straits when low low
        """

        
        self._singles = []
        self._hand_info = None

        if lowFlushStrait == None:
            if direction==PokerHandDirection.LOW:
                lowFlushStrait = True
            else:
                lowFlushStrait = False
        self.direction = direction
        self.lowFlushStrait = lowFlushStrait
        
        
            
        PokerHandBase.__init__(self, numcards=numcards,
                               namelist=namelist, cardlist=cardlist,
                               direction=direction)

    # Public methods


    def copy(self):
        """
        Return a deep copy
        """
        ph = PokerHandHL(self, deck=self.deck,
                       numcards=self.numcards,
                       namelist=None, cardlist=None,
                       direction=self.direction,
                       lowFlushStrait=self.lowFlushStrait)
        return ph


    def simpleString(self, short=True, full=False):
        """
        Return simple string, including cards
        """
        hand_str = self.show_value(short=short, full=full)
        hs = "\t{}".format(hand_str)
                        # Separate player cards and board cards
        player_str = ""
        board_str = ""
        cards = self._cards
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
        return hs

    
    def show_value(self, short=False, full=True):

        """Returns a string containing the name of, and
        sometimes more information about, a poker hand.

        Arguments:
        short -- set to True to receive two character value
        full -- set to True to include other information, e.g.
        when full is True "Full house" becomes "Full house, aces
        full of threes" or similar.

        Returns: string object containing hand evaluation.

        """

        if short:
            return _HAND_STRINGS_SHORT[self._score[0]]
        elif full:
            hsl = _HAND_STRINGS_LONG[self._score[0]]
            if hsl.fargs:
                arg_list = [rank_string(self._hand_info_item(item))
                            for item in hsl.fargs]
                return hsl.fstr.format(*arg_list).capitalize()
            else:
                return hsl.fstr.format()
        else:
            return _HAND_STRINGS_NORMAL[self._score[0]]

    
    def showCards(self):
        """
        Return string showing cards
        """
        card_str = ""
        for card in self.get_list():
            cs = card.name_string(short=True)
            if card_str != "":
                card_str += " "
            card_str += cs
        return card_str
            
    def video_winnings(self, bet, easy=False):
        return None         # Not implemented 

    # Non-public methods

    def _hand_info_item(self, item_index):

        """Returns the value of a hand info item."""

        item_dict = {
            _HIGH_CARD: 0 if not self._singles else self._singles[0],
            _LOW_PAIR: self._hand_info.low_pair,
            _HIGH_PAIR: self._hand_info.high_pair,
            _THREE: self._hand_info.three,
            _FOUR: self._hand_info.four,
            _FLUSH: self._hand_info.flush,
            _STRAIGHT: self._hand_info.straight,
            _STRAIGHTFLUSH: self._hand_info.straight_flush,
            _ROYALFLUSH: self._hand_info.royal_flush
        }

        return item_dict[item_index]

    def _evaluate(self):

        """Evaluates a poker hand and stores information
        necessary for later comparison.
        If direction is Low and lowFlushStrait is True
        ignore straights and flushes

        """

        # Identify singles, pairs, threes and fours

        (self._singles, low_pair,
         high_pair, three, four) = self._get_rank_matches()

        high_card = 0
        if (self.direction != PokerHandDirection.LOW) or  not self.lowFlushStrait:
            # Check for a straight, and set the high card

            straight, high_card = self._check_straight()

            # Check for a flush

            flush = self._check_flush()
        else:
            straight = False
            flush = False

        # Check for a straight and royal flush

        straightflush = False
        royal = False

        if flush and straight:
            straightflush = True
            if high_card == 14:
                royal = True

        # Populate HandInfo instance attribute and set score

        self._hand_info = _HandInfo(high_card, low_pair,
                                    high_pair, three,
                                    four, flush, straight,
                                    straightflush, royal)
        self._set_score()

    def _set_score(self):

        """Stores a score for the hand, to enable us to
        compare them, later. The score is a list,
        representing - from left to right - the things
        that determine a winning poker hand. For example,
        for a three of a kind, first compare the overall
        category (e.g. a three of a kind (4) always beats
        a pair (2) but never beats a flush (6)). If we
        have two threes of a kind, then compare the ranks
        of the threes (self.three). If the ranks of the
        threes are the same (this is possible in reality
        if wild cards or community cards are used) then
        look through the remaining cards (self._singles)
        for the hightest card. Because of the way Python
        compares lists, we can set up the score like this
        and have Python do almost all of the dirty work
        for us just using comparison operators.

        """

        if self._hand_info.royal_flush:
            self._score = [9]
        elif self._hand_info.straight_flush:
            self._score = [8, self._hand_info.high_card]
        elif self._hand_info.four:
            self._score = [7, self._hand_info.four, self._singles]
        elif self._hand_info.three and self._hand_info.low_pair:
            self._score = [6, self._hand_info.three, self._hand_info.low_pair]
        elif self._hand_info.flush:
            self._score = [5, self._ranks(reverse=True)]
        elif self._hand_info.straight:
            self._score = [4, self._hand_info.high_card]
        elif self._hand_info.three:
            self._score = [3, self._hand_info.three, self._singles]
        elif self._hand_info.high_pair:
            self._score = [2, self._hand_info.high_pair,
                           self._hand_info.low_pair, self._singles]
        elif self._hand_info.low_pair:
            self._score = [1, self._hand_info.low_pair, self._singles]
        else:
            self._score = [0, self._singles]

    def _get_rank_matches(self):

        """Returns information about rank properties."""

        rank_counts = self._get_rank_counts()

        singles = []
        low_pair = 0
        high_pair = 0
        three = 0
        four = 0

        for val in sorted(rank_counts):
            if rank_counts[val] == 1:
                singles.append(val)
            elif rank_counts[val] == 2:
                if not low_pair:
                    low_pair = val
                else:
                    high_pair = val
            elif rank_counts[val] == 3:
                three = val
            elif rank_counts[val] == 4:
                four = val
            elif rank_counts[val] == 5:
                raise NotImplementedError("Five of a kind not implemented.")

        singles.reverse()

        return [singles, low_pair, high_pair, three, four]

    def _check_straight(self):

        """Checks for a straight.

        Returns a two-element tuple. The first element is
        True if a straight is found. The second element
        represents the high card if a straight is found, or
        None if a straight is not found. This information
        is important because an A-2-3-4-5 (a "wheel straight")
        is the only time in a standard poker hand where the
        ace is treated as the low card, so we'd need to know
        that the high card was five, in this instance.

        """

        sorted_ranks = self._ranks(sort=True)
        high_card = sorted_ranks[-1]
        straight = False

        if len(set(sorted_ranks)) == len(sorted_ranks):
            if sorted_ranks[-1] - sorted_ranks[0] == PokerCardBase.cardsInStrait()-1:
                straight = True
            elif sorted_ranks[-1] - sorted_ranks[-2] == PokerCardBase.cardsInStrait()-1:      # A,2,3,4,... ???
                straight = True
                high_card = PokerCardBase.cardsInStrait()

        return (straight, high_card)

    def _check_flush(self):

        """Checks if we have a flush, returns True if we
        do and false if we don't.

        """

        if PokerCardBase.cardsInHand in self._get_suit_counts().values():
            return True
        else:
            return False

    def _cards_changed(self):

        """Override superclass function and evaluate hand."""

        PokerHandBase._cards_changed(self)
        if len(self._cards) == PokerCardBase.cardsInHand():
            self._evaluate()

    