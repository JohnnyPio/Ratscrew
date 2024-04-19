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

# Start separate thread to check for Enter key press

enter_thread = threading.Thread(target=check_for_enter)
enter_thread.daemon = True
enter_thread.start()


# Initialize the flipping
player_index = 0
current_player = game.get_current_player_from_index(player_index, players_hands)
current_player.flip_single_card(my_game.pile)

both_players_have_more_than_zero_cards = True
while both_players_have_more_than_zero_cards:
    current_card = my_game.pile.cards[-1]
    current_player = game.get_next_player_from_current_player(current_player, players_hands)
    if check_for_enter():
        current_player = game.get_next_player_from_current_player(current_player, players_hands)

    if not game.card_is_royal(current_card):
        current_player.flip_single_card(my_game.pile)
    else:
        # Need a way for the time delay inside this loop and also the slap listener
        if not current_player.can_complete_flipping_for_royals(current_card, my_game.pile):
            my_game.pile.shuffle()
            player_before = game.get_player_before_current_player(current_player, players_hands)
            print(f"{player_before.name} wins the pile")
            player_before.add_cards(list(my_game.pile.cards))
            my_game.pile.empty()
            player_before.flip_single_card(my_game.pile)
            current_player = game.get_next_player_from_current_player(current_player, players_hands)

    # TODO This works well except in a royal situation. Need to have a way to pull royal sitch up
    if game.is_slappable_event(my_game.pile):
        game.computer_slap_delay()
        game.players_in_slap_event(computer_player)

    if not game.all_players_have_cards(players_hands):
        both_players_have_more_than_zero_cards = False
        break

