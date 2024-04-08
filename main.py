import deck
import player
import game

my_deck = deck.Deck()
my_deck.shuffle()
pile = deck.Deck()
pile.empty()

computer_player = player.Player("computer")
player_1 = player.Player("player1")
players_hands = [computer_player, player_1]
my_deck.initial_full_deck_deal_to_all_players(players_hands)





# TODO Someway to flip turns after each player is done

while len(computer_player.cards) > 0 or len(player_1.cards) > 0:
    comp_card = computer_player.flip_single_card(pile)
    if game.card_is_royal(comp_card) == "Ace":
        player_1.flip_for_ace(pile)
    if game.card_is_royal(comp_card) == "King":
        player_1.flip_for_king(pile)
    if game.card_is_royal(comp_card) == "Queen":
        player_1.flip_for_queen(pile)
    if game.card_is_royal(comp_card) == "Jack":
        player_1.flip_for_jack(pile)
    player_1.flip_single_card(pile)

