class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def is_face_card(self):
        return self.rank in ["J", "Q", "K", "A"]
