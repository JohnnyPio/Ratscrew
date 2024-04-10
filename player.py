import game


class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def add_cards(self, cards):
        for card in cards:
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

    # TODO More refactoring needed. Need to have a way to know if player runs out of cards
    def flip_for_royal(self, last_card, current_pile):
        max_cards = 0
        flipped_cards = []
        if last_card[0] == "Ace":
            max_cards = 4
            for _ in range(max_cards):
                if len(self.cards) > 0:
                    flipped_card = self.flip_single_card(current_pile)
                    flipped_cards.append(flipped_card)
                    if game.card_is_royal(flipped_card):
                        return True
                else:
                    print("out of cards")
                    return False
            for card in flipped_cards:
                if not game.card_is_royal(card):
                    print("no royals here")
                    return False
            # TODO Add handling for player running out of cards
        elif last_card[0] == "King":
            max_cards = 3
            for _ in range(3):
                flipped_card = self.flip_single_card(current_pile)
                flipped_cards.append(flipped_card)
                if game.card_is_royal(flipped_card):
                    return True
            for card in flipped_cards:
                if not game.card_is_royal(card):
                    print("no royals here")
                    return False
        elif last_card[0] == "Queen":
            max_cards = 2
            for _ in range(max_cards):
                flipped_card = self.flip_single_card(current_pile)
                flipped_cards.append(flipped_card)
                if game.card_is_royal(flipped_card):
                    return True
            for card in flipped_cards:
                if not game.card_is_royal(card):
                    print("no royals here")
                    return False
        elif last_card[0] == "Jack":
            max_cards = 1
            for _ in range(max_cards):
                flipped_card = self.flip_single_card(current_pile)
                flipped_cards.append(flipped_card)
                if game.card_is_royal(flipped_card):
                    return True
            for card in flipped_cards:
                if not game.card_is_royal(card):
                    print("no royals here")
                    return False

    def player_gets_pile(self, current_pile):
        self.cards.append(current_pile)

    def __str__(self):
        hand_str = ""
        for card in self.cards:
            hand_str += str(card) + "\n"
        return hand_str
