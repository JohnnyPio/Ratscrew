import game


class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self, card):
        if card in self.cards:
            self.cards.remove(card)
        else:
            print("Card not found in hand.")

    def flip_single_card(self, current_pile):
        flipped_card = self.cards[-1]
        print(f"{self.name}'s flipped cards is {flipped_card}")
        current_pile.add_card(flipped_card)
        self.cards.pop(-1)
        return flipped_card

# TODO Refactor into a single "flip_for_royal" method

    def flip_for_ace(self, current_pile):
        for _ in range(4):
            flipped_card = self.flip_single_card(current_pile)
            if game.card_is_royal(flipped_card):
                break

    def flip_for_king(self, current_pile):
        for _ in range(3):
            flipped_card = self.flip_single_card(current_pile)
            if game.card_is_royal(flipped_card):
                break

    def flip_for_queen(self, current_pile):
        for _ in range(2):
            flipped_card = self.flip_single_card(current_pile)
            if game.card_is_royal(flipped_card):
                break

    def flip_for_jack(self, current_pile):
        for _ in range(1):
            flipped_card = self.flip_single_card(current_pile)
            if game.card_is_royal(flipped_card):
                break

    def __str__(self):
        hand_str = ""
        for card in self.cards:
            hand_str += str(card) + "\n"
        return hand_str
