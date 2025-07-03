import os

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def is_face_card(self):
        return self.rank in ["J", "Q", "K", "A"]

    def image_filename(self):
        rank_map = {"J": "jack", "Q": "queen", "K": "king", "A": "ace"}
        rank = rank_map.get(self.rank, self.rank)
        suit = self.suit.lower()
        return os.path.join("ui", "assets", f"{rank}_of_{suit}.png")