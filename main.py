import player
import game

players_hands = []
computer_player = player.Player("computer")
computer_player.set_computer_player()
players_hands.append(computer_player)
player_1 = player.Player("player1")
players_hands.append(player_1)

difficulty = input("Set game difficulty (1 = Easy | 2 = Medium | 3 = Hard): ")

my_game = game.Game(players_hands, difficulty)
# TODO Fix bug where royal pile has slappable event and clobbers slap opp
my_game.initialize_game()
my_game.run_the_game()
