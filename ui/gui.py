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

    challenge_status = tk.Label(root, text="", font=("Arial", 12))
    challenge_status.pack()

    card_counts = tk.Frame(root)
    card_counts.pack(pady=5)
    player_count_label = tk.Label(card_counts, text=f"You: {p1.card_count()} cards", font=("Arial", 12))
    player_count_label.pack(side=tk.LEFT, padx=20)
    computer_count_label = tk.Label(card_counts, text=f"Computer: {p2.card_count()} cards", font=("Arial", 12))
    computer_count_label.pack(side=tk.RIGHT, padx=20)

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

    def update_card_counts():
        player_count_label.config(text=f"You: {p1.card_count()} cards")
        computer_count_label.config(text=f"Computer: {p2.card_count()} cards")

    def clear_cards():
        player_card_label.config(image="")
        computer_card_label.config(image="")
        challenge_status.config(text="")

    def play_one(event=None):
        result = game.play_one()
        update_card_counts()

        if not p1.has_cards():
            clear_cards()
            output.config(text="You have no more cards. Game over.")
            return
        elif not p2.has_cards():
            clear_cards()
            output.config(text="Computer has no more cards. You win!")
            return

        if result is None:
            return

        player, card = result

        if game.last_pile_winner:
            clear_cards()
            output.config(text=f"{player.name} played {card}. {game.last_pile_winner.name} claimed the pile!")
            return

        if player == p1:
            show_card_image(player_card_label, card)
        else:
            show_card_image(computer_card_label, card)

        if game.challenge_count > 0:
            text = f"{player.name} played {card}. {game.challenge_player.name} played a royal! {game.challenge_count} chance(s) remain."
            challenge_status.config(text=f"Challenge: {game.challenge_count} card(s) left")
        else:
            text = f"{player.name} played {card}. Slap now if needed."
            challenge_status.config(text="")
        output.config(text=text)

    def slap(event=None):
        if game.slap(p1):
            output.config(text="Slap successful! You claimed the pile.")
            clear_cards()
            update_card_counts()
        else:
            output.config(text="Bad slap! Nothing happens.")

    tk.Button(root, text="Play Card", command=play_one).pack(pady=5)
    tk.Button(root, text="Slap!", command=slap).pack(pady=5)

    root.bind("<space>", slap)
    root.bind("<Return>", play_one)

    root.mainloop()
