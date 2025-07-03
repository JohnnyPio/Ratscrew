class GameRules:
    def __init__(self, player1, player2):
        self.p1 = player1
        self.p2 = player2
        self.pile = []
        self.turn = self.p1  # Start with player 1

    def play_one(self):
        card = self.turn.play_card()
        if card:
            self.pile.append(card)
        return self.turn, card

    def next_turn(self):
        self.turn = self.p1 if self.turn == self.p2 else self.p2

    def slap(self):
        if len(self.pile) >= 2 and self.pile[-1].rank == self.pile[-2].rank:
            return True
        return False

    def claim_pile(self, player):
        player.add_cards(self.pile)
        self.pile.clear()