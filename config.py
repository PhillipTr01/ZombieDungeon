""" Python Top Down Shooter - ZombieDungeon
    *
    *

    param:
        Author: Stefan Nemanja Banov & Phillip Tran
        Date: 06.06.2021
        Version: 1.0.0
        License: free

    Sources:
        none
"""

config = {
    # -------- Video -------- #
    'resolution_width': 1125,
    'resolution_height': 675,
    'tile_size': 75,
    'player_size': 55,
    'zombie_size': 58,
    'weapon_size': 40,
    'fps': 60,

    # ------- Pregame ------- #
    'base_rooms_per_level': 5,  # Minimum number of rooms per level
    'animation_speed': 3,
    'min_zombie_count': 2,  # Minimum number of zombies per room
    'max_zombie_count': 5,  # Maximum number of zombies per room

    # ------- Player ------- #
    'player_speed': 350,  # Pixels per Second
    'player_health': 5,
    'player_invincible_time': 50,

    # ------- Zombie ------- #
    'zombie_speed': 150,  # Pixels per Second
    'zombie_health': 3,
    'zombie_damage': 1,
    'zombie_invincible_time': 10,

    # ------- Weapons ------- #
    'weapon_speed': 10,     # Pixels per Second
    'weapon_lifetime': 900,    # in milliseconds
    'weapon_damage': 1,
    'weapon_shoot_delay': 30    # If set to 0 the player will be able to spam the weapon
}
