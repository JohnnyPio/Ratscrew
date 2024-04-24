import time
import slap
from deck import Deck


def max_cards_to_flip(last_card):
    if last_card[0] == "Ace":
        return 4
    elif last_card[0] == "King":
        return 3
    elif last_card[0] == "Queen":
        return 2
    elif last_card[0] == "Jack":
        return 1


def card_is_royal(card):
    top_card_rank = card[0]
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


# TODO The two below won't be static once the difficulty attribute is created
def delay_between_card_flips():
    # Should change based on easy,med,hard
    delay = 1  # x second delay
    time.sleep(delay)


def computer_slap_delay():
    # Should change based on easy,med,hard
    delay = 0.5  # x second delay
    # time.sleep(delay)
    return delay


class Game:
    def __init__(self, players):
        self.players = players
        self.pile = Deck()
        self.pile.shuffle()
        self.pile.initial_full_deck_deal_to_all_players(self.players)
        self.pile.empty()
        self.current_player = players[0]
        self.current_player.flip_single_card(self.pile)
        self.callbacks = []
        self.should_continue_dealing = True

    def get_index_from_player(self):
        return self.players.index(self.current_player)

    def get_next_player_from_current_player(self):
        self.current_player = self.players[(self.get_index_from_player() + 1) % len(self.players)]

    def get_player_before_current_player(self):
        return self.players[(self.get_index_from_player() - 1) % len(self.players)]

    # TODO Break this method up
    def player_wins_the_pile(self):
        self.pile.shuffle()
        player_before = self.get_player_before_current_player()
        print(f"{player_before.name} wins the pile")
        print(f"{self.players[0].name} has {self.players[0].get_number_of_cards()}")
        print(f"{self.players[1].name} has {self.players[1].get_number_of_cards()}")
        player_before.add_cards(list(self.pile.cards))
        self.pile.empty()
        player_before.flip_single_card(self.pile)
        self.get_next_player_from_current_player()

    def player_buries_their_card(self, player):
        top_player_card = player.cards[0]
        self.pile.cards.insert(0, top_player_card)
        player.remove_card(top_player_card)

    def all_players_have_cards(self):
        for player in self.players:
            if not player.cards:
                print(f"{player.name} loses")
                return False
        return True

    def is_slappable_event(self):
        if self.pile.matching_sandwich_cards() or self.pile.matching_top_cards():
            return True
        else:
            return False

    def can_complete_flipping_for_royals(self):
        last_card = self.pile.get_top_card()
        max_cards = max_cards_to_flip(last_card)
        flipped_cards = []
        for _ in range(max_cards):
            if not self.pile.cards:
                print("out of cards")
                return False

            self.current_player.flip_single_card(self.pile)
            self.notify_observers()
            flipped_cards.append(self.pile.get_top_card())

            if card_is_royal(self.pile.get_top_card()):
                return True

        if not any(card_is_royal(card) for card in self.pile.cards[-1 * len(flipped_cards)]):
            print("no royals here")
            return False

    def any_player_has_slapped(self):
        if any(player.set_as_slapped for player in self.players):
            return True
        else:
            return False

    def get_sole_bot_player(self):
        return next((x for x in self.players if x.is_player_a_bot), ValueError)

    # TODO This works well except in a royal situation. Need to have a way to pull royal sitch up
    def a_bot_player_slaps(self):
        this_slap = slap.Slap()
        this_slap.add_player_to_slap_pile(self.get_sole_bot_player(), computer_slap_delay())
        self.get_sole_bot_player().set_as_slapped()

    def add_observer(self, callback):
        self.callbacks.append(callback)

    def notify_observers(self):
        for callback in self.callbacks:
            callback(self.pile)  # Pass the current pile to the observer

    def stop_dealing(self):
        self.should_continue_dealing = False
