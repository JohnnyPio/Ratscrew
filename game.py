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
