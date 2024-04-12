# TODO add a listener for the user to flip when pressing spacebar

def card_is_royal(card):
    if card[0] == "Ace":
        return True
    elif card[0] == "King":
        return True
    elif card[0] == "Queen":
        return True
    elif card[0] == "Jack":
        return True
    else:
        return False


def get_current_player_from_index(current_player_index, all_players):
    return all_players[current_player_index]


def get_index_from_player(current_player, all_players):
    return all_players.index(current_player)


def get_next_player_from_current_player(current_player, all_players):
    current_player_index = get_index_from_player(current_player, all_players)
    return all_players[(current_player_index + 1) % len(all_players)]


def get_player_before_current_player(current_player, all_players):
    current_player_index = get_index_from_player(current_player, all_players)
    return all_players[(current_player_index - 1) % len(all_players)]
