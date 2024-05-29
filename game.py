import time
from pynput import keyboard
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
        self.observe_for_end_game = Observer()
        self.observe_for_slap_opportunity = Observer()
        self.should_continue_dealing = True
        self.current_player = None
        self.difficulty = difficulty
        self.current_slap = None
        self.last_card_flip_time = None

    # TODO maybe a better way to move the exit code up a level?
    def monitor_for_end_game(self):
        self.a_player_is_out_of_cards()

    def monitor_for_slap_opportunity(self):
        with keyboard.Events() as events:
            # TODO the below timeout should match the slap delay
            event = events.get(1.0)
            human = self.get_sole_human_player()

            # TODO try "if event is not None"

            if event is None and not self.is_slappable_event():
                return

            # # TODO Remove below eventually, causes a bug when no event
            # if event.key == keyboard.Key.enter:
            #     return

            if not self.is_current_slap_event():
                self.create_slap_event()

            if event is None and self.is_slappable_event():
                print("computer Slaps alone")
                # TODO Fix bug where royal pile has slappable event and clobbers slap opp
                self.bot_player_slaps()
                winner_of_slap = self.current_slap.get_name_of_slap_winner()
                self.player_wins_the_pile(winner_of_slap)
                self.run_the_game()

            if event.key == keyboard.Key.space and not self.is_slappable_event():
                self.player_buries_their_card(human)
                print("bury a card")
                self.print_players_and_number_of_cards()

            if event.key == keyboard.Key.space and self.is_slappable_event():
                key_press_time = time.time()
                duration = key_press_time - self.last_card_flip_time
                print(f"hooray a human slap in {duration}!")
                self.current_slap.add_player_and_slaptime_to_slap(human, duration)
                self.bot_player_slaps()
                winner_of_slap = self.current_slap.get_name_of_slap_winner()
                self.player_wins_the_pile(winner_of_slap)

            self.remove_slap_event()

    def is_slappable_event(self):
        if self.pile.matching_sandwich_cards() or self.pile.matching_top_cards():
            return True
        else:
            return False

    def bot_player_slaps(self):
        bot_player = self.get_sole_bot_player()
        # TODO the second arg below should reflect the game difficulty
        self.current_slap.add_player_and_slaptime_to_slap(bot_player, 0.9)

    # TODO This should probably return a Boolean and move the logic up
    def a_player_is_out_of_cards(self):
        for player in self.players:
            if player.get_number_of_cards() == 0:
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
        self.print_players_and_number_of_cards()
        self.pile.empty()
        self.flip_add_to_pile_then_remove_and_delay()

    def set_current_player(self, the_player: Player):
        self.current_player = the_player

    def print_players_and_number_of_cards(self):
        self.print_player_and_number_of_cards(0)
        self.print_player_and_number_of_cards(1)

    # TODO Maybe just make this static and print both players
    def print_player_and_number_of_cards(self, index):
        print(f"{self.players[index].name} has {self.players[index].get_number_of_cards()}")

    def flip_add_to_pile_then_remove_and_delay(self):
        self.notify_all_observers()
        first_card = self.current_player.flip_single_card()
        self.add_card_to_pile(first_card)
        self.last_card_flip_time = time.time()
        self.current_player.remove_top_card_from_hand()
        self.delay_between_card_flips()

    def notify_all_observers(self):
        self.observe_for_slap_opportunity.notify_observers()
        self.observe_for_end_game.notify_observers()

    def add_card_to_pile(self, flipped_card):
        self.pile.add_card(flipped_card)

    def initialize_observers(self):
        self.observe_for_slap_opportunity.add_observer(self.monitor_for_slap_opportunity)
        self.observe_for_end_game.add_observer(self.a_player_is_out_of_cards)

    def initialize_game(self):
        self.initialize_observers()
        self.pile.shuffle()
        self.full_deck_deal_to_all_players()
        self.pile.empty()
        self.set_current_player(self.get_sole_bot_player())
        self.flip_add_to_pile_then_remove_and_delay()

    def full_deck_deal_to_all_players(self):
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

        if not self.is_slappable_event():
            self.any_royal_card_in_list(flipped_cards)

    def any_royal_card_in_list(self, card_list):
        previous_cards_in_pile = self.get_previous_pile_card(card_list)
        if not any(card_is_royal(card) for card in previous_cards_in_pile):
            self.delay_between_card_flips()
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
    # TODO Turn these into Enums instead of numbers
    def is_difficulty_easy(self):
        return self.difficulty == "1"

    def is_difficulty_medium(self):
        return self.difficulty == "2"

    def is_difficulty_hard(self):
        return self.difficulty == "3"

    def is_difficulty_godlike(self):
        return self.difficulty == "5"

    def delay_between_card_flips(self):
        delay = int
        if self.is_difficulty_easy():
            delay = 1
        elif self.is_difficulty_medium():
            delay = .85
        elif self.is_difficulty_hard():
            delay = .7
        elif self.is_difficulty_godlike():
            delay = .1
        else:
            ValueError()
        time.sleep(delay)

    def computer_slap_delay(self):
        delay = int
        if self.is_difficulty_easy():
            delay = 1
        elif self.is_difficulty_medium():
            delay = .85
        elif self.is_difficulty_hard():
            delay = .70
        elif self.is_difficulty_godlike():
            delay = .50
        else:
            ValueError()
        return delay

    # These aren't used yet

    def player_buries_their_card(self, player):
        top_player_card = player.cards[0]
        self.pile.cards.insert(0, top_player_card)
        player.remove_top_card_from_hand()

    def any_player_has_slapped(self):
        if any(player.set_as_slapped for player in self.players):
            return True
        else:
            return False

    # TODO Fix this to be not hacky, similar to bot method
    def get_sole_human_player(self):
        return self.players[1]

    # TODO Move this to Slap
    def a_bot_player_slaps(self):
        this_slap = slap.Slap()
        this_slap.add_player_and_slaptime_to_slap(self.get_sole_bot_player(), self.computer_slap_delay())
        self.get_sole_bot_player().set_as_slapped()

    def create_slap_event(self):
        self.current_slap = slap.Slap()

    def is_current_slap_event(self):
        if self.current_slap:
            return True
        else:
            return False

    def remove_slap_event(self):
        self.current_slap = None
