import random

from game import Game


class Deck(Game):
    def __init__(self):
        super().__init__()
        self.cards = []
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        for suit in suits:
            for value in values:
                self.cards.append((value, suit))

    def shuffle(self):
        random.shuffle(self.cards)

    def __iter__(self):
        return iter(self.cards)

    def __str__(self):
        deck_str = ""
        for card in self.cards:
            deck_str += card[0] + " of " + card[1] + "\n"
        return deck_str

    def initial_full_deck_deal_to_all_players(self, all_players):
        num_players = len(all_players)
        player_index = 0
        player_hands = {a_player.name: [] for a_player in all_players}

        for card in self:
            a_player = all_players[player_index]
            player_hands[a_player.name].append(card)
            player_index = (player_index + 1) % num_players

        for a_player in all_players:
            a_player.cards = player_hands[a_player.name]

    def empty(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)
