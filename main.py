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

# TODO Should probably make a new Game class that involves a flip method for each player. Likely will need to inherit from the player classes. Will also need a pile class as well.
while len(computer_player.cards) > 0 or len(player_1.cards) > 0:
    game.flip_card(computer_player, pile)
    game.flip_card(player_1, pile)
