""" Python Top Down Shooter - ZombieDungeon
    *
    * This class portrays the Weapon

    param:
        Author: Stefan Nemanja Banov & Phillip Tran
        Date: 06.06.2021
        Version: 1.0.0
        License: free

"""

import pygame

from config import *


class Fireball(pygame.sprite.Sprite):

    def __init__(self, game, x, y, dir):
        self.dir = dir
        pygame.sprite.Sprite.__init__(self, game.weapon_sprites)
        if dir == 'left':
            self.image = pygame.transform.scale(pygame.image.load("images/player/weapons/fireball_left.png"),
                                                (config['weapon_size'], config['weapon_size']))
        elif dir == 'right':
            self.image = pygame.transform.scale(pygame.image.load("images/player/weapons/fireball_right.png"),
                                                (config['weapon_size'], config['weapon_size']))
        elif dir == 'up':
            self.image = pygame.transform.scale(pygame.image.load("images/player/weapons/fireball_up.png"),
                                                (config['weapon_size'], config['weapon_size']))
        elif dir == 'down':
            self.image = pygame.transform.scale(pygame.image.load("images/player/weapons/fireball_down.png"),
                                                (config['weapon_size'], config['weapon_size']))

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.speed = config['weapon_speed']
        self.spawn_time = pygame.time.get_ticks()
        self.game = game

    def update(self):

        if self.dir == 'left':
            self.rect.x -= self.speed
        elif self.dir == 'right':
            self.rect.x += self.speed
        elif self.dir == 'up':
            self.rect.y -= self.speed
        elif self.dir == 'down':
            self.rect.y += self.speed

        if pygame.sprite.spritecollideany(self, self.game.collision_sprites):
            self.kill()

        if pygame.time.get_ticks() - self.spawn_time > config['weapon_lifetime']:
            self.kill()
