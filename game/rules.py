class GameRules:
    def __init__(self, player1, player2):
        self.p1 = player1
        self.p2 = player2
        self.pile = []
        self.turn = self.p1
        self.challenge_count = 0
        self.challenge_player = None
        self._waiting_for_clear = False

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
        if self._waiting_for_clear:
            self._waiting_for_clear = False
            return None

        card = self.turn.play_card()
        if not card:
            if self.challenge_count > 0:
                print(f"{self.turn.name} ran out of cards during challenge.")
                self.claim_pile(self.challenge_player)
                self.turn = self.challenge_player
                self.challenge_player = None
                self.challenge_count = 0
            return None

        self.pile.append(card)

        if self.challenge_count > 0:
            return self._handle_challenge(card)
        else:
            return self._handle_normal(card)

    def _handle_normal(self, card):
        if card.is_face_card():
            self.challenge_player = self.turn
            self.challenge_count = card.face_card_count()
            self.next_turn()
        else:
            self.next_turn()
        return self.turn, card

    def _handle_challenge(self, card):
        print(f"CHALLENGE: {self.turn.name} plays {card}")

        if self.turn == self.challenge_player:
            print("Challenger tried to play during challenge. Ignored.")
            self.next_turn()
            return None

        if card.is_face_card():
            self.challenge_player = self.turn
            self.challenge_count = card.face_card_count()
            print(f"New face card: {card}. {self.turn.name} becomes challenger with {self.challenge_count} tries.")
            self.next_turn()
        else:
            self.challenge_count -= 1
            print(f"No face card. Remaining tries: {self.challenge_count}")

            if self.challenge_count == 0:
                print(f"Challenge failed. {self.challenge_player.name} wins the pile.")
                self.claim_pile(self.challenge_player)
                self.turn = self.challenge_player
                self.challenge_player = None
            else:
                self.next_turn()

        return self.turn, card

    def next_turn(self):
        self.turn = self.p1 if self.turn == self.p2 else self.p2

    def slap(self):
        if len(self.pile) >= 2 and self.pile[-1].rank == self.pile[-2].rank:
            self.claim_pile(self.p1)
            self.challenge_count = 0
            self.challenge_player = None
            return True
        return False

    def claim_pile(self, player):
        print(f"{player.name} claims pile of {len(self.pile)} cards.")
        player.add_cards(self.pile)
        self.pile.clear()
        self._waiting_for_clear = True
