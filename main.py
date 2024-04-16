import deck
import player
import game
import keyboard
import threading

my_deck = deck.Deck()
my_deck.shuffle()
pile = deck.Deck()
pile.empty()

players_hands = []
computer_player = player.Player("computer")
players_hands.append(computer_player)
player_1 = player.Player("player1")
players_hands.append(player_1)
my_deck.initial_full_deck_deal_to_all_players(players_hands)


def on_enter(event):
    global enter_pressed
    enter_pressed = True


def check_for_enter():
    global enter_pressed
    if enter_pressed:
        print("Enter key pressed")
        game.slap(pile, players_hands)
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
current_player.flip_single_card(pile)

both_players_have_more_than_zero_cards = True
while both_players_have_more_than_zero_cards:
    current_card = pile.cards[-1]
    current_player = game.get_next_player_from_current_player(current_player, players_hands)
    if check_for_enter():
        current_player = game.get_next_player_from_current_player(current_player, players_hands)

    if not game.card_is_royal(current_card):
        current_player.flip_single_card(pile)
    else:
        # Need a way for the time delay inside this loop and also the slap listener
        if not current_player.can_complete_flipping_for_royals(current_card, pile):
            pile.shuffle()
            player_before = game.get_player_before_current_player(current_player, players_hands)
            print(f"{player_before.name} wins the pile")
            player_before.add_cards(list(pile.cards))
            pile.empty()
            player_before.flip_single_card(pile)
            current_player = game.get_next_player_from_current_player(current_player, players_hands)

    if not game.all_players_have_cards(players_hands):
        both_players_have_more_than_zero_cards = False
        break

