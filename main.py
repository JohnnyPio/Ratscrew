import player
import game

players_hands = []
computer_player = player.Player("computer")
computer_player.set_computer_player()
players_hands.append(computer_player)
player_1 = player.Player("player1")
players_hands.append(player_1)


def run_the_game():
    both_players_have_more_than_zero_cards = True
    while both_players_have_more_than_zero_cards and my_game.should_continue_dealing:
        my_game.get_next_player_from_current_player()
        top_card = my_game.pile.get_top_card_of_deck()

        if not game.card_is_royal(top_card):
            my_game.flip_add_to_pile_then_remove_and_delay()

        else:
            if not my_game.can_complete_flipping_for_royals():
                my_game.player_wins_the_pile(my_game.get_previous_player_before_current_player())

        if not my_game.all_players_have_cards():
            break


my_game = game.Game(players_hands)
my_game.initial_shuffle_deck_deal_then_empty_pile()
my_game.add_observer(my_game.monitor_for_slaps)
run_the_game()
