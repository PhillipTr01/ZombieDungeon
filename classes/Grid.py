""" Python Top Down Shooter - ZombieDungeon
    *
    * This class portrays the Grid
        - Each level contains one random generated grid
        - The Rooms created are distributed on the grid

    param:
        Author: Stefan Nemanja Banov & Phillip Tran
        Date: 06.06.2021
        Version: 1.0.0
        License: free

    Sources:
        Fill a two dimensional Array:
            Link: https://www.snakify.org/de/lessons/two_dimensional_lists_arrays/
"""

import random

from config import *
from classes.Room import *


class Grid:

    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        self.start_x = 0
        self.start_y = 0
        self.grid = []
        self.base_rooms_per_level = config['base_rooms_per_level']
        self.room_count = 1

    # ------------ Grid Manipulation ------------ #

    def fill_grid(self, level):
        """
        fill_grid

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
        self.start_x = round((self.size_x - 1) / 2)
        self.start_y = round((self.size_y - 1) / 2)
        self.grid = [[Room(-1, -1, 'e', -1)] * self.size_y for _ in range(self.size_x)]
        self.grid[self.start_y][self.start_x] = Room(self.start_x, self.start_y, 's', 0)
        self.grid[self.start_y][self.start_x].status = 1

        room_count = 0

        y = self.start_y
        x = self.start_x
        previous_door = ''

        while room_count < self.base_rooms_per_level + random.randint(-1, level):
            possible_ways = []

            if y + 1 in range(0, self.size_y) and self.grid[y + 1][x].previous_door == 'e':
                possible_ways.append('down')
            if y - 1 in range(0, self.size_y) and self.grid[y - 1][x].previous_door == 'e':
                possible_ways.append('up')
            if x + 1 in range(0, self.size_x) and self.grid[y][x + 1].previous_door == 'e':
                possible_ways.append('right')
            if x - 1 in range(0, self.size_x) and self.grid[y][x - 1].previous_door == 'e':
                possible_ways.append('left')

            if len(possible_ways) == 0:
                break

            chosen_room = random.randint(0, len(possible_ways) - 1)

            if possible_ways[chosen_room] == 'up':
                previous_door = 'd'
                y -= 1
            elif possible_ways[chosen_room] == 'down':
                previous_door = 'u'
                y += 1
            elif possible_ways[chosen_room] == 'left':
                previous_door = 'r'
                x -= 1
            elif possible_ways[chosen_room] == 'right':
                previous_door = 'l'
                x += 1

            self.grid[y][x] = Room(x, y, previous_door, random.randint(1, len(rooms) - 1))

            room_count += 1

        self.fill_rooms_with_doors(self.grid[y][x])

    def fill_rooms_with_doors(self, last_room):
        """
        fill_rooms_with_doors

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
        x = last_room.x
        y = last_room.y
        previous_door = last_room.previous_door

        self.room_count = 0

        while self.grid[y][x].previous_door != 'e':
            doors = []

            if y + 1 in range(0, self.size_y) and self.grid[y + 1][x].previous_door != 'e':
                doors.append('down')

            if y - 1 in range(0, self.size_y) and self.grid[y - 1][x].previous_door != 'e':
                doors.append('up')

            if x + 1 in range(0, self.size_x) and self.grid[y][x + 1].previous_door != 'e':
                doors.append('right')

            if x - 1 in range(0, self.size_x) and self.grid[y][x - 1].previous_door != 'e':
                doors.append('left')

            self.grid[y][x].doors = doors

            if previous_door == 'u':
                y -= 1
            elif previous_door == 'd':
                y += 1
            elif previous_door == 'l':
                x -= 1
            elif previous_door == 'r':
                x += 1
            elif previous_door == 's':
                break

            self.room_count += 1

            previous_door = self.grid[y][x].previous_door
