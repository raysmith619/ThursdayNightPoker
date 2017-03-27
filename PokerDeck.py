"""Card deck module.

Library Release 1.1

Copyright 2017 Ray Smith
Adapted from Paul Griffiths deck.py
Email: raysmith@alum.mit.edu

Distributed under the terms of the GNU General Public License.
http://www.gnu.org/licenses/

"""


import random
from collections import Counter

from PyTrace import tR
from PokerCard import PokerCard


class EmptyDeckError(Exception):

    """Exception class for trying to draw a card from an empty deck.

    """

    pass


class PokerDeck(object):

    """Implements a deck of cards, using Card instances.

    Public methods:
    __init__(packs)
    discard()
    discard_size()
    draw()
    get_card_list()
    get_discard_list()
    replace_discards()
    shuffle()

    """
    
    def __init__(self, packs=1, nsuit=4, ninsuit=13,
                 ncard=None):

        """Initializes a Deck instance.

        Creates a deck of cards, and an empty discard pile.

        Arguments:
        packs -- the number of packs to put into the deck, set to
        something greater than 1 to create a deck consisting of
        multiple packs.
        nsuit - number of suits: default=4
        ninsuit = number in each suit
        ncards - 1-52 how many cards in deck
            Mostly for debugging / experimentation, to 
            reduce the combinatorial math
        """

        if (nsuit is not None or
            ninsuit is not None or
            ncard is not None):
            PokerCard.setup(nsuit=nsuit, ninsuit=ninsuit,
                             ncard=ncard)
        if not isinstance(packs, int) or not packs > 0:
            raise ValueError("Argument 'packs' must be a positive integer.")
        
        nCard = PokerCard.getNCard()
        self._cards = [PokerCard(index=idx) for pack in range(packs)
                                       for idx in range(nCard-1, -1, -1)]
        self._discards = []

        ###new_deck = PokerDeck()
        ###new_deck_cards = new_deck.get_card_list()
        self._deckSet = set(list(self._cards))
        deck_hash = Counter();
        for card in self._cards:
            deck_hash[card.index()] = card
        self._deckHash = deck_hash
        
    # Public methods

    def deckSet(self):
        """ Returns set of cards in desk """
        return self._deckSet
    
    
    def discard(self, cards):

        """Adds a list of cards to the discard pile.

        Arguments:
        card -- the Card instance list to be added. Under normal
        circumstances, this list will have originally been taken
        from the same deck using the draw() method, but this is
        not necessarily so.

        """

        self._discards.extend(cards)

    def discard_size(self):

        """Returns the number of cards in the discard pile."""

        return len(self._discards)

    def draw(self, number=1):

        """Draws one or more cards from the top of the deck and returns
        it or them in a list.

        Arguments:
        number -- the number of cards to draw.

        """
        if tR('deck'):
            print("drawing {} card".format(number))
        if number > len(self._cards):
            raise EmptyDeckError("Ran out of cards - Too many players?")
        else:
            drawn_cards = self._cards[-number:]

            # Call reverse() to simulate cards being popped
            # off the top of the deck in order

            drawn_cards.reverse()
            self._cards = self._cards[0:-number]
        if tR('deck'):
            list_string = ""
            for dcard in drawn_cards:
                if list_string != "":
                    list_string += " "
                list_string += dcard.name_string()
            print("drawn cards: {}".format(list_string))
            
        return drawn_cards

    def get_card_list(self):

        """Returns a copy of the card list."""

        return self._cards[:]

    def get_discard_list(self):

        """Returns a copy of the discard list."""

        return self._discards[:]

    def replace_discards(self):

        """Replaces the discard pile at the bottom of the deck."""

        self._discards.extend(self._cards)
        self._cards = self._discards
        self._discards = []

    def shuffle(self, return_discards=True):

        """Shuffles the deck.

        Arguments:
        return_discards -- If set to 'True', the discard pile is added
        back to the deck before shuffling, otherwise the discard pile
        remains intact and only the remaining cards in the deck
        are shuffled.

        """

        if return_discards and self._discards:
            self.replace_discards()

        random.shuffle(self._cards)

    # Indexing and iteration methods

    def __len__(self):

        """Returns the number of cards remaining in the deck.

        Excludes the cards in the discard pile.

        """

        return len(self._cards)

    def __getitem__(self, key):

        """Returns the card at the specified index."""

        return self._cards[key]

    def __setitem__(self, key, value):

        """Sets the card at the specified index."""

        if not isinstance(value, PokerCard):
            raise TypeError("Only Card instances can be assigned.")
        else:
            self._cards[key] = value

    def __delitem__(self, key):

        """Deletes the card at the specified index."""

        return self._cards.pop(key)

    def __iter__(self):

        """Returns an iterator object of the cards list."""

        return iter(self._cards)

    def __contains__(self, item):

        """Returns true if item is in the cards list."""

        if not isinstance(item, PokerCard):
            return False
        else:
            for card in self._cards:
                if card.index() == item.index():
                    return True
            else:
                return False
