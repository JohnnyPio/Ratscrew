# TODO add a listener for the user to flip when pressing spacebar
def flip_card(player, pile):
    flipped_card = player.cards[-1]
    print(f"the flipped cards is {flipped_card}")
    pile.add_card(flipped_card)
    player.cards.pop(-1)
    if card_is_royal(flipped_card):
        print(f"royal alert - a {flipped_card[0]} has been played")


def card_is_royal(card):
    print(f"the card is a {card[0]}")
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
