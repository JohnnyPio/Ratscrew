import tkinter as tk
from tkinter import PhotoImage
import os
from game.deck import Deck
from game.player import Player
from game.rules import GameRules


def start_game():
    root = tk.Tk()
    root.title("Egyptian Ratscrew")
    root.geometry("500x1000")

    deck = Deck()
    p1_hand, p2_hand = deck.deal()
    p1 = Player("You", p1_hand)
    p2 = Player("Computer", p2_hand)
    game = GameRules(p1, p2)

    output = tk.Label(root, text="Welcome to Egyptian Ratscrew!", font=("Arial", 14))
    output.pack(pady=10)

    frame = tk.Frame(root)
    frame.pack(pady=10)

    computer_label = tk.Label(frame, text="Computer:")
    computer_label.grid(row=0, column=0, padx=10)
    computer_card_label = tk.Label(frame)
    computer_card_label.grid(row=0, column=1, padx=10)

    player_label = tk.Label(frame, text="You:")
    player_label.grid(row=1, column=0, padx=10)
    player_card_label = tk.Label(frame)
    player_card_label.grid(row=1, column=1, padx=10)

    def show_card_image(label, card):
        if not card:
            label.config(image="")
            return
        path = card.image_filename()
        if os.path.exists(path):
            img = PhotoImage(file=path)
            label.config(image=img)
            label.image = img  # Keep reference to avoid garbage collection
        else:
            label.config(text=str(card))

    def deal_one(event=None):
        player, card = game.play_one()
        if player == p1:
            show_card_image(player_card_label, card)
        else:
            show_card_image(computer_card_label, card)

        if not p1.has_cards():
            output.config(text="You have no more cards. Game over.")
        elif not p2.has_cards():
            output.config(text="Computer has no more cards. You win!")
        else:
            output.config(text=f"{player.name} played {card}. Slap now if needed.")

        game.next_turn()

    def slap(event=None):
        if game.slap():
            game.claim_pile(p1)
            output.config(text="Slap successful! You claimed the pile.")
            player_card_label.config(image="")
            computer_card_label.config(image="")
        else:
            output.config(text="Bad slap! Nothing happens.")

    tk.Button(root, text="Deal Card", command=deal_one).pack(pady=5)
    tk.Button(root, text="Slap!", command=slap).pack(pady=5)

    root.bind("<Return>", deal_one)
    root.bind("<space>", slap)

    root.mainloop()
