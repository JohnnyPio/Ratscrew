import game


def max_cards_to_flip(last_card):
    if last_card[0] == "Ace":
        return 4
    elif last_card[0] == "King":
        return 3
    elif last_card[0] == "Queen":
        return 2
    elif last_card[0] == "Jack":
        return 1


class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def add_cards(self, cards):
        for card in cards:
            self.cards.append(card)

    def remove_card(self, card):
        if card in self.cards:
            self.cards.remove(card)
        else:
            print("Card not found in hand.")

    def flip_single_card(self, current_pile):
        flipped_card = self.cards[0]
        print(f"{self.name}'s flipped cards is {flipped_card}")
        current_pile.add_card(flipped_card)
        self.cards.pop(0)
        return flipped_card

    def can_complete_flipping_for_royals(self, last_card, current_pile):
        max_cards = max_cards_to_flip(last_card)
        flipped_cards = []
        for _ in range(max_cards):
            if not self.cards:
                print("out of cards")
                return False

            flipped_card = self.flip_single_card(current_pile)
            flipped_cards.append(flipped_card)

            if game.card_is_royal(flipped_card):
                return True

        if not any(game.card_is_royal(card) for card in flipped_cards):
            print("no royals here")
            return False


def player_gets_pile(self, current_pile):
    self.cards.append(current_pile)


def __str__(self):
    hand_str = ""
    for card in self.cards:
        hand_str += str(card) + "\n"
    return hand_str
