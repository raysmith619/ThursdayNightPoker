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

Games["44"] = PokerGame("44", nPlayerCards=4, nUp=0,
                nBoard=8, nBoardUp=0,
                direction=PokerHandDirection.HIGH_LOW,
                plays=pls)

Games["Adjacent"] = PokerGame("Adjacent", nPlayerCards=4,
                               nUp=0, nBoard=8, nBoardUp=0,
                               direction=PokerHandDirection.HIGH_LOW,
                        plays=pls)
        