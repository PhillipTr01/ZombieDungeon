""" Python Top Down Shooter - ZombieDungeon
    *
    *

    param:
        Author: Stefan Nemanja Banov & Phillip Tran
        Date: 06.06.2021
        Version: 1.0.0
        License: free

    Sources:
        Health Container:
            Tutorial-Link: https://www.youtube.com/watch?v=WLYEsgYkEvY

"""

import pygame

from config import *


class Player(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        self.sprites = []
        self.initialize_sprites()
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        pygame.sprite.Sprite.__init__(self, game.character_sprites)
        self.rect = self.image.get_rect()
        self.max_health = config['max_health_player']
        self.health = config['max_health_player']
        self.game = game
        self.x = x * config["tile_size"] - config["tile_size"] / 2
        self.y = y * config["tile_size"] - config["tile_size"] / 2
        self.mx = 0
        self.my = 0
        self.animation_time = 0

    def update(self):
        self.x += self.mx * self.game.dt
        self.y += self.my * self.game.dt
        self.rect.topleft = (self.x, self.y)

        if pygame.sprite.spritecollideany(self, self.game.collision_sprites):
            self.x -= self.mx * self.game.dt
            self.y -= self.my * self.game.dt
            self.rect.topleft = (self.x, self.y)

    # ------------ Sprites ------------ #

    def initialize_sprites(self):
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/sprites/tile000.png"),
                                                   (config['player_size'], config['player_size'])))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/sprites/tile001.png"),
                                                   (config['player_size'], config['player_size'])))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/sprites/tile002.png"),
                                                   (config['player_size'], config['player_size'])))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/sprites/tile003.png"),
                                                   (config['player_size'], config['player_size'])))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/sprites/tile004.png"),
                                                   (config['player_size'], config['player_size'])))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/sprites/tile005.png"),
                                                   (config['player_size'], config['player_size'])))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/sprites/tile006.png"),
                                                   (config['player_size'], config['player_size'])))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/sprites/tile007.png"),
                                                   (config['player_size'], config['player_size'])))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/sprites/tile008.png"),
                                                   (config['player_size'], config['player_size'])))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/sprites/tile009.png"),
                                                   (config['player_size'], config['player_size'])))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/sprites/tile010.png"),
                                                   (config['player_size'], config['player_size'])))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/sprites/tile011.png"),
                                                   (config['player_size'], config['player_size'])))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/sprites/tile012.png"),
                                                   (config['player_size'], config['player_size'])))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/sprites/tile013.png"),
                                                   (config['player_size'], config['player_size'])))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/sprites/tile014.png"),
                                                   (config['player_size'], config['player_size'])))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/sprites/tile015.png"),
                                                   (config['player_size'], config['player_size'])))

    def sprite_update(self, direction):
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
                #     self.current_sprite = 0
                # if 4 <= self.current_sprite <= 7:
                #     self.current_sprite = 4
                # if 8 <= self.current_sprite <= 11:
                #     self.current_sprite = 8
                # if 12 <= self.current_sprite <= 15:
                #     self.current_sprite = 12

            self.image = self.sprites[self.current_sprite]
            self.animation_time = 0
        else:
            self.animation_time += 1

    # --------------------------------- #

    # ----------- Movement ----------- #

    def movement(self):
        self.mx = 0
        self.my = 0
        direction = "idle"
        key = pygame.key.get_pressed()
        if key[pygame.K_a] and not key[pygame.K_d]:
            self.mx = -config['player_speed']
            direction = "left"

        if key[pygame.K_d] and not key[pygame.K_a]:
            self.mx = config['player_speed']
            direction = "right"

        if key[pygame.K_w] and not key[pygame.K_s]:
            self.my = -config['player_speed']
            direction = "up"

        if key[pygame.K_s] and not key[pygame.K_w]:
            self.my = config['player_speed']
            direction = "down"

        # Satz des Pythagoras sein Vater:
        if self.mx != 0 and self.my != 0:
            self.mx *= 0.7071
            self.my *= 0.7071

        self.sprite_update(direction)

    # -------------------------------- #

    # ------------ Health ------------ #

    def get_damage(self, damage):
        if self.health > 0:
            self.health -= damage

    def get_health(self, health):
        if self.health < self.max_health:
            self.health += health

    # -------------------------------- #
