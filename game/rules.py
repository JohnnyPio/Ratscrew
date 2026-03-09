class GameRules:
    def __init__(self, player1, player2):
        self.p1 = player1
        self.p2 = player2
        self.pile = []
        self.turn = self.p1
        self.challenge_count = 0
        self.challenge_player = None  # player who wins the pile if the challenge fails
        self.last_pile_winner = None

    def get_game_state(self):
        return {
            'turn': self.turn.name,
            'pile': [str(card) for card in self.pile],
            'pile_size': len(self.pile),
            'challenge_count': self.challenge_count,
            'challenge_player': self.challenge_player.name if self.challenge_player else None,
            'player_counts': {
                self.p1.name: self.p1.card_count(),
                self.p2.name: self.p2.card_count()
            }
        }

    def play_one(self):
        self.last_pile_winner = None

        card = self.turn.play_card()
        if not card:
            if self.challenge_count > 0:
                self._resolve_challenge(self.challenge_player)
            return None

        self.pile.append(card)
        played_by = self.turn

        if self.challenge_count > 0:
            self._respond_to_challenge(card)
        else:
            self._play_normal(card)

        return played_by, card

    def _play_normal(self, card):
        if card.is_face_card():
            self.challenge_player = self.turn
            self.challenge_count = card.face_card_count()
        self.next_turn()

    def _respond_to_challenge(self, card):
        if card.is_face_card():
            # Counter-challenge: this player becomes the new pile winner,
            # and the opponent is now the responder.
            self.challenge_player = self.turn
            self.challenge_count = card.face_card_count()
            self.next_turn()
        else:
            self.challenge_count -= 1
            if self.challenge_count == 0:
                self._resolve_challenge(self.challenge_player)
            # else: no next_turn — the responder keeps playing

    def _resolve_challenge(self, winner):
        self.claim_pile(winner)
        self.turn = winner
        self.challenge_player = None
        self.challenge_count = 0

    def next_turn(self):
        self.turn = self.p1 if self.turn == self.p2 else self.p2

    def slap(self, player=None):
        if len(self.pile) >= 2 and self.pile[-1].rank == self.pile[-2].rank:
            slapper = player or self.p1
            self.claim_pile(slapper)
            self.challenge_count = 0
            self.challenge_player = None
            self.turn = slapper
            return True
        return False

    def claim_pile(self, player):
        player.add_cards(self.pile)
        self.pile.clear()
        self.last_pile_winner = player
