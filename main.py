import deck
import player

my_deck = deck.Deck()
my_deck.shuffle()
pile = deck.Deck()
pile.empty()

computer_player = player.Player("computer")
player_1 = player.Player("player1")
players_hands = [computer_player, player_1]

my_deck.initial_full_deck_deal_to_all_players(players_hands)

# TODO Should probably make a new Game class that involves a flip method for each player. Likely will need to inherit from the player classes. Will also need a pile class as well.
while computer_player.cards.__len__() > 0 or player_1.cards.__len__ > 0:
    print(computer_player.cards[-1])
    pile.add_card(computer_player.cards[-1])
    computer_player.cards.pop(-1)

    print(player_1.cards[-1])
    pile.add_card(player_1.cards[-1])
    player_1.cards.pop(-1)

    print(f"pile is {pile} and length is {pile.__len__()}")
