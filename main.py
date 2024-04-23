import player
import game

players_hands = []
computer_player = player.Player("computer")
computer_player.set_computer_player()
players_hands.append(computer_player)
player_1 = player.Player("player1")
players_hands.append(player_1)


def run_the_game():
    both_players_have_more_than_zero_cards = True
    while both_players_have_more_than_zero_cards and my_game.should_continue_dealing:
        my_game.get_next_player_from_current_player()

        if not game.card_is_royal(my_game.pile.get_top_card()):
            my_game.current_player.flip_single_card(my_game.pile)
            my_game.notify_observers()
        else:
            if not my_game.can_complete_flipping_for_royals():
                my_game.player_wins_the_pile()

        if not my_game.all_players_have_cards():
            break


def test(pile):
    if pile.matching_sandwich_cards() or pile.matching_top_cards():
        print("Slap time")
        my_game.stop_dealing()


my_game = game.Game(players_hands)
my_game.add_observer(test)
run_the_game()
