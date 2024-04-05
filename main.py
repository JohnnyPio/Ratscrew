import deck
import player

my_deck = deck.Deck()
my_deck.shuffle()

computer_player = player.Player("computer")
player_1 = player.Player("player1")
list_of_players = [computer_player, player_1]

deck.initial_full_deck_deal_to_all_players(my_deck, list_of_players)
print(f"computer player is {computer_player}")
print(f"player1 is {player_1}")

# TODO Should probably make a new Game class that involves a flip method for each player. Likely will need to inherit from the player classes. Will also need a pile class as well.
