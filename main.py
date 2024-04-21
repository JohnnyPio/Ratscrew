import threading

import player
import game
import keyboard

import slap

players_hands = []
computer_player = player.Player("computer")
computer_player.set_computer_player()
players_hands.append(computer_player)
player_1 = player.Player("player1")
players_hands.append(player_1)

my_game = game.Game(players_hands)

def run_the_game():
    both_players_have_more_than_zero_cards = True
    while both_players_have_more_than_zero_cards:

        current_card = my_game.pile.cards[-1]
        my_game.get_next_player_from_current_player()

        if not game.card_is_royal(current_card):
            my_game.current_player.flip_single_card(my_game.pile)
        else:
            # Need a way for the time delay inside this loop and also the slap listener
            # TODO Slappable event not shown in royal sitch
            if not my_game.can_complete_flipping_for_royals():
                my_game.player_wins_the_pile()

        if not my_game.all_players_have_cards():
            both_players_have_more_than_zero_cards = False
            break


run_the_game()
