""" Python Top Down Shooter - ZombieDungeon
    *
    * This class is the main class. It contains the main-loop of the program

    param:
        Author: Stefan Nemanja Banov & Phillip Tran
        Date: 06.06.2021
        Version: 1.0.0
        License: free

    Sources:
        Sprites:
            The Sprites of this game have been designed and drawn by Nina Vukovic and Stefan Nemanja Banov
"""

from classes.Game import *

import classes.Room as rooms


if __name__ == "__main__":
    active_game = Game()
    active_game.room_decoding(rooms.rooms[0])

    while True:
        active_game.general_key_events()

        if active_game.gamestate == 0:  # Program running
            active_game.start_screen()
        elif active_game.gamestate == 1:  # Game started
            active_game.update()
            active_game.draw()
            active_game.player.movement()
        elif active_game.gamestate == 2:  # Game paused
            active_game.draw()
        elif active_game.gamestate == 3:  # Game lost
            pass
