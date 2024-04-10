import deck
import player
import game
from player import Player


my_deck = deck.Deck()
my_deck.shuffle()
pile = deck.Deck()
pile.empty()

computer_player = player.Player("computer")
player_1 = player.Player("player1")
# TODO fix this for more than 2 players
players_hands: list[Player] = [computer_player, player_1]
my_deck.initial_full_deck_deal_to_all_players(players_hands)

player_index = 0
current_player = players_hands[player_index]
current_player.flip_single_card(pile)

both_players_have_more_than_zero_cards = True
while both_players_have_more_than_zero_cards:
    current_card = pile.cards[-1]
    player_index = (player_index + 1) % len(players_hands)
    current_player = players_hands[player_index]

    if game.card_is_royal(current_card):
        print(f"the current player is {current_player.name}")
        if not current_player.flip_for_royal(current_card, pile):
            player_before = players_hands[
                (player_index - 1) % len(players_hands)]  # TODO Write method for getting the player before
            pile.shuffle()
            player_before.add_cards(list(pile.cards))
            pile.cards = []  # TODO why doesn't pile.empty() work here?
            player_before.flip_single_card(pile)
    else:
        current_player.flip_single_card(pile)

    if len(computer_player.cards) == 0:
        both_players_have_more_than_zero_cards = False
        print(f"computer_player loses")
        break
    if len(player_1.cards) == 0:
        both_players_have_more_than_zero_cards = False
        print(f"player_1 wins")
        break
