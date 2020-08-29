import numpy as np
from itertools import permutations as permut, combinations as comb

BS = ['BS'+str(i) for i in range(1, 14)]
BC = ['BC' + str(i) for i in range(1, 14)]
RD = ['RD' + str(i) for i in range(1, 14)]
RH = ['RH' + str(i) for i in range(1, 14)]

numb_seq = [{str(i+x) for x in range(3)} for i in range(1, 12)] + [{'1', '12', '13'}]


def suit_sep(player):
    '''Seperates the suit of player's cards
    And Prints the seperated suit cards'''
    for suit in [BS, BC, RD, RH]:
        cards = []
        for c in player.cards:
            if str(c) in suit:
                cards.append(c)
        for c in cards:
            print(c, end=' ')
        print()
        print('-'*60)


def is_seq(*cards):
    '''checks whether cards are in sequence or not.
       Returns True if  cards form a sequence. All cards must be different.'''
    tot_cards = len(cards)
    suits = set()
    for c in cards:
        suits.add(c.suit)
    if len(suits) != 1: return False
    if len(cards) == 2:
        if (cards[0]+1) == cards[1] or (cards[0]-1) == cards[1]: 
            return True
        return False
    tot = permut(cards, len(cards))
    for ss in tot:
        if is_seq(ss[0], ss[1]):
            if is_seq(*ss[1:]):
                return True
    return False


def is_trial(*cards):
    '''Returns True if  all cards have same number
    len(cards) must be > 1.
    '''
    numb = set() # Counts the number of occurences
    for c in cards:
        numb.add(c.number)
    if len(numb) == 1:
        return True
    return False



class Card():
    '''Makes the card'''
    def __init__(self, color, suit, number):
        '''color, suit, number must be string'''
        self.color = color
        self.suit = suit
        self.number = number
    
    def __str__(self):
        return self.color + self.suit + self.number

    def __add__(self, n=1):
        if self.number == '13':
            return Card(self.color, self.suit, '1')
        return Card(self.color, self.suit, str(int(self.number)+1))

    def __sub__(self, n=1):
        if self.number == '1':
            return Card(self.color, self.suit, '13')
        return Card(self.color, self.suit, str(int(self.number)-1))

    def alter(self):
        '''returns the alter card'''
        if self.suit == 'C':
            return Card('B', 'S', self.number)
        if self.suit == 'S':
            return Card('B', 'C', self.number)
        if self.suit == 'H':
            return Card('R', 'D', self.number)
        return Card('R', 'H', self.number)

    def __eq__(self, other):
        if str(self) == str(other):
            return True
        return False

    def maal_value(self, maal):
        '''returns the maal value of a card'''
        if self == maal:
            return 3
        if self == maal.alter():
            return 5
        if self == (maal -1) or self == (maal+1):
            return 2
        return 0

    def is_jocker(self, maal):
        if self.maal_value(maal) != 0 or self.number == maal.number:
            return True
        return False

    def is_faltu(self, player):
        if player.maal_watched:
            if self.is_jocker(player.Maal):
                return False
            cards = player.cards[:]
            cards.remove(self)
            for card in cards:
                if card.number == self.number:
                    return False
            if (self+1) in player.cards or (self-1) in player.cards:
                return False
            return True
        if (self+1) in player.cards or (self-1) in player.cards:
            return False
        return True




class MarriageBook():
    '''Creates a Book of Cards for Marriage game
       Total 52*3 Cards are created'''
    def __init__(self, lamphe=None):
        self.cards = []
        self.make()
        self.shuffle()

    def shuffle(self):
        np.random.shuffle(self.cards)

    def make(self):
        for _ in range(3):
            for card in BS:
                self.cards.append(Card(card[0], card[1], card[2:]))
            for card in BC:
                self.cards.append(Card(card[0], card[1], card[2:]))
            for card in RH:
                self.cards.append(Card(card[0], card[1], card[2:]))
            for card in RD:
                self.cards.append(Card(card[0], card[1], card[2:]))


class Player():
    '''Creates a Player for Marriage'''
    def __init__(self, name, money):
        self.name = name
        self.Maal = None
        self.money = money
        self.maal_watched = False
        self.cards = []
        self.jockers = []
        self.non_jockers = []
        self.seq_shown = False
        self.shown_sequences = []

    def pick_card(self, B):
        '''B is the Marriage Book of cards'''
        card = B.cards[0]
        self.cards.append(card)
        B.cards.pop(0)
        return card

    def check_seq(self):
        seq_count = 0
        for suit in [BS, BC, RD, RH]:
            if seq_count >= 3: 
                self.maal_watched = True
                return True
            cards = []
            for c in self.cards:
                if str(c) in suit:
                    cards.append(c)
            if len(cards) < 3: continue
            while True:
                tot_seq = comb(cards, 3)
                for card3 in tot_seq:
                    if {str(c)[2:] for c in card3} in numb_seq:
                        seq_count += 1
                        for c in card3:
                            cards.remove(c)
                        break
                else:
                    break
        if seq_count >= 3 :
            self.maal_watched = True
            return True
        return False

    def collect_seq(self):
        self.sequences = []
        for suit in [BS, BC, RD, RH]:
            cards = []
            for c in self.cards:
                if str(c) in suit:
                    cards.append(c)
            if len(cards) < 3:
                continue
            seq = []
            while True:
                tot = comb(cards, 3)  # All the combinations of cards of size 3
                for card3 in tot:
                    if {str(c)[2:] for c in card3} in numb_seq:
                        seq.append(card3)
                        for c in card3:
                            cards.remove(c)
                        break
                else:
                    break
            self.sequences.append(seq)
        return self.sequences

    def show_seq(self, maal_cut, B):
        collect = []
        self.hand_cards = []
        for seq in self.collect_seq():
            for card3 in seq:
                collect.append(card3)
        self.shown_sequences = collect[:3]
        self.seq_shown = True
        for c in self.cards:
            for card3 in self.shown_sequences:
                if c in card3:
                    break
            else:
                self.hand_cards.append(c)
        return collect[:3]

    def seperate_jocker(self):
        for c in self.hand_cards: # This Loop seperates jocker cards from Non-jockers
            if c.is_jocker(self.Maal):
                self.jockers.append(c)
            else:
                self.non_jockers.append(c)

    def check_baze(self):
        if self.maal_watched:
            self.seperate_jocker()
            match_3seq_cards = []
            cards = self.non_jockers[:] # Copying Non-jocker Cards
            while True:
                tot = comb(cards, 3)
                for card3 in tot:
                    if is_seq(*card3) or is_trial(*card3):
                        match_3seq_cards.append(card3)
                        for c in card3:
                            cards.remove(c)
                        break
                else:
                    break
            if len(cards) == 0:
                if len(match_3seq_cards) == len(self.jockers):
                    return True
            match_2seq_cards = []
            while True:
                tot = comb(cards, 2)
                for card2 in tot:
                    if is_seq(*card2) or is_trial(*card2):
                        match_2seq_cards.append(card2)
                        for c in card2:
                            cards.remove(c)
                        break
                else:
                    break
            if len(cards) == 0:
                l = len(self.jockers)
                if len(match_2seq_cards) in (l, l+1, l+2, l+3,  l*2, l*3, l*4) :
                    return True
        return False


    def throw(self):
        if self.maal_watched:
            for card in self.cards:
                if card.is_faltu(self):
                    return card
            non_jockers = []
            for card in self.cards:
                if not card.is_jocker(self.Maal):
                    return card
        for card in self.cards:
            if card.is_faltu(self):
                return card
        non_seq = []
        for card in self.cards:
            if (card+1) not in self.cards or (card-1) not in self.cards:
                return card
    def __str__(self):
        return 'Name = {}\nMoney = {}'.format(self.name, self.money)



            

            




