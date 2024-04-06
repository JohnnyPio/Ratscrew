ace = "Ace"
king = "King"
queen = "Queen"
jack = "Jack"


# TODO add a listener for the user to flip when pressing spacebar
def flip_card(player, pile):
    flipped_card = player.cards[-1]
    print(f"the flipped cards is {flipped_card}")
    pile.add_card(flipped_card)
    player.cards.pop(-1)
    if card_is_royal(flipped_card):
        print(f"royal alert - a {flipped_card[0]} has been played")
        # TODO Need to return a enum or something if this returns a royal as to what royal it is. That enum could
        #  also be used as the return value in card_is_royal instead of just "True. Maybe return the string
        #   value instead of True?


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
