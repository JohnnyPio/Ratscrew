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
# TODO Fix lots of bugs where player1 also buries a card after slapping, see observer
# TODO Fix end of game rules where the player can stay alive if they have a royal and it still needs to be played by the opponent
# TODO Fix stash
my_game.initialize_game()
my_game.run_the_game()
