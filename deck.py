import random


class Deck:
    def __init__(self):
        self.cards = []
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        for suit in suits:
            for value in values:
                self.cards.append((value, suit))

    def __iter__(self):
        return iter(self.cards)

    def __str__(self):
        deck_str = ""
        for card in self.cards:
            deck_str += card[0] + " of " + card[1] + "\n"
        return deck_str

    def shuffle(self):
        random.shuffle(self.cards)

    def empty(self):
        self.cards = []
        return self

    def add_card(self, card):
        self.cards.append(card)

    def matching_top_cards(self):
        if len(self.cards) >= 2 and self.cards[-1][0] == self.cards[-2][0]:
            return True

    def matching_sandwich_cards(self):
        if len(self.cards) >= 3 and self.cards[-1][0] == self.cards[-3][0]:
            return True

    def get_top_card_of_deck(self):
        if len(self.cards) > 0:
            return self.cards[-1]
