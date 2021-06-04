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

# Zombies and Doors are not needed! Will be added later
w = "w"  # Wall
g = "g"  # Ground
p = "p"  # Player Spawn

# All available rooms - this can be extended by appending a new room [OPEN]
rooms = [[[w, w, w, w, w, w, w, w, w, w, w, w, w, w, w],  # Room 0
          [w, g, g, g, g, g, g, g, g, g, g, g, g, g, w],
          [w, g, g, g, g, g, g, g, g, g, g, g, g, g, w],
          [w, g, g, g, g, g, g, g, g, g, g, g, g, g, w],
          [w, g, g, g, g, g, g, p, g, g, g, g, g, g, w],
          [w, g, g, g, g, g, g, g, g, g, g, g, g, g, w],
          [w, g, g, g, g, g, g, g, g, g, g, g, g, g, w],
          [w, g, g, g, g, g, g, g, g, g, g, g, g, g, w],
          [w, w, w, w, w, w, w, w, w, w, w, w, w, w, w]],
         [[w, w, w, w, w, w, w, w, w, w, w, w, w, w, w],  # Room 1
          [w, g, g, g, g, g, g, g, g, g, g, g, g, g, w],
          [w, g, g, g, g, g, g, g, g, g, g, g, g, g, w],
          [w, g, g, g, g, g, g, g, g, g, g, g, g, g, w],
          [w, g, g, g, g, g, g, g, g, g, g, g, g, g, w],
          [w, g, g, g, g, g, g, g, g, g, g, g, g, g, w],
          [w, g, g, g, g, g, g, g, g, g, g, g, g, g, w],
          [w, g, g, g, g, g, g, g, g, g, g, g, g, g, w],
          [w, w, w, w, w, w, w, w, w, w, w, w, w, w, w]]
         ]


class Room:
    """ Room

        the class room holds information about each individual room, like:
            - Position on grid
            - Their design (obstacles in room)
            - Door-Position

        attributes:
            x(int): x-coordinate of position on grid
            y(int): y-coordinate of position on grid
            doors(array of str): contains the information of door-positions
            previous_room(str): direction of previous room
            room_number(int): index of 'rooms-array' (above)
            status(int): status of the room [0 - Created; 1 - Visited; 2 - Visiting but cleared; 3 - Cleared]

        test:
            * room_number matches the right element in array
            * doors contains the right information
    """

    def __init__(self, x, y, previous_room, room_number):
        self.x = x
        self.y = y
        self.doors = []
        self.previous_room = previous_room
        self.room_number = room_number
        self.status = 0
