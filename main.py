import threading

import player
import game
from event import Event

players_hands = []
computer_player = player.Player("computer")
computer_player.set_computer_player()
players_hands.append(computer_player)
player_1 = player.Player("player1")
players_hands.append(player_1)

my_game = game.Game(players_hands)


# slap_listener_event = Event()


def run_the_game():
    both_players_have_more_than_zero_cards = True
    while both_players_have_more_than_zero_cards:
        my_game.get_next_player_from_current_player()

        if not game.card_is_royal(my_game.pile.get_top_card()):
            my_game.current_player.flip_single_card(my_game.pile)
        else:
            if not my_game.can_complete_flipping_for_royals():
                my_game.player_wins_the_pile()

        if not my_game.all_players_have_cards():
            break
        if my_game.is_slappable_event():
            my_game.a_bot_player_slaps()
            # print(f"computer has slapped is {computer_player.has_slapped}")
            # print(f"has anyone slapped: {my_game.any_player_has_slapped()}")


# run_the_game()
listen_thread = threading.Thread(target=my_game.monitor_deck)
listen_thread.start()

game_thread = threading.Thread(target=run_the_game)
game_thread.start()

listen_thread.join()
