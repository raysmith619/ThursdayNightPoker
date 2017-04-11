from __future__ import print_function
import sys
import re

from PyTrace import PyTrace
from PokerTable import PokerTable
from PokerComb import PokerComb


hand_file_name = "PokerComb_high_52_4_13.npy"
deck_comb = PokerComb()
if not deck_comb.fileExists(hand_file_name):
    print("File {} not found".format(hand_file_name))
    sys.exit()

print("Load info from file:{}".format(hand_file_name))
PokerComb.timenow("Start File loading")
deck_comb.loadComb(hand_file_name)
PokerComb.timenow("{} file load".format(hand_file_name))
hands = deck_comb.getDescs()

PokerComb.timenow("Before file save")
nhands = len(hands)
out_file = hand_file_name
out_file += ".hands"
outf = open(out_file, 'w')

for i in xrange(nhands):
    hand_desc = hands[i]
    hand_str = deck_comb.desc2handStr(hand_desc)
    hand_desc_nibs = deck_comb.nibs(hand_desc)
    print("{}  desc_nibs: {} desc_str: {} ".format(
        hand_str, hand_desc_nibs, hand_desc), file=outf)
PokerComb.timenow("After file save")
        

