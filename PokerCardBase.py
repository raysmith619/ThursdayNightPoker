"""Playing card module.

Library Release 1.1

Copyright 2017
Based on Paul Griffiths card.py
On reflection, pcard.py might have been used unchanged.

Email: raysmith@alum.mit.edu

Distributed under the terms of the GNU General Public License.
http://www.gnu.org/licenses/

"""


from __future__ import division


# Public constants

ACE = 1
TWO = 2
THREE = 3
FOUR = 4
FIVE = 5
SIX = 6
SEVEN = 7
EIGHT = 8
NINE = 9
TEN = 10
JACK = 11
QUEEN = 12
KING = 13

CLUBS = 0
HEARTS = 1
SPADES = 2
DIAMONDS = 3

# Non-public constants

_ALLOWABLE_RANK_STRINGS = {
    "ace": 14, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "jack": 11, "queen": 12, "king": 13,
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7,
    "8": 8, "9": 9, "10": 10
}
_ALLOWABLE_SUIT_STRINGS = {
    "clubs": 0, "hearts": 1, "spades": 2, "diamonds": 3
}
_RANK_SHORT_STRINGS = {
    1: "A", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6",
    7: "7", 8: "8", 9: "9", 10: "10", 11: "J", 12: "Q",
    13: "K", 14: "A"
}
_RANK_LONG_STRINGS = {
    1: "ace", 2: "two", 3: "three", 4: "four",
    5: "five", 6: "six", 7: "seven", 8: "eight",
    9: "nine", 10: "ten", 11: "jack", 12: "queen",
    13: "king", 14: "ace"
}
_SUIT_LONG_STRINGS = ["clubs", "hearts", "spades", "diamonds"]


# Public functions


def get_rank_integer(rank):

    """Returns a valid integer rank from an input of unspecified type."""

    if rank in range(1, PokerCardBase.nInSuit):
        return PokerCardBase.nInSuit if rank == 1 else rank
    elif isinstance(rank, basestring):
        if not rank:
            raise ValueError("Missing rank value.")

        for key in _ALLOWABLE_RANK_STRINGS.iterkeys():
            if key.startswith(rank.lower()):
                return _ALLOWABLE_RANK_STRINGS[key]

    raise ValueError("Invalid rank value '{0}'".format(rank))


def get_suit_integer(suit):

    """Returns a valid integer suit from an input of unspecified type."""

    if suit in range(0, PokerCardBase.nSuit):
        return suit
    elif isinstance(suit, basestring):
        if not suit:
            raise ValueError("Missing suit value.")

        for key in _ALLOWABLE_SUIT_STRINGS.iterkeys():
            if key.startswith(suit.lower()):
                return _ALLOWABLE_SUIT_STRINGS[key]

    raise ValueError("Invalid suit value '{0}'".format(suit))


def rank_string(rank, short=False, capitalize=False):

    """Returns a string representing a specified rank,
    e.g. "ace", "five", "jack".

    Arguments:
    rank -- an integer from 1 to nInSuit, inclusive, representing the
    rank for which a string is to be returned. Aces can be passed
    in either as 1 or nInSuit. 11 is jack, 12 is queen, and 13 is king.
    short -- set to True to output short strings, i.e. "A"
    instead of "ace", "4" instead of "four", "J" instead
    of "jack".
    capitalize -- set to True to capitalize the first letter
    of the word (long strings only).

    """

    if rank not in range(1, PokerCardBase.nInSuit+2):
        raise ValueError("Invalid rank value '{} not in (1 to {})'".format(rank,
                        PokerCardBase.nInSuit+1))

    if short:
        outstr = _RANK_SHORT_STRINGS[rank]
    else:
        outstr = _RANK_LONG_STRINGS[rank]

    if capitalize:
        outstr = outstr.capitalize()

    return outstr


def suit_string(suit, short=False, capitalize=False):

    """Returns a string representing a specified suit,
    e.g. "clubs", "hearts", "diamonds".

    Arguments:
    suit -- an integer from 0 to nSuit-1, inclusive, representing the
    suit for which a string is to be returned. 0 is clubs, 1 is
    hearts, 2 is spades, and 3 is diamonds.
    short -- set to True to output short strings, i.e. "C"
    instead of "clubs", "S" instead of "spades"
    capitalize -- set to True to capitalize the first letter
    of the word (long strings only).

    """

    if suit not in range(0, PokerCardBase.nSuit):
        raise ValueError("Invalid suit value '{0}'".format(suit))

    if short:
        outstr = _SUIT_LONG_STRINGS[suit][0].upper()
    else:
        outstr = _SUIT_LONG_STRINGS[suit]

    if capitalize:
        outstr = outstr.capitalize()

    return outstr


# Non-public functions

def _get_index_integer(index):

    """Returns a valid index integer from an input of unspecified type."""

    if index in range(0, PokerCardBase.nCard):
        return index
    else:
        raise ValueError("Invalid index value '{}' of {}".format(index,
                                            PokerCardBase.nCard))


def _get_rank_and_suit_from_index(index):

    """Returns a two-element tuple containing a valid
    rank and suit integer from a provided valid index integer.

    """

    rank = index % PokerCardBase.nInSuit + 1
    if rank == 1:
        rank = PokerCardBase.nInSuit+1
    return (rank, index // PokerCardBase.nInSuit)


def _get_index_from_rank_and_suit(rank, suit):

    """Returns an integer representing a valid index
    from provided valid rank and suit integers.

    """

    return suit * PokerCardBase.nInSuit + ((rank - 1) if rank != PokerCardBase.nInSuit+1 else 0)


def _get_rank_and_suit_from_name(name):

    """Returns a two-element tuple representing a valid rank integer
    and a valid suit integer from a provided short name.

    """

    return (get_rank_integer(name[0:-1]), get_suit_integer(name[-1]))


def _get_index_from_name(name):

    """Returns an integer representing a valid index
    from a provided short name.

    """

    rank = get_rank_integer(name[0:-1])
    suit = get_suit_integer(name[-1])

    return _get_index_from_rank_and_suit(rank, suit)


# Exceptions

class CardArgumentError(Exception):

    """Exception raised when arguments to the Card class
    initializer are mismatched or missing.

    """

    pass


# Class

class PokerCardBase(object):

    """Playing card class.

    Public methods:
    __init__(rank, suit, index)
    copy()
    rank()
    suit()
    index()
    rank_string(short, capitalized)
    suit_string(short, capitalized)
    name_string(short, capitalized)

    Comparison operators:
    All are overloaded. Card instances are compared by rank only,
    i.e. suits are irrelevant. Aces are always treated as high by
    the comparison operators.

    Conversion operators:
    __str__ -- returns the result from name_string(capitalized=True)
    __int__ -- returns the card rank, with aces always one.

    """

    
    # Modified via class function setup()
    # No support for larger nSuit, nInSuit values
    nSuit = 4
    nInSuit = 13
    nCard = nSuit*nInSuit
    nCardInHand = 5
    nCardInStrait = nCardInHand
    nCardInFlush = nCardInHand
    
    
    @staticmethod
    def setPokerSettings(nsuit=None,
              ninsuit=None,
              ncard=None,
              nCardInHand=None,
              nCardInStrait=None,
              nCardInFlush=None):
        """
        Setup basic poker rules, especially if different
        than the traditional rules
        
        Set values that are present and leave the others unchanged
        If ncard is not specified
            then nCard = nSuit * nInSuit
        If nCardInHand is specified and nCardInStrait and nCardInFlush are not
            then nCardInStrait and nCardInFlush are set to nCardInHand
        """
        if nsuit is not None:
            PokerCardBase.nSuit = nsuit
        if ninsuit is not None:
            PokerCardBase.nInSuit = ninsuit
        if ncard is not None:
            PokerCardBase.nCard = ncard
        elif nsuit is not None or ninsuit is not None:
            PokerCardBase.nCard = PokerCardBase.nSuits() * PokerCardBase.cardsInSuit()
        if nCardInHand is not None:
            PokerCardBase.nCardInHand = nCardInHand
        if nCardInStrait is not None:
            PokerCardBase.nCardInStrait = nCardInStrait
        if nCardInFlush is not None:
            PokerCardBase.nCardInFlush = nCardInFlush
        if nCardInHand is not None and nCardInStrait is None and nCardInFlush is None:
            PokerCardBase.nCardInStrait = nCardInHand
            PokerCardBase.nCardInFlush = nCardInFlush
    
    
    @staticmethod
    def setupHand(
              nCardInHand=None,
              nCardInStrait=None,
              nCardInFlush=None):
        if nCardInHand is not None:
            PokerCardBase.nCardInHand = nCardInHand
            PokerCardBase.nCardInFlush = nCardInHand        # New default => all cards in hand
            PokerCardBase.nCardInStrait = nCardInHand

        # Over ride current or new defaults if present
        if nCardInStrait is not None:
            PokerCardBase.nCardInStrait = nCardInStrait
        if nCardInFlush is not None:
            PokerCardBase.nCardInFlush = nCardInFlush
            


    """ class functions """
    @staticmethod
    def cardsInHand():
        return PokerCardBase.nCardInHand

    @staticmethod
    def cardsInStrait():
        return PokerCardBase.nCardInStrait

    @staticmethod
    def nSuits():
        return PokerCardBase.nSuit

    @staticmethod
    def cardsInSuit():
        return PokerCardBase.nInSuit

    @staticmethod
    def cardsInFlush():
        return PokerCardBase.nCardInFlush


    @staticmethod
    def getNCard():
        """
        Get number of cards in deck
        """
        return PokerCardBase.nCard

        
    def __init__(self, rank=None, suit=None, index=None, name=None,
                 nSuit=None, nInSuit=None, nCard=None):

        """Instance initialization function.

        Arguments:
        rank -- rank of card, integer from 1 to 14 inclusive. Jack is 11,
        queen is 12, king is 13, and ace is 14. An ace can also
        be passed in with a value of 1. The names can also be
        passed in, e.g. "ace", "three", "king", or any shorter
        starting substring, e.g. "a", "e", "j", "k". The result is
        uncertain in the case of ambiguity, i.e. "t" may resolve to
        "two" or it may resolve to "ten", so use strings long enough
        to avoid ambiguity unless you want unpredictable results.
        suit -- suit of card, an integer from 0 to 3 inclusive representing
        clubs, hearts, spades or diamonds, in that order. The names
        can also be passed in, similar to the rank, e.g. "clubs",
        "sp", "hear", "d".
        index -- an integer from 0 to nCard inclusive, where 0 is the
        ace of clubs, 1 is the two of clubs, 2 is the three of clubs,
        and so on, progressing from ace to king through clubs, hearts,
        spades, and then diamonds, so that 51 is the king of diamonds.
        name -- a string of the form "AC" or "10D", corresponding to the
        type of string returned from name_string(short=True)
        direction -- evaluation direction HIGH, LOW, HIGH_LOW
        NOTE: internal values nInSuit, nSuit, nCards
        can be setup by class function setup
        Exceptions raised:
        CardArgumentError -- if all arguments are missing, or if an
        index is provided in addition to a rank and a suit, or if
        one but not both of a rank and a suit are provided.
        ValueError -- if any of the provided values are invalid.

        """
        if (suit is not None and rank is not None and
                 index is None and name is None):
            self._rank = get_rank_integer(rank)
            self._suit = get_suit_integer(suit)
            self._index = _get_index_from_rank_and_suit(self._rank, self._suit)
        elif (index is not None and rank is None and
                 suit is None and name is None):
            self._index = _get_index_integer(index)
            self._rank, self._suit = _get_rank_and_suit_from_index(index)
            ###print("index={}, rank = {}, suit = {}".format(index, self._rank, self._suit))
        elif (name is not None and rank is None and
                 suit is None and index is None):
            self._rank, self._suit = _get_rank_and_suit_from_name(name)
            self._index = _get_index_from_rank_and_suit(self._rank, self._suit)
        else:
            raise CardArgumentError("Missing or mismatched card arguments.")

    # Public methods

    def copy(self):

        """Returns a copy of the card."""

        return self.__class__(self, index=self.index())

    def rank(self):

        """Returns the integer rank of a card.
        ??? Do we need to adjust when playing LOW ???
        Aces are always returned as nInSuit+1, kings as 13,
        queens as 12, and jacks as 11.

        """

        return self._rank

    def suit(self):

        """Returns the integer suit of a card.

        0 represents clubs, 1 represents hearts, 2 represents
        spades, and 3 represents diamonds.

        """

        return self._suit

    def index(self):

        """Returns the integer index of a card.

        The index is an integer from 0 to nCard inclusive, where 0 is the
        ace of clubs, 1 is the two of clubs, 2 is the three of clubs,
        and so on, progressing from ace to king through clubs, hearts,
        spades, and then diamonds, so that 51 is the king of diamonds.
        The above is for regular decks.  When nSuit, nInSuit are changed
        the cards wrap ad nInSuit and clipped if index > nCard

        """

        return self._index

    def rank_string(self, short=False, capitalize=False):

        """Returns a string representing the rank of the card,
        e.g. "ace", "five", "jack".

        Arguments:
        short -- set to True to output short strings, i.e. "A"
        instead of "ace", "4" instead of "four", "J" instead
        of "jack".
        capitalize -- set to True to capitalize the first letter
        of the word (long strings only).

        """

        return rank_string(self._rank, short=short, capitalize=capitalize)

    def suit_string(self, short=False, capitalize=False):

        """Returns a string representing the suit of the card,
         e.g. "clubs", "hearts", "diamonds".

        Arguments:
        short -- set to True to output short strings, i.e. "C"
        instead of "clubs", "S" instead of "spades"
        capitalize -- set to True to capitalize the first letter
        of the word (long strings only).

        """

        return suit_string(self._suit, short=short, capitalize=capitalize)

    def name_string(self, short=False, capitalize=False):

        """Returns a string representing the name of the card,
         e.g. "ace of spades", "four of hearts", "ten of diamonds".

        Arguments:
        short -- set to True to output short strings, i.e. "AS"
        instead of "ace of spades", "4H" instead of "four of hearts"
        capitalize -- set to True to capitalize the first letter
        of the rank and the suit (long strings only).

        """

        if short:
            ofstr = ""
        else:
            ofstr = " of "

        return (self.rank_string(short=short, capitalize=capitalize) + ofstr +
                self.suit_string(short=short, capitalize=capitalize))

    # Non-public methods

    def _sort_index(self):

        """Returns an alternate index suitable for sorting, where cards
        are ordered first by rank, and then by suit order.

        """

        rank = 0 if self._rank == PokerCardBase.nInSuit-1 else self._rank - 1
        return self._suit + rank * PokerCardBase.nSuit

    # Conversion operators

    def __str__(self):

        """Override string conversion operator to return representation
        of card in long capitalize "Ace of Spades" format.

        """

        return self.name_string(capitalize=True)

    def __int__(self):

        """Override integer conversion operator to return card rank,
        with aces always returned as 1, kings as 13, queens as
        12, and jacks as 11.

        Note that this deliberately returns a different result from
        the rank() method, where aces are always returned as 14,
        not 1. The rank() method would normally be used in preference
        to converting to an integer when evaluating a hand, since
        in most cases the ace is treated as the highest card. For
        a plain integer representation, however, representing it
        as 1 is more natural than representing it as 14.

        """

        return self._rank if self._rank != PokerCardBase.nInSuit+1 else 1

    # Comparison operators

    # Disable pylint message for access to protected other._rank,
    # usage is safe when comparing two types of the same class
    # by an instance method.
    #
    # pylint: disable=W0212

    def __eq__(self, other):

        """Override == operator to compare based on card rank only."""

        return self._rank == other._rank

    def __ne__(self, other):

        """Override != operator to compare based on card rank only."""

        return self._rank != other._rank

    def __gt__(self, other):

        """Override > operator to compare based on card rank only.

        Aces are always treated as high.

        """

        return self._rank > other._rank

    def __lt__(self, other):

        """Override < operator to compare based on card rank only.

        Aces are always treated as high.

        """

        return self._rank < other._rank

    def __ge__(self, other):

        """Override >= operator to compare based on card rank only.

        Aces are always treated as high.

        """

        return self._rank >= other._rank

    def __le__(self, other):

        """Override <= operator to compare based on card rank only.

        Aces are always treated as high.

        """

        return self._rank <= other._rank

    # pylint: enable=W0212
