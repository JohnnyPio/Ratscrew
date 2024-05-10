import time

from player import Player
import slap
from deck import Deck
from observer import Observer


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


class Game:
    def __init__(self, players, difficulty):
        self.players = players
        self.pile = Deck()
        self.observe_for_slap_opportunity = Observer()
        self.observe_for_human_slap = Observer()
        self.should_continue_dealing = True
        self.current_player = None
        self.difficulty = difficulty

    def monitor_for_slap_opportunity(self):
        if self.is_slappable_event():
            print("Slap time")
            print("computer Slaps")
            self.observe_for_slap_opportunity.remove_observers()
            self.observe_for_slap_opportunity.add_observer(self.monitor_for_slap_opportunity)
            self.observe_for_slap_opportunity.add_observer(self.all_players_have_cards)
            # TODO Not sure why this is showing a warning now?? Check git
            self.player_wins_the_pile(self.get_sole_bot_player())
            self.run_the_game()

    def is_slappable_event(self):
        if self.pile.matching_sandwich_cards() or self.pile.matching_top_cards():
            return True
        else:
            return False

    def all_players_have_cards(self):
        for player in self.players:
            if not player.cards:
                print(f"{player.name} loses, game over")
                self.stop_dealing()
                exit()

    def stop_dealing(self):
        self.should_continue_dealing = False

    def get_sole_bot_player(self):
        return next((x for x in self.players if x.is_player_a_bot))

    def player_wins_the_pile(self, the_player: Player):
        self.pile.shuffle()
        self.set_current_player(the_player)
        print(f"{self.current_player.get_name()} wins the pile")
        self.current_player.add_cards(list(self.pile.get_cards()))
        self.print_player_and_number_of_cards(0)
        self.print_player_and_number_of_cards(1)
        self.pile.empty()
        self.flip_add_to_pile_then_remove_and_delay()

    def set_current_player(self, the_player: Player):
        self.current_player = the_player

    # TODO Maybe just make this static and print both players
    def print_player_and_number_of_cards(self, index):
        print(f"{self.players[index].name} has {self.players[index].get_number_of_cards()}")

    def flip_add_to_pile_then_remove_and_delay(self):
        first_card = self.current_player.flip_single_card()
        self.observe_for_slap_opportunity.notify_observers()
        self.add_card_to_pile(first_card)
        self.current_player.remove_top_card_from_hand()
        self.delay_between_card_flips()

    def add_card_to_pile(self, flipped_card):
        self.pile.add_card(flipped_card)

    def initialize_game(self):
        self.pile.shuffle()
        self.initial_full_deck_deal_to_all_players()
        self.pile.empty()
        self.set_current_player(self.get_sole_bot_player())
        self.flip_add_to_pile_then_remove_and_delay()

    def initial_full_deck_deal_to_all_players(self):
        num_players = len(self.players)
        player_index = 0
        player_hands = {a_player.name: [] for a_player in self.players}

        for card in self.pile:
            a_player = self.players[player_index]
            player_hands[a_player.name].append(card)
            player_index = (player_index + 1) % num_players

        for a_player in self.players:
            a_player.cards = player_hands[a_player.name]

    def run_the_game(self):
        while self.should_continue_dealing:
            self.set_next_player_from_current_player()

            if not card_is_royal(self.pile.get_top_card()):
                self.flip_add_to_pile_then_remove_and_delay()
            else:
                if not self.can_complete_flipping_for_royals():
                    self.player_wins_the_pile(self.get_previous_player_before_current_player())

    def set_next_player_from_current_player(self):
        next_player_index = (self.get_index_from_player() + 1) % len(self.players)
        self.set_current_player(self.players[next_player_index])

    def get_index_from_player(self):
        return self.players.index(self.current_player)

    # TODO Break this up
    def can_complete_flipping_for_royals(self):
        last_card = self.pile.get_top_card()
        max_cards = max_cards_to_flip(last_card)
        flipped_cards = []
        for _ in range(max_cards):
            if not self.pile.cards:
                print("out of cards")
                return False

            self.flip_add_to_pile_then_remove_and_delay()
            flipped_cards.append(self.pile.get_top_card())

            if card_is_royal(self.pile.get_top_card()):
                return True

        self.any_royal_card_in_list(flipped_cards)

    def any_royal_card_in_list(self, card_list):
        previous_cards_in_pile = self.get_previous_pile_card(card_list)
        if not any(card_is_royal(card) for card in previous_cards_in_pile):
            print("no royals here")
            return False
        else:
            return True

    # TODO Odd behavior for this one
    def get_previous_pile_card(self, card_list):
        return self.pile.cards[-len(card_list):]

    def get_previous_player_before_current_player(self):
        previous_player_index = (self.get_index_from_player() - 1) % len(self.players)
        return self.players[previous_player_index]

    # Delay stuff
    def is_difficulty_easy(self):
        return self.difficulty == "1"

    def is_difficulty_medium(self):
        return self.difficulty == "2"

    def is_difficulty_hard(self):
        return self.difficulty == "3"

    def delay_between_card_flips(self):
        delay = 0
        if self.is_difficulty_easy:
            delay = 1
        elif self.is_difficulty_medium:
            delay = .85
        elif self.is_difficulty_hard:
            delay = .7
        else:
            ValueError()
        time.sleep(delay)

    def computer_slap_delay(self):
        delay = 0
        if self.is_difficulty_easy:
            delay = 1
        elif self.is_difficulty_medium:
            delay = .75
        elif self.is_difficulty_hard:
            delay = .5
        else:
            ValueError()
        return delay

    # These aren't used yet

    def player_buries_their_card(self, player):
        top_player_card = player.cards[0]
        self.pile.cards.insert(0, top_player_card)
        player.remove_card(top_player_card)

    def any_player_has_slapped(self):
        if any(player.set_as_slapped for player in self.players):
            return True
        else:
            return False

    # TODO Move this to Slap
    def a_bot_player_slaps(self):
        this_slap = slap.Slap()
        this_slap.add_player_to_slap_pile(self.get_sole_bot_player(), self.computer_slap_delay())
        self.get_sole_bot_player().set_as_slapped()
