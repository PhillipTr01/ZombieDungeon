""" Python Top Down Shooter - ZombieDungeon
    *
    *

    param:
        Author: Stefan Nemanja Banov & Phillip Tran
        Date: 06.06.2021
        Version: 1.0.0
        License: free

    Sources:
        [1] Fireball (Sprites):
            Link: https://www.pngitem.com/pimgs/m/64-641943_8-bit-cherry-png-download-mario-fireball-8.png
"""

import pygame

from config import *


class Fireball(pygame.sprite.Sprite):
    """ Fireball

            the fireball is a weapon used by the player to damage / kill zombies

        attributes:
            dir(str): the direction in which the fireball flies
            rect(rect): rectangle of fireball
            rect.x(int): coordinates of fireball in x-axis
            rect.y(int): coordinates of fireball in y-axis
            speed(int): the speed at which the fireball flies (Pixels per second)
            spawn_time(int): time in milliseconds
            game(game): current game running

        test:
            * fireball shows right sprites
            * fireball flies in right direction and speed
            * collisions work
    """

    def __init__(self, game, x, y, dir):
        pygame.sprite.Sprite.__init__(self, game.weapon_sprites)
        if dir == 'left':
            self.image = pygame.transform.scale(pygame.image.load("images/player/weapons/fireball_left.png"),   # [1]
                                                (config['weapon_size'], config['weapon_size']))
        elif dir == 'right':
            self.image = pygame.transform.scale(pygame.image.load("images/player/weapons/fireball_right.png"),  # [1]
                                                (config['weapon_size'], config['weapon_size']))
        elif dir == 'up':
            self.image = pygame.transform.scale(pygame.image.load("images/player/weapons/fireball_up.png"),     # [1]
                                                (config['weapon_size'], config['weapon_size']))
        elif dir == 'down':
            self.image = pygame.transform.scale(pygame.image.load("images/player/weapons/fireball_down.png"),   # [1]
                                                (config['weapon_size'], config['weapon_size']))

        # [SOUND]: fireball shoot sound can be added here

        self.dir = dir
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = config['weapon_speed']
        self.spawn_time = pygame.time.get_ticks()
        self.game = game

    def update(self):
        """
        update

            this method updates the position of the fireball and eventually kills the instance.

            param:
                none

            return:
                none

            test:
                * Fireball is shooting and moving in the right direction
                * Fireball is killed after lifetime or on collision
        """

        # Based on the direction move the Fireball in x or y axis
        if self.dir == 'left':
            self.rect.x -= self.speed
        elif self.dir == 'right':
            self.rect.x += self.speed
        elif self.dir == 'up':
            self.rect.y -= self.speed
        elif self.dir == 'down':
            self.rect.y += self.speed

        # Check if Fireball collided with a wall or if Fireball no longer exists (lifetime)
        if pygame.sprite.spritecollideany(self, self.game.collision_sprites) \
                or pygame.time.get_ticks() - self.spawn_time > config['weapon_lifetime']:
            self.kill()
