import tkinter as tk
import os
from PIL import Image, ImageTk, ImageDraw
from game.deck import Deck
from game.player import Player
from game.rules import GameRules


DIFFICULTIES = {
    "Easy":   {"play_delay": 3000, "slap_delay": 3500},
    "Medium": {"play_delay": 1500, "slap_delay": 1800},
    "Hard":   {"play_delay": 500,  "slap_delay": 400},
}

PILE_SHOW_DELAY = 1500

# --- Palette ---
TABLE_BG    = "#2b5c3e"   # deep felt green
SECTION_BG  = "#1f4530"   # darker green for player panels
TEXT_FG     = "#f0e6c8"   # warm cream
MUTED_FG    = "#a8c4a2"   # muted green-cream for secondary text
GOLD        = "#d4af37"   # gold accent
CHALLENGE_FG = "#ff8c42"  # orange for challenge warnings
BTN_PLAY_BG = "#3a7d52"
BTN_PLAY_ACT = "#2e6342"
BTN_SLAP_BG = "#8b1a1a"
BTN_SLAP_ACT = "#6e1414"
RADIO_SEL   = "#5a9e72"

CARD_W, CARD_H = 160, 232
CARD_RADIUS = 12


def _styled_button(parent, text, bg, active_bg, command=None, font_size=13):
    return tk.Button(
        parent, text=text, command=command,
        bg=bg, fg=TEXT_FG,
        activebackground=active_bg, activeforeground=TEXT_FG,
        font=("Georgia", font_size, "bold"),
        relief=tk.FLAT, bd=0,
        padx=24, pady=10,
        cursor="hand2",
        disabledforeground="#666666",
    )


def _card_slot(parent):
    """A fixed-size frame that holds a card image label without resizing."""
    container = tk.Frame(parent, width=CARD_W, height=CARD_H, bg=SECTION_BG)
    container.pack_propagate(False)
    label = tk.Label(container, bg=SECTION_BG)
    label.pack(expand=True, fill=tk.BOTH)
    return container, label


def start_game():
    root = tk.Tk()
    root.title("Egyptian Rat Screw")
    root.geometry("500x900")
    root.resizable(False, False)
    root.configure(bg=TABLE_BG)

    deck = Deck()
    p1_hand, p2_hand = deck.deal()
    p1 = Player("You", p1_hand)
    p2 = Player("Computer", p2_hand)
    game = GameRules(p1, p2)

    def _load_image(path):
        raw = Image.open(path).resize((CARD_W, CARD_H), Image.LANCZOS)

        # Flatten RGBA onto white first — avoids black where alpha was transparent
        card = Image.new("RGB", (CARD_W, CARD_H), (255, 255, 255))
        if raw.mode == "RGBA":
            card.paste(raw.convert("RGB"), mask=raw.getchannel("A"))
        else:
            card.paste(raw.convert("RGB"))

        # Rounded corner mask
        mask = Image.new("L", (CARD_W, CARD_H), 0)
        ImageDraw.Draw(mask).rounded_rectangle(
            [0, 0, CARD_W - 1, CARD_H - 1], radius=CARD_RADIUS, fill=255
        )

        # Composite white card onto panel background (corners become the felt colour)
        bg_rgb = tuple(int(SECTION_BG[i:i + 2], 16) for i in (1, 3, 5))
        result = Image.new("RGB", (CARD_W, CARD_H), bg_rgb)
        result.paste(card, mask=mask)

        # Thin border
        ImageDraw.Draw(result).rounded_rectangle(
            [0, 0, CARD_W - 1, CARD_H - 1], radius=CARD_RADIUS,
            outline="#aaaaaa", width=1
        )

        return ImageTk.PhotoImage(result)

    # Load card back once
    back_path = os.path.join("ui", "assets", "back.png")
    back_img = _load_image(back_path) if os.path.exists(back_path) else None

    # ── Title ────────────────────────────────────────────────────
    tk.Label(root, text="EGYPTIAN RAT SCREW",
             font=("Georgia", 18, "bold"), bg=TABLE_BG, fg=GOLD
             ).pack(pady=(18, 4))

    # ── Computer panel ───────────────────────────────────────────
    comp_panel = tk.Frame(root, bg=SECTION_BG, pady=12)
    comp_panel.pack(fill=tk.X, padx=20, pady=(4, 0))

    comp_name_label = tk.Label(comp_panel, text="COMPUTER",
                               font=("Georgia", 11, "bold"), bg=SECTION_BG, fg=MUTED_FG)
    comp_name_label.pack()
    computer_count_label = tk.Label(comp_panel, text=f"{p2.card_count()} cards",
                                    font=("Georgia", 12), bg=SECTION_BG, fg=TEXT_FG)
    computer_count_label.pack()
    _, computer_card_label = _card_slot(comp_panel)
    computer_card_label.master.pack(pady=8)

    # ── Status area ──────────────────────────────────────────────
    status_frame = tk.Frame(root, bg=TABLE_BG)
    status_frame.pack(fill=tk.X, padx=20, pady=8)

    output = tk.Label(status_frame, text="Press Play Card or Enter to start.",
                      font=("Georgia", 12), bg=TABLE_BG, fg=TEXT_FG,
                      wraplength=440, justify=tk.CENTER)
    output.pack()

    challenge_status = tk.Label(status_frame, text="",
                                font=("Georgia", 11, "bold"), bg=TABLE_BG, fg=CHALLENGE_FG)
    challenge_status.pack(pady=(2, 0))

    # ── Player panel ─────────────────────────────────────────────
    player_panel = tk.Frame(root, bg=SECTION_BG, pady=12)
    player_panel.pack(fill=tk.X, padx=20, pady=(0, 4))

    _, player_card_label = _card_slot(player_panel)
    player_card_label.master.pack(pady=8)
    player_count_label = tk.Label(player_panel, text=f"{p1.card_count()} cards",
                                  font=("Georgia", 12), bg=SECTION_BG, fg=TEXT_FG)
    player_count_label.pack()
    tk.Label(player_panel, text="YOU",
             font=("Georgia", 11, "bold"), bg=SECTION_BG, fg=MUTED_FG).pack()

    # ── Difficulty selector ───────────────────────────────────────
    diff_frame = tk.Frame(root, bg=TABLE_BG)
    diff_frame.pack(pady=(10, 4))
    tk.Label(diff_frame, text="Difficulty:", font=("Georgia", 11),
             bg=TABLE_BG, fg=MUTED_FG).pack(side=tk.LEFT, padx=(0, 8))
    difficulty_var = tk.StringVar(value="Medium")
    for name in DIFFICULTIES:
        tk.Radiobutton(
            diff_frame, text=name, variable=difficulty_var, value=name,
            font=("Georgia", 11),
            bg=TABLE_BG, fg=TEXT_FG,
            selectcolor=SECTION_BG, activebackground=TABLE_BG, activeforeground=TEXT_FG,
            indicatoron=0,
            padx=10, pady=4,
            relief=tk.FLAT, bd=1,
        ).pack(side=tk.LEFT, padx=3)

    # ── Buttons ──────────────────────────────────────────────────
    btn_frame = tk.Frame(root, bg=TABLE_BG)
    btn_frame.pack(pady=10)
    play_btn = _styled_button(btn_frame, "▶  Play Card  [Enter]", BTN_PLAY_BG, BTN_PLAY_ACT)
    play_btn.pack(side=tk.LEFT, padx=8)
    slap_btn = _styled_button(btn_frame, "✋  Slap!  [Space]", BTN_SLAP_BG, BTN_SLAP_ACT)
    slap_btn.pack(side=tk.LEFT, padx=8)

    # ── Scheduled job handles ────────────────────────────────────
    computer_play_job = [None]
    computer_slap_job = [None]

    # ── Helpers ──────────────────────────────────────────────────

    def get_delays():
        return DIFFICULTIES[difficulty_var.get()]

    def show_card_image(label, card):
        path = card.image_filename()
        try:
            img = _load_image(path)
            label.config(image=img, text="")
            label.image = img
        except Exception:
            label.config(image="", text=str(card), fg=TEXT_FG, font=("Georgia", 10))

    def reset_card_to_back(label):
        if back_img:
            label.config(image=back_img, text="")
            label.image = back_img
        else:
            label.config(image="", text="")

    def update_card_counts():
        player_count_label.config(text=f"{p1.card_count()} cards")
        computer_count_label.config(text=f"{p2.card_count()} cards")

    def clear_cards():
        reset_card_to_back(player_card_label)
        reset_card_to_back(computer_card_label)
        challenge_status.config(text="")

    def set_play_enabled(enabled):
        play_btn.config(state=tk.NORMAL if enabled else tk.DISABLED)

    def set_all_enabled(enabled):
        state = tk.NORMAL if enabled else tk.DISABLED
        play_btn.config(state=state)
        slap_btn.config(state=state)

    def cancel_computer_jobs():
        if computer_play_job[0]:
            root.after_cancel(computer_play_job[0])
            computer_play_job[0] = None
        if computer_slap_job[0]:
            root.after_cancel(computer_slap_job[0])
            computer_slap_job[0] = None

    def check_game_over():
        if not p1.has_cards():
            cancel_computer_jobs()
            clear_cards()
            output.config(text="You have no more cards.  Game over.", fg=BTN_SLAP_BG)
            set_all_enabled(False)
            return True
        if not p2.has_cards():
            cancel_computer_jobs()
            clear_cards()
            output.config(text="Computer is out of cards.  You win!", fg=GOLD)
            set_all_enabled(False)
            return True
        return False

    def schedule_computer_actions():
        cancel_computer_jobs()
        delays = get_delays()
        if len(game.pile) >= 2 and game.pile[-1].rank == game.pile[-2].rank:
            computer_slap_job[0] = root.after(delays["slap_delay"], _computer_slap)
        if game.turn == p2:
            set_play_enabled(False)
            computer_play_job[0] = root.after(delays["play_delay"], _computer_play)
        else:
            set_play_enabled(True)

    def _after_pile_shown():
        clear_cards()
        output.config(fg=TEXT_FG)
        if not check_game_over():
            schedule_computer_actions()

    def _handle_result(result):
        update_card_counts()
        if check_game_over():
            return
        if result is None:
            schedule_computer_actions()
            return

        player, card = result
        if player == p1:
            show_card_image(player_card_label, card)
        else:
            show_card_image(computer_card_label, card)

        if game.last_pile_winner:
            set_all_enabled(False)
            winner_name = game.last_pile_winner.name
            output.config(
                text=f"{player.name} played {card}.  {winner_name} claimed the pile!",
                fg=GOLD,
            )
            challenge_status.config(text="")
            root.after(PILE_SHOW_DELAY, _after_pile_shown)
        else:
            if game.challenge_count > 0:
                text = (f"{player.name} played {card}.  "
                        f"{game.challenge_player.name} played a royal — "
                        f"{game.challenge_count} chance(s) remain.")
                challenge_status.config(
                    text=f"⚔  Challenge: {game.challenge_count} card(s) left")
            else:
                text = f"{player.name} played {card}.  Slap if you see a match!"
                challenge_status.config(text="")
            output.config(text=text, fg=TEXT_FG)
            schedule_computer_actions()

    def _computer_play():
        computer_play_job[0] = None
        _handle_result(game.play_one())

    def _computer_slap():
        computer_slap_job[0] = None
        if game.slap(p2):
            cancel_computer_jobs()
            update_card_counts()
            set_all_enabled(False)
            output.config(text="Computer slapped and claimed the pile!", fg=CHALLENGE_FG)
            challenge_status.config(text="")
            root.after(PILE_SHOW_DELAY, _after_pile_shown)

    def play_one(event=None):
        if game.turn != p1:
            return
        cancel_computer_jobs()
        _handle_result(game.play_one())

    def slap(event=None):
        cancel_computer_jobs()
        if game.slap(p1):
            update_card_counts()
            set_all_enabled(False)
            output.config(text="You slapped and claimed the pile!", fg=GOLD)
            challenge_status.config(text="")
            root.after(PILE_SHOW_DELAY, _after_pile_shown)
        else:
            output.config(text="Bad slap!  Nothing happens.", fg=CHALLENGE_FG)
            schedule_computer_actions()

    play_btn.config(command=play_one)
    slap_btn.config(command=slap)
    root.bind("<space>", slap)
    root.bind("<Return>", play_one)

    # Initialise both slots with the card back
    clear_cards()

    root.mainloop()
