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

    def get_cards(self):
        return self.cards

    def empty(self):
        self.cards = []
        return self

    def add_card(self, card):
        self.cards.append(card)

    def matching_top_cards(self):
        if (self.number_of_cards_greater_than_or_equal_to(2)
                and self.get_card_value_from_index(-1) == self.get_card_value_from_index(-2)):
            return True

    def matching_sandwich_cards(self):
        if (self.number_of_cards_greater_than_or_equal_to(3)
                and self.get_card_value_from_index(-1) == self.get_card_value_from_index(-3)):
            return True

    def get_top_card(self):
        if len(self.cards) > 0:
            return self.cards[-1]

    def number_of_cards_greater_than_or_equal_to(self, number):
        if len(self.cards) >= number:
            return True

    def get_card_value_from_index(self, card_index):
        return self.cards[card_index][0]
