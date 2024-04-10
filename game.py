# TODO add a listener for the user to flip when pressing spacebar
import deck


def card_is_royal(card):
    if card[0] == "Ace":
        return True
    elif card[0] == "King":
        return True
    elif card[0] == "Queen":
        return True
    elif card[0] == "Jack":
        return True
    else:
        return False


class Game:
    def __init__(self):
        self.players = []
        self.dealing_deck = deck.Deck
        self.pile = []

    def add_player(self, player):
        self.players.append(player)

