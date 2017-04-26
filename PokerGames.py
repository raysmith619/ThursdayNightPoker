'''
Poker rules for one game

@author: raysm
'''
from PokerGame import PokerGame
from PokerPlay import PokerPlay
from PokerHandDirection import PokerHandDirection

Games = {}
nbd=2;hsb=True
pl = PokerPlay(nBoard=2, hasBet=True)
pls =[pl, pl, pl, pl]
"""
Notation:
[n] - hidden card at position n
 n  - exposed card at position n
"""

Games["toy"] = PokerGame("toy",
                nCardInHand = 2,   # Hand size (number of cards making a hand)
                nsuit=3,
                ninsuit=3,
                nCardInStrait=2,    # No one card straits/flushes
                nCardInFlush=2,
                nPlayerCards=1, # Number of cards to each player
                nBoard=1, nBoardUp=0,
                boardSelections = [(1,)],  # Board selections
                direction=PokerHandDirection.HIGH_LOW,
                plays=[pl, pl])

Games["toy2"] = PokerGame("toy2",
                nCardInHand = 3,   # Hand size (number of cards making a hand)
                nsuit=4,
                ninsuit=8,
                
                nPlayerCards=3, # Number of cards to each player
                nBoard=2, nBoardUp=0,
                boardSelections = [(1, 2)],  # Board selections
                direction=PokerHandDirection.HIGH_LOW,
                plays=[pl, pl])

"""
44:
    board arranged:
        [1] [2] [3] [4]
        [5] [6] [7] [8]
    Players receive 4 car
    
    
    
    
    
    
    
    
    ds down each.
    Hands are made using 1-4 of the cards in either of the board
    rows.
    Game proceeds with a bet at the beginning of each round.
    After each bet is a card from each row is exposed.
"""

Games["44"] = PokerGame("44", nPlayerCards=4, nUp=0,
                nBoard=8, nBoardUp=0,
                boardSelections = [[1,2,3,4],
                                   [5,6,7,8]],
                direction=PokerHandDirection.HIGH_LOW,
                plays=pls)


"""
Pick-2:
Each player, being dealt 5 down cards, uses exactly 2 of their hand cards combined
with 3 from the board cards.
"""


"""
Fifty-five:
"""

"""
Red-Black:
Each player is dealt 5 down cards.
The board is created with two columns, Red and Black respectively, of 3 down cards.
Board arangement:
     1  2
     3  4
     5  6
"""


Games["Adjacent"] = PokerGame("Adjacent", nPlayerCards=4,
                        nUp=0, nBoard=8, nBoardUp=0,
                        direction=PokerHandDirection.HIGH_LOW,
                        plays=pls)
        