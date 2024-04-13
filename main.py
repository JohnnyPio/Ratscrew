import deck
import player
import game
from player import Player

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

# Initialize the flipping
player_index = 0
current_player = game.get_current_player_from_index(player_index, players_hands)
current_player.flip_single_card(pile)

both_players_have_more_than_zero_cards = True
while both_players_have_more_than_zero_cards:
    current_card = pile.cards[-1]
    current_player = game.get_next_player_from_current_player(current_player, players_hands)

    if not game.card_is_royal(current_card):
        current_player.flip_single_card(pile)
    else:
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
