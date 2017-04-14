'''
Poker Deal - current hand settings

@author: raysm
'''
from __future__ import print_function

from PyTrace import tR

from PokerCard import PokerCard
from PokerCardBase import PokerCardBase
from PokerComb import PokerComb
from PokerTable import PokerTable
from PokerGames import Games
from PokerBoard import PokerBoard
from PokerDeck import PokerDeck
from PokerHandDirection import PokerHandDirection


class PokerDeal(object):
    """ Direction """
    HIGH = PokerHandDirection.HIGH
    LOW = PokerHandDirection.LOW
    HIGH_LOW = PokerHandDirection.HIGH_LOW
    
    '''
    Poker deal - current hand
    '''
    def __init__(self,
                 table=None,         # Table
                 shuff=True,
                 deck = None,
                 gameName = None,
                 nplay = None,       # Default from game
                 minBet = None,
                 pot = None,
                direction=None,     # Direction: 1 - high, 2 - low, 3 - high-low
                lowFlushStrait=None):
        '''
        Constructor
        Deal
        '''
        """
        The game "rules the show" and can specify almost all the playing conditions
        """
        if gameName == None:
            gameName = table.game.name
        self.gameName = gameName
        game = self.game = Games[gameName]
        game.setPokerSettings()      # Setup basic settings

        """
        deal the deck
        """
        if deck == None:
            deck = PokerDeck()
        self.deck = deck

        if table is None:
            table = PokerTable(deck=deck)
        self.table = table
        
        if direction == None:
            direction = game.direction
        self.direction = direction
        
        if lowFlushStrait == None:
            lowFlushStrait = game.direction
        self.lowFlushStrait = lowFlushStrait
        
        if nplay == None:
            nplay = len(game.plays)
        self.nPlay = nplay
        self.playNum = 0
        if minBet == None:
            minBet = 1
        if pot == None:
            pot = 0
        self.pot = pot
        self.players = []       # Players participating
        
        
                        # Join each player to deal
        for player in table.players:
            self.joinDeal(player)
                        
        """
        place the board cards
        """
        self.board = PokerBoard(self, self.deck, gameName=self.gameName)
        """
        Deal out cards, one to player, until per-player number
        is reached
        """
        for i in range(self.game.nPlayerCards):
            pos = i + 1
            for player in table.players:
                cards = self.deck.draw(1)
                if len(cards) == 1:
                    card = cards[0]
                    if tR("deal"):
                        print("draw:{}".format(card))
                    if card is not None:
                        player.addCard(card)
                    else:
                        print("draw:{} None".format(card))
                        raise ValueError("drawing None is not expected")
                else:
                    print("draw:{} of {} cards".format(card,len(cards)))
                    raise ValueError("len(cards) is not 1:{}".format(len(cards)))




    def bet(self, player=None, doPrompt=False, amount=None,
            position=0):
        """
        Do bet or betting round.
        player - player's bet
                None - all players
        doPrompt - True - prompt for input
                    False - automatic bet
        amount - amount to bet
                None - best guess
        """
        if player == None:
            for player in self.table.players:
                self.bet(player=player, doPrompt=doPrompt, amount=amount)
            return
        
        if doPrompt:
            amount = player.bet(deal = self, doPrompt=doPrompt,
                                position=position, amount=amount)
        if amount == None:
            amount = player.minBet     
        if amount != None:
            amount = player.bet(amount=amount, position=position)
            if amount != None:
                self.pot += amount


    def deckSet(self):
        return self.deck.deckSet()
    
        
    def dealNext(self, toPlayer=None):
        if toPlayer == None:
            for player in self.table.players:
                self.dealNext(toPlayer=toPlayer)
            return
        
        card = self.deck
        toPlayer.addCard(card)

    
    def getBoard(self):
        return self.board

            
    def getHands(self, player=None,
                 direction=None):
        """
        Determine what hands are currently makeable given
        the player's cards and community cards
        Returns PokerComb object with hands info
        player - current player
        direction - High, Low, High_Low
        """
        if direction is None:
            direction = self.direction
            
        player_cards = player.getCards()
        board = self.getBoard()
        board_groups = board.getGroups()
        hand_comb = PokerComb(direction=direction,
                              lowFlushStrait=self.lowFlushStrait)
        for board_group in board_groups:
            hand_cards = player_cards[:]        # copy group
            board_group_list = list(board_group)
            hand_cards.extend(board_group_list)      # Possibly more than 5
            if len(hand_cards) >= self.handSize():
                hand_comb.addComb(hand_cards, self.handSize())
        return hand_comb


    def getPlayer(self, pos=1):
        """
        obtain player by position, starting at 1
        """
        return self.players[pos-1]
    
    def nPlayers(self):
        """
        Returns number of participating players
        """
        return len(self.players)
    
    

    def handSize(self):
        return PokerCardBase.cardsInHand()

    def hasMorePlays(self):
        if self.playNum < self.nPlay:
            return True
        return False


    def joinDeal(self, player):
        """
        Join player to deal,
        recording player having joined
        """
        self.players.append(player)
        player.joinDeal(self)
        
    
    def nextPlay(self):
        if self.hasMorePlays():
            self.playNum += 1
            return self.game.plays[self.playNum-1]
        return None
    
    
    def play(self):
        pl = self.thisPlay = self.nextPlay()
        if pl == None:
            return
        
        if pl.hasBoardShow():   
            self.showBoard()
        if pl.hasDeal():
            self.dealNext()
        if pl.hasBet:
            self.bet()
        self.displaySimple()
    
    
    def showBoard(self):
        nshow = self.thisPlay.nBoard
        for i in range(nshow):
            self.board.showCard()
        
        
            
    def displaySimple(self, showAll=False, showMe=True):
        self.board.displaySimple(showAll=showAll)
        for player in self.table.players:
            isMe = False
            if self.table.isMe(player):
                isMe = True

            player.displaySimple(showAll=showAll, showMe=showMe,
                                 isMe=isMe)
            
        print("Pot: {}".format(self.pot))    