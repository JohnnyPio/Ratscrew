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

    def __str__(self):
        hand_str = ""
        for card in self.cards:
            hand_str += str(card) + "\n"
        return hand_str

