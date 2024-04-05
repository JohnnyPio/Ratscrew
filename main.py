import deck

my_deck = deck.Deck()
print("Original Deck:")
print(my_deck)
my_deck.shuffle()
print("Shuffled Deck:")
print(my_deck)
print("Dealing a card:")
print(my_deck.deal())
