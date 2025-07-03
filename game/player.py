class Player:
    def __init__(self, name, hand):
        self.name = name
        self.hand = hand

    def play_card(self):
        return self.hand.pop(0) if self.hand else None

    def add_cards(self, cards):
        self.hand.extend(cards)

    def has_cards(self):
        return bool(self.hand)