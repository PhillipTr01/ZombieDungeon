""" Python Top Down Shooter - ZombieDungeon
    *
    * This class portrays the rooms
        - It contains all pre-made rooms

    param:
        Author: Stefan Nemanja Banov & Phillip Tran
        Date: 06.06.2021
        Version: 1.0.0
        License: free

"""

w = "w"  # Wall
g = "g"  # Ground
d = "d"  # Door
p = "p"  # Player Spawn
z = "z"  # Zombie Spawn

rooms = [
    [[w, w, w, w, w, w, w, w, w, w, w, w, w, w, w],
     [w, z, g, g, g, g, g, g, g, g, g, g, g, z, w],
     [w, g, g, g, g, g, g, g, g, g, g, g, g, g, w],
     [w, g, g, g, g, g, g, g, g, g, g, g, g, g, w],
     [w, g, g, g, g, g, g, p, g, g, g, g, g, g, w],
     [w, g, g, g, g, g, g, g, g, g, g, g, g, g, w],
     [w, g, g, g, g, g, g, g, g, g, g, g, g, g, w],
     [w, z, g, g, g, g, g, g, g, g, g, g, g, z, w],
     [w, w, w, w, w, w, w, w, w, w, w, w, w, w, w]]
]


class Room:

    def __init__(self, x, y, previous_door, room_number):
        self.x = x
        self.y = y
        self.previous_door = previous_door
        self.room_number = room_number
        self.status = 0  # 0 - Created, 1 - Visited, 2 - Cleared
