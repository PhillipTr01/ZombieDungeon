""" Python Top Down Shooter - ZombieDungeon
    *
    * This class portrays the Zombie

    param:
        Author: Stefan Nemanja Banov & Phillip Tran
        Date: 06.06.2021
        Version: 1.0.0
        License: free

"""

import pygame

from config import *


class Zombie(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        self.sprites = []
        self.initialize_sprites()
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        pygame.sprite.Sprite.__init__(self, game.enemy_sprites)
        self.rect = self.image.get_rect()
        self.x = x * config["tile_size"]
        self.y = y * config["tile_size"]
        self.game = game
        self.mx = 0
        self.my = 0
        self.animation_time = 0

    def update(self):
        """
        update

            -

            param:
                none

            return:
                none

            test:
                * -
        """
        self.ai_movement()
        self.x += self.mx * self.game.dt
        self.y += self.my * self.game.dt
        self.rect.topleft = (self.x, self.y)

    # ------------ Sprites ------------ #

    def initialize_sprites(self):
        """
        initialize_sprites

            -

            param:
                none

            return:
                none

            test:
                * -
        """
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/tile000.png"),
                                                   (config['zombie_size'], config['zombie_size'])))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/tile001.png"),
                                                   (config['zombie_size'], config['zombie_size'])))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/tile002.png"),
                                                   (config['zombie_size'], config['zombie_size'])))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/tile003.png"),
                                                   (config['zombie_size'], config['zombie_size'])))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/tile004.png"),
                                                   (config['zombie_size'], config['zombie_size'])))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/tile005.png"),
                                                   (config['zombie_size'], config['zombie_size'])))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/tile006.png"),
                                                   (config['zombie_size'], config['zombie_size'])))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/tile007.png"),
                                                   (config['zombie_size'], config['zombie_size'])))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/tile008.png"),
                                                   (config['zombie_size'], config['zombie_size'])))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/tile009.png"),
                                                   (config['zombie_size'], config['zombie_size'])))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/tile010.png"),
                                                   (config['zombie_size'], config['zombie_size'])))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/tile011.png"),
                                                   (config['zombie_size'], config['zombie_size'])))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/tile012.png"),
                                                   (config['zombie_size'], config['zombie_size'])))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/tile013.png"),
                                                   (config['zombie_size'], config['zombie_size'])))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/tile014.png"),
                                                   (config['zombie_size'], config['zombie_size'])))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/tile015.png"),
                                                   (config['zombie_size'], config['zombie_size'])))

    def sprite_update(self, direction):
        """
        sprite_update

            -

            param:
                direction(str): -

            return:
                none

            test:
                * -
        """
        if self.animation_time == config['animation_speed']:
            if direction == "down":
                if self.current_sprite >= 3:
                    self.current_sprite = 0
                else:
                    self.current_sprite += 1

            if direction == "left":
                if 4 <= self.current_sprite < 7:
                    self.current_sprite += 1
                else:
                    self.current_sprite = 4

            if direction == "right":
                if 8 <= self.current_sprite < 11:
                    self.current_sprite += 1
                else:
                    self.current_sprite = 8

            if direction == "up":
                if 12 <= self.current_sprite < 15:
                    self.current_sprite += 1
                else:
                    self.current_sprite = 12

            if direction == "idle":
                self.current_sprite = 0
                # if 0 < self.current_sprite <= 3:
                # self.current_sprite = 0
                # if 4 <= self.current_sprite <= 7:
                # self.current_sprite = 4
                # if 8 <= self.current_sprite <= 11:
                # self.current_sprite = 8
                # if 12 <= self.current_sprite <= 15:
                # self.current_sprite = 12

            self.image = self.sprites[self.current_sprite]
            self.animation_time = 0
        else:
            self.animation_time += 1

    # ------------ Movement ------------ #

    def ai_movement(self):
        """
        ai_movement

            -

            param:
                none

            return:
                none

            test:
                * -
        """
        self.mx = 0
        self.my = 0

        # Checking Difference to Players-X Position
        subx = self.x - self.game.player.x
        if subx < 0:
            self.mx = config['zombie_speed']
        else:
            self.mx = -config['zombie_speed']

        # Checking Difference to Players-Y Position
        suby = self.y - self.game.player.y
        if suby < 0:
            self.my = config['zombie_speed']
        else:
            self.my = -config['zombie_speed']

        if self.mx != 0 and self.my != 0:
            self.mx *= 0.7071
            self.my *= 0.7071

        # Muss noch angepasst werden, so dass der Zombie in alle Richtungen läuft
        self.sprite_update("left")
