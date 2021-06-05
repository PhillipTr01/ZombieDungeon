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
        Sound:
            - [OPEN]
"""

from classes.Game import *

if __name__ == "__main__":

    # Create an instance of the Game class
    active_game = Game()

    while True:

        active_game.general_key_events()

        if active_game.gamestate == 0:  # Program is running (start screen)
            active_game.start_screen()
        elif active_game.gamestate == 1:  # Game has been started
            active_game.update()
        elif active_game.gamestate == 2:  # Game has been paused
            active_game.draw()
        elif active_game.gamestate == 3:  # Game over - Give the user opportunity to restart the game
            active_game.game_over_screen()
            # Restart game - without going back to the start screen
            if pygame.key.get_pressed()[pygame.K_r]:  # Sollte gegen Try again Button ausgetauscht werden [OPEN]
                del active_game
                active_game = Game()
                active_game.gamestate = 1
