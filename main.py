import player
import game
import keyboard

import slap

players_hands = []
computer_player = player.Player("computer")
players_hands.append(computer_player)
player_1 = player.Player("player1")
players_hands.append(player_1)

my_game = game.Game(players_hands)


# def on_enter(event):
#     global enter_pressed
#     enter_pressed = True
#
#
# def check_for_enter():
#     global enter_pressed
#     if enter_pressed:
#         print("Enter key pressed")
#         my_game.slap()
#         enter_pressed = False

    # if check_for_enter():
    #     current_player = game.get_next_player_from_current_player(current_player, players_hands)


# enter_pressed = False
# keyboard.on_press_key("enter", on_enter)

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

    # TODO This works well except in a royal situation. Need to have a way to pull royal sitch up
    if my_game.is_slappable_event():
        this_slap = slap.Slap()
        this_slap.add_player_to_slap_pile(computer_player, game.computer_slap_delay())

    if not my_game.all_players_have_cards():
        both_players_have_more_than_zero_cards = False
        break
