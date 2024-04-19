import deck
import player
import game
import keyboard
import threading

players_hands = []
computer_player = player.Player("computer")
players_hands.append(computer_player)
player_1 = player.Player("player1")
players_hands.append(player_1)

my_game = game.Game(players_hands)


def on_enter(event):
    global enter_pressed
    enter_pressed = True


def check_for_enter():
    global enter_pressed
    if enter_pressed:
        print("Enter key pressed")
        game.slap(my_game.pile, players_hands)
        enter_pressed = False


enter_pressed = False
keyboard.on_press_key("enter", on_enter)

both_players_have_more_than_zero_cards = True
while both_players_have_more_than_zero_cards:
    current_card = my_game.pile.cards[-1]
    my_game.get_next_player_from_current_player()
    # if check_for_enter():
    #     current_player = game.get_next_player_from_current_player(current_player, players_hands)

    if not my_game.top_card_is_royal():
        my_game.current_player.flip_single_card(my_game.pile)
    else:
        # Need a way for the time delay inside this loop and also the slap listener
        if not my_game.current_player.can_complete_flipping_for_royals(current_card, my_game.pile):
            my_game.player_wins_the_pile()

    # TODO This works well except in a royal situation. Need to have a way to pull royal sitch up
    if game.is_slappable_event(my_game.pile):
        game.computer_slap_delay()
        game.players_in_slap_event(computer_player)

    if not game.all_players_have_cards(players_hands):
        both_players_have_more_than_zero_cards = False
        break
