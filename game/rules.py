class GameRules:
    def __init__(self, player1, player2):
        self.p1 = player1
        self.p2 = player2
        self.pile = []
        self.turn = self.p1  # Start with player 1
        self.challenge_count = 0
        self.challenge_player = None

    def play_one(self):
        # During challenge, only non-challenger can play
        if self.challenge_count > 0 and self.turn == self.challenge_player:
            return self.turn, None

        card = self.turn.play_card()
        if card:
            self.pile.append(card)

            if card.is_face_card():
                self.challenge_count = card.face_card_count()
                self.challenge_player = self.turn
                self.next_turn()
            elif self.challenge_count > 0:
                self.challenge_count -= 1
                if card.is_face_card():
                    self.challenge_count = card.face_card_count()
                    self.challenge_player = self.turn
                    self.next_turn()
                elif self.challenge_count == 0:
                    self.claim_pile(self.challenge_player)
                    self.challenge_player = None
                    self.next_turn()
            else:
                self.next_turn()

        return self.turn, card

    def next_turn(self):
        self.turn = self.p1 if self.turn == self.p2 else self.p2

    def slap(self):
        if len(self.pile) >= 2 and self.pile[-1].rank == self.pile[-2].rank:
            self.claim_pile(self.p1)  # Human wins on slap
            self.challenge_count = 0
            self.challenge_player = None
            return True
        return False

    def claim_pile(self, player):
        player.add_cards(self.pile)
        self.pile.clear()