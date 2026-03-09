import os
import sys


def _resource_path(relative_path):
    """Return the correct path whether running from source or a PyInstaller bundle."""
    base = getattr(sys, '_MEIPASS', os.path.join(os.path.dirname(__file__), '..'))
    return os.path.join(base, relative_path)


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def is_face_card(self):
        return self.rank in ["J", "Q", "K", "A"]

    def face_card_count(self):
        return {"J": 1, "Q": 2, "K": 3, "A": 4}.get(self.rank, 0)

    def image_filename(self):
        rank_map = {"J": "jack", "Q": "queen", "K": "king", "A": "ace"}
        rank = rank_map.get(self.rank, self.rank)
        suit = self.suit.lower()
        return _resource_path(os.path.join("ui", "assets", f"{rank}_of_{suit}.png"))
