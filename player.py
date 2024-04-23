import game


def add_card_to_pile(current_pile, flipped_card):
    current_pile.add_card(flipped_card)


class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.has_slapped = False
        self.isbot = False

    def __str__(self):
        hand_str = ""
        for card in self.cards:
            hand_str += str(card) + "\n"
        return hand_str

    def add_card(self, card):
        self.cards.append(card)

    def remove_top_card_from_hand(self):
        self.cards.pop(0)

    def add_cards(self, cards):
        for card in cards:
            self.cards.append(card)

    # TODO This needs to be broken up. Perhaps moved into game. And have the notify observer here.
    def flip_single_card(self, current_pile):
        flipped_card = self.cards[0]
        print(f"{self.name}'s flipped cards is {flipped_card}")
        add_card_to_pile(current_pile, flipped_card)
        self.remove_top_card_from_hand()
        game.delay_between_card_flips()
        return flipped_card

    def set_as_slapped(self):
        self.has_slapped = True

    def set_computer_player(self):
        self.isbot = True

    def is_player_a_bot(self):
        if self.isbot:
            return True
        else:
            return False
