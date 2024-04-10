import deck
import player
import game
from player import Player

my_game = game.Game()
pile = my_game.pile

my_game.add_player(player.Player("computer"))
my_game.add_player(player.Player("player1"))
# TODO fix this for more than 2 players
my_game.dealing_deck.initial_full_deck_deal_to_all_players(my_game.dealing_deck, my_game.players)


player_index = 0
current_player = my_game.players[player_index]
current_player.flip_single_card(pile)

both_players_have_more_than_zero_cards = True
while both_players_have_more_than_zero_cards:
    current_card = pile.cards[-1]
    player_index = (player_index + 1) % len(my_game.players)
    current_player = my_game.players[player_index]

    if game.card_is_royal(current_card):
        print(f"the current player is {current_player.name}")
        if not current_player.flip_for_royal(current_card, pile):
            player_before = my_game.players[
                (player_index - 1) % len(my_game.players)]  # TODO Write method for getting the player before
            pile.shuffle()
            player_before.add_cards(list(pile.cards))
            pile.cards = []  # TODO why doesn't pile.empty() work here?
            player_before.flip_single_card(pile)
    else:
        current_player.flip_single_card(pile)

    if len(my_game.players[0].cards) == 0:
        both_players_have_more_than_zero_cards = False
        print(f"computer_player loses")
        break
    if len(my_game.players[1].cards) == 0:
        both_players_have_more_than_zero_cards = False
        print(f"player_1 wins")
        break
