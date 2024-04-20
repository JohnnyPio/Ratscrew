class Slap:
    def __init__(self):
        self.slapping_players = ()

    def add_player_to_slap_pile(self, player, slap_time):
        new_slapping_player_tuple = (player, slap_time)
        self.slapping_players = new_slapping_player_tuple
        print(f"{player.name} added to slap pile")

