class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.has_slapped = False
        self.isbot = False

    def __str__(self):
        hand_str = ""
        for card in self.cards:
            hand_str += str(card) + "\n"
        return hand_str

### GET/SET Methods
    def set_as_slapped(self):
        self.has_slapped = True

    def set_computer_player(self):
        self.isbot = True

    def get_number_of_cards(self):
        return len(self.cards)

    def get_name(self):
        return self.name

    def is_player_a_bot(self):
        if self.isbot:
            return True
        else:
            return False

    def get_top_card_of_player(self):
        if len(self.cards) > 0:
            return self.cards[0]

### OTHER METHODS
    def add_card(self, card):
        self.cards.append(card)

    def remove_top_card_from_hand(self):
        self.cards.pop(0)

    def add_cards(self, cards):
        for card in cards:
            self.cards.append(card)

    def flip_single_card(self):
        flipped_card = self.get_top_card_of_player()
        print(f"{self.name}'s flipped cards is {flipped_card}")
        return flipped_card

