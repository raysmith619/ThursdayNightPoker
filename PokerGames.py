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
Games["toy"] = PokerGame("toy",
                handSize = 4,   # Hand size (number of cards making a hand)
                nStraitCards=None, # Length of strait, default: handSize
                nFlushCards=None,  # Length of flush, default: handSize
                nPlayerCards=3, # Number of cards to each player
                nBoard=4, nBoardUp=0,
                direction=PokerHandDirection.HIGH_LOW,
                plays=[pl, pl])

Games["44"] = PokerGame("44", nPlayerCards=4, nUp=0,
                nBoard=8, nBoardUp=0,
                direction=PokerHandDirection.HIGH_LOW,
                plays=pls)

Games["Adjacent"] = PokerGame("Adjacent", nPlayerCards=4,
                               nUp=0, nBoard=8, nBoardUp=0,
                               direction=PokerHandDirection.HIGH_LOW,
                        plays=pls)
        