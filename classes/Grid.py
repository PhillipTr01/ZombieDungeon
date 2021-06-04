""" Python Top Down Shooter - ZombieDungeon
    *
    *

    param:
        Author: Stefan Nemanja Banov & Phillip Tran
        Date: 06.06.2021
        Version: 1.0.0
        License: free

    Sources:
        [1] Fill a two dimensional Array:
            Link: https://www.snakify.org/de/lessons/two_dimensional_lists_arrays/
"""

import random

from config import *
from classes.Room import *


class Grid:
    """ Grid

        This class portrays the Grid of the Map
            - The main-function of this class is to arrange all rooms properly
            - Each level contains one random generated grid
            - The Rooms created are distributed on this grid

        attributes:
            grid(2d-array of rooms): represents the map. contains
            size_x(int): size of grid in x-axis
            size_y(int): size of grid in y-axis
            start_x(int): x-coordinate of start_room
            start_y(int): y-coordinate of start_room
            base_rooms_per_level(int): minimum number of rooms per level
            room_count(int): number of valid rooms on grid

        test:
            * grid size properly set
            * grid created with valid (information correct) rooms only (empty rooms doesn't count)
    """

    def __init__(self, size_x, size_y):
        self.grid = []
        self.size_x = size_x
        self.size_y = size_y
        self.start_x = 0
        self.start_y = 0
        self.base_rooms_per_level = config['base_rooms_per_level']
        self.room_count = -1

    # ------------ Grid Manipulation ------------ #

    def fill_grid(self, level):
        """ fill_grid

            fills the grid with random rooms, so that a dungeon-like grid is created (all side by side)
                1. Create Startroom
                2. Loop: Create random rooms next to the previous room
                    2.1 All possible empty fields on the grid are added to the possible_ways array
                    2.2 A random element of the array is chosen to be the next room
                    Example:
                        c = current room
                        x = field with room
                        o = empty field

                        x x o o o
                        x x o o o
                        o x x c o
                        o o o o o
                        o o o o o

                        - possible_ways array is filled with ['right', 'up', 'down']

                        if element 2 has been chosen, then the grid will look like this:
                        x x o o o
                        x x o c o
                        o x x x o
                        o o o o o
                        o o o o o
                3. The previous door (direction) is saved for later


            param:
                level(int): current level of game

            return:
                none

            test:
                * grid is valid (rooms count have the limit, rooms can only spawn side by side...)
                * previous door is saved correctly
        """

        # Set start coordinates to the middle of the grid
        self.start_x = round((self.size_x - 1) / 2)
        self.start_y = round((self.size_y - 1) / 2)

        # initialize grid with empty rooms
        self.grid = [[Room(-1, -1, 'e', -1)] * self.size_y for _ in range(self.size_x)]     # [1]
        self.grid[self.start_y][self.start_x] = Room(self.start_x, self.start_y, 's', 0)
        self.grid[self.start_y][self.start_x].status = 1

        count = 0

        y = self.start_y
        x = self.start_x
        previous_room = ''

        while count < self.base_rooms_per_level + random.randint(-1 + round(level / 2), level):
            possible_ways = []

            # Find all possible ways that are not already occupied or out of bounds
            if y + 1 in range(0, self.size_y) and self.grid[y + 1][x].previous_room == 'e':
                possible_ways.append('down')
            if y - 1 in range(0, self.size_y) and self.grid[y - 1][x].previous_room == 'e':
                possible_ways.append('up')
            if x + 1 in range(0, self.size_x) and self.grid[y][x + 1].previous_room == 'e':
                possible_ways.append('right')
            if x - 1 in range(0, self.size_x) and self.grid[y][x - 1].previous_room == 'e':
                possible_ways.append('left')

            # If there are no possible ways, the generator is in a deadlock situation
            if len(possible_ways) == 0:
                break

            # Chose a random way and move the coordinates to that position
            chosen_way = possible_ways[random.randint(0, len(possible_ways) - 1)]

            if chosen_way == 'up':
                previous_room = 'd'
                y -= 1
            elif chosen_way == 'down':
                previous_room = 'u'
                y += 1
            elif chosen_way == 'left':
                previous_room = 'r'
                x -= 1
            elif chosen_way == 'right':
                previous_room = 'l'
                x += 1

            # Create rooms with given information
            self.grid[y][x] = Room(x, y, previous_room, random.randint(1, len(rooms) - 1))

            count += 1

        self.fill_rooms_with_doors(self.grid[y][x])

    def fill_rooms_with_doors(self, last_room):
        """ fill_rooms_with_doors

            adds all doors needed to the rooms
                1. Get all information from the last room that has been created on the grid
                2. Loop: Check all rooms next to the room (up, down, left, right).
                   If those rooms exists add a door for it.
                3. Now the previous door variable is needed -
                   With this variable you can go back to the beginning room by room

            param:
                last_room(room): last created room on the grid

            return:
                none

            test:
                * last room is indeed the last room on the grid
                * all doors have been filled right and on each room on the grid
        """

        # Get information of the latest created room
        x = last_room.x
        y = last_room.y
        previous_room = last_room.previous_room

        self.room_count = 0

        # Move backwards from the last room to the start room
        # Add a door for each neighbour of the room
        while self.grid[y][x].previous_room != 'e':
            doors = []

            if y + 1 in range(0, self.size_y) and self.grid[y + 1][x].previous_room != 'e':
                doors.append('down')

            if y - 1 in range(0, self.size_y) and self.grid[y - 1][x].previous_room != 'e':
                doors.append('up')

            if x + 1 in range(0, self.size_x) and self.grid[y][x + 1].previous_room != 'e':
                doors.append('right')

            if x - 1 in range(0, self.size_x) and self.grid[y][x - 1].previous_room != 'e':
                doors.append('left')

            self.grid[y][x].doors = doors

            # Move to the next room based on the previous_room
            if previous_room == 'u':
                y -= 1
            elif previous_room == 'd':
                y += 1
            elif previous_room == 'l':
                x -= 1
            elif previous_room == 'r':
                x += 1
            elif previous_room == 's':
                break

            self.room_count += 1

            previous_room = self.grid[y][x].previous_room
