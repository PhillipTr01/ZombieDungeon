""" Python Top Down Shooter - ZombieDungeon
    *
    * This file is used as config
        - You can change many options here

    param:
        Author: Stefan Nemanja Banov & Phillip Tran
        Date: 06.06.2021
        Version: 1.0.0
        License: free

"""

config = {
    # -------- Video_Settings -------- #
    'resolution_width': 1125,
    'resolution_height': 675,
    'tile_size': 75,
    'player_size': 60,
    'zombie_size': 65,
    'fps': 60,

    # ------- Pregame_Settings ------- #
    'base_rooms_per_level': 5,
    'animation_speed': 3,
    'player_speed': 350,  # Pixels per Second
    'zombie_speed': 150,
    'zombie_damage': 1,
    'max_health_player': 5,
    'zombie_health': 2
}
