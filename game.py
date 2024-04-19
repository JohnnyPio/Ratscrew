import time

from deck import Deck


# TODO add a listener for the user to flip when pressing spacebar

class Game:
    def __init__(self, players):
        self.players = players
        self.pile = Deck()
        self.pile.shuffle()
        self.pile.initial_full_deck_deal_to_all_players(self.players)
        self.pile.empty()
        self.current_player = players[0]
        self.current_player.flip_single_card(self.pile)

    def get_current_player_from_index(self):
        return self.players[self.current_player]

    def get_index_from_player(self):
        return self.players.index(self.current_player)

    def get_next_player_from_current_player(self):
        self.current_player = self.players[(self.get_index_from_player() + 1) % len(self.players)]

    def get_player_before_current_player(self):
        return self.players[(self.get_index_from_player() - 1) % len(self.players)]

    def player_wins_the_pile(self):
        self.pile.shuffle()
        player_before = self.get_player_before_current_player()
        print(f"{player_before.name} wins the pile")
        player_before.add_cards(list(self.pile.cards))
        self.pile.empty()
        player_before.flip_single_card(self.pile)
        self.get_next_player_from_current_player()

    # TODO Needs fixing but should be better, actually should be a method in deck() class
    def top_card_is_royal(self):
        top_card = self.pile.cards[0]
        top_card_rank = top_card[0]
        if top_card_rank == "Ace":
            return True
        elif top_card_rank == "King":
            return True
        elif top_card_rank == "Queen":
            return True
        elif top_card_rank == "Jack":
            return True
        else:
            return False


def all_players_have_cards(all_players):
    for player in all_players:
        if not player.cards:
            print(f"{player.name} loses")
            return False
    return True


def slap(pile, players):
    while True:
        if matching_top_cards(pile):
            print(f"Player {players[-1]} slapped the deck!")
        elif matching_sandwich_cards(pile):
            print(f"Player {players[-1]} slapped the deck!")
        else:
            print("No match! Keep playing...")


def delay_between_card_flips():
    # Should change based on easy,med,hard
    delay = 2  # x second delay
    time.sleep(delay)


def computer_slap_delay():
    # Should change based on easy,med,hard
    delay = 0.5  # x second delay
    time.sleep(delay)


def matching_top_cards(pile):
    if len(pile.cards) >= 2 and pile.cards[-1][0] == pile.cards[-2][0]:
        return True


def matching_sandwich_cards(pile):
    if len(pile.cards) >= 3 and pile.cards[-1][0] == pile.cards[-3][0]:
        return True


def is_slappable_event(pile):
    if matching_sandwich_cards(pile) or matching_top_cards(pile):
        return True


def players_in_slap_event(players):
    all_players_to_slap = [players]
    names = [player.name for player in all_players_to_slap]
    print(f"here's who slapped {names}")
    return all_players_to_slap
