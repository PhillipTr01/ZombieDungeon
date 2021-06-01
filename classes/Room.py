""" Python Top Down Shooter - ZombieDungeon
    *
    *

    param:
        Author: Stefan Nemanja Banov & Phillip Tran
        Date: 06.06.2021
        Version: 1.0.0
        License: free

"""

from classes.Objects import *
from classes.Player import *

w = "w"  # Wall
g = "g"  # Ground
d = "d"  # Door
p = "p"  # Player Spawn

rooms = [
    [[w, w, w, w, w, w, w, w, w, w, w, w, w, w, w],
     [w, g, g, g, g, g, g, g, g, g, g, g, g, g, w],
     [w, g, g, g, g, g, g, g, g, g, g, g, g, g, w],
     [w, g, g, g, g, g, g, g, w, g, g, g, g, g, w],
     [w, g, g, g, g, g, g, p, g, w, g, g, g, g, w],
     [w, g, g, g, g, g, g, g, g, g, w, g, g, g, w],
     [w, g, g, g, g, g, g, g, g, g, g, w, g, g, w],
     [w, g, g, g, g, g, g, g, g, g, g, w, g, g, w],
     [w, w, w, w, w, w, w, w, w, w, w, w, w, w, w]]
]


class Room:

    def __init__(self, x, y, previous_door):
        self.x = x
        self.y = y
        self.previous_door = previous_door
        self.status = 0  # 0 - Created, 1 - Visited, 2 - Cleared