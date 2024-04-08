ace = "Ace"
king = "King"
queen = "Queen"
jack = "Jack"


# TODO add a listener for the user to flip when pressing spacebar

def card_is_royal(card):
    print(f"the card is a {card[0]}")
    if card[0] == ace:
        return ace
    elif card[0] == king:
        return king
    elif card[0] == queen:
        return queen
    elif card[0] == jack:
        return jack
    else:
        return False
