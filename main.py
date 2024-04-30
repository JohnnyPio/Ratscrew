import player
import game

players_hands = []
computer_player = player.Player("computer")
computer_player.set_computer_player()
players_hands.append(computer_player)
player_1 = player.Player("player1")
players_hands.append(player_1)

my_game = game.Game(players_hands)
#TODO Now that we have the slap and card observers, we should make an observer class with names
#TODO Fix: The number of cards gets larger on each slap
my_game.add_observer(my_game.monitor_for_slaps)
my_game.add_observer(my_game.all_players_have_cards)
my_game.initialize_game()
my_game.run_the_game()
