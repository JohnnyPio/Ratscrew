import deck

my_deck = deck.Deck()
print("Original Deck:")
print(my_deck)
my_deck.shuffle()
print("Shuffled Deck:")
print(my_deck)
print("Dealing a card:")
print(my_deck.deal())

# TODO - Going to want to have one class - card_hand. That will need at least two instances constructed, one for my
#  hand and one for the computer's hand.



