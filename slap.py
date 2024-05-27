class Slap:
    def __init__(self):
        self.slapping_players = ()

    def add_player_and_slaptime_to_slap(self, player, slap_time):
        new_slapping_player_tuple = (player, slap_time)
        list_of_players = list(self.slapping_players)
        list_of_players.append(new_slapping_player_tuple)
        self.slapping_players = list_of_players
        print(f"{player.get_name()} added to slap pile")

    def get_name_of_slap_winner(self):
        slap_winner_tuple = min([(y, x) for x, y in self.slapping_players])[::-1]
        player_who_wins_slap = slap_winner_tuple[0]
        return player_who_wins_slap
