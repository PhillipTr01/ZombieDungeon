""" Python Top Down Shooter - ZombieDungeon
    *
    *

    param:
        Author: Stefan Nemanja Banov & Phillip Tran
        Date: 06.06.2021
        Version: 1.0.0
        License: free

    Sources:
        [1] Sprites:
                Designer: Nina Vukovic (Friend of developer) and Stefan Nemanja Banov
"""

import pygame
import logging

from config import *


class Ground(pygame.sprite.Sprite):
    """ Ground

        embodies a passable structure object.

        attributes:
            image(surface): sprite of ground
            rect(rect): rectangle of ground
            rect.x(int): coordinates of ground in x-axis
            rect.y(int): coordinates of ground in y-axis

        test:
            * right sprite is displayed
            * position is correct
    """
    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self, game.background_sprites)
        try:
            self.image = pygame.transform.scale(pygame.image.load("images/objects/ground.png"),     # [1]
                                            (config['tile_size'], config['tile_size']))
        except FileNotFoundError:
            logging.critical("The ground sprite could not be found.")
        self.rect = self.image.get_rect()
        self.rect.x = x * config['tile_size']
        self.rect.y = y * config['tile_size']


class Wall(pygame.sprite.Sprite):
    """ Wall

        embodies an obstacle. Moving objects like the enemies and players can't pass this object

        attributes:
            image(surface): sprite of wall
            rect(rect): rectangle of wall
            rect.x(int): coordinates of wall in x-axis
            rect.y(int): coordinates of wall in y-axis

        test:
            * right sprite is displayed
            * position is correct
    """
    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self, game.collision_sprites)
        try:
            self.image = pygame.transform.scale(pygame.image.load("images/objects/wall.png"),       # [1]
                                            (config['tile_size'], config['tile_size']))
        except FileNotFoundError:
            logging.critical("The wall sprite could not be found.")
        self.rect = self.image.get_rect()
        self.rect.x = x * config['tile_size']
        self.rect.y = y * config['tile_size']


class Door(pygame.sprite.Sprite):
    """ Door

        embodies the doors of the room. This object spawns when all zombies of the room have been killed.

        attributes:
            image(surface): sprite of door
            rect(rect): rectangle of door
            rect.x(int): coordinates of door in x-axis
            rect.y(int): coordinates of door in y-axis

        test:
            * right sprite is displayed
            * position is correct
    """
    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self, game.door_sprites)
        self.image = pygame.transform.scale(pygame.image.load("images/objects/ground.png"),     # [1]
                                            (config['tile_size'], config['tile_size']))
        self.rect = self.image.get_rect()
        self.rect.x = x * config['tile_size']
        self.rect.y = y * config['tile_size']
