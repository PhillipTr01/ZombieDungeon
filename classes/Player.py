""" Python Top Down Shooter - ZombieDungeon
    *
    * This class portrays the Player

    param:
        Author: Stefan Nemanja Banov & Phillip Tran
        Date: 06.06.2021
        Version: 1.0.0
        License: free

    Sources:
        [1] Player (Sprites):
                Designer: Nina Vukovic (Friend of developer) and Stefan Nemanja Banov
        [2] Health Container:
            Tutorial-Link: https://www.youtube.com/watch?v=WLYEsgYkEvY

"""
import pygame.mixer

from classes.Weapons import *


class Player(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        self.sprites = []
        self.initialize_sprites()
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        pygame.sprite.Sprite.__init__(self, game.character_sprites)
        self.rect = self.image.get_rect()
        self.x = x * config["tile_size"]
        self.y = y * config["tile_size"]
        self.game = game
        self.mx = 0
        self.my = 0
        self.animation_time = 0

        self.invincible_count = 0
        self.shoot_delay = 0
        self.door_count = 0
        self.health = config['player_health']

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
        if self.health == 0:
            self.game.gamestate = 3

        self.x += self.mx * self.game.dt
        self.y += self.my * self.game.dt
        self.rect.topleft = (self.x, self.y)

        if pygame.sprite.spritecollideany(self, self.game.collision_sprites):
            self.x -= self.mx * self.game.dt
            self.y -= self.my * self.game.dt
            self.rect.topleft = (self.x, self.y)

        if pygame.sprite.groupcollide(self.game.enemy_sprites, self.game.character_sprites, False, False):
            if self.invincible_count == 0:
                self.get_damage(config['zombie_damage'])
                self.invincible_count = 50
            self.x -= self.mx * self.game.dt
            self.y -= self.my * self.game.dt
            self.rect.topleft = (self.x, self.y)

        if pygame.sprite.spritecollideany(self, self.game.door_sprites):
            self.game.next_room(pygame.sprite.spritecollideany(self, self.game.door_sprites))

        if self.invincible_count > 0:
            self.invincible_count -= 1

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
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/player/tile000.png"),
                                                   (config['player_size'], config['player_size'])))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/player/tile001.png"),
                                                   (config['player_size'], config['player_size'])))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/player/tile002.png"),
                                                   (config['player_size'], config['player_size'])))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/player/tile003.png"),
                                                   (config['player_size'], config['player_size'])))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/player/tile004.png"),
                                                   (config['player_size'], config['player_size'])))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/player/tile005.png"),
                                                   (config['player_size'], config['player_size'])))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/player/tile006.png"),
                                                   (config['player_size'], config['player_size'])))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/player/tile007.png"),
                                                   (config['player_size'], config['player_size'])))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/player/tile008.png"),
                                                   (config['player_size'], config['player_size'])))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/player/tile009.png"),
                                                   (config['player_size'], config['player_size'])))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/player/tile010.png"),
                                                   (config['player_size'], config['player_size'])))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/player/tile011.png"),
                                                   (config['player_size'], config['player_size'])))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/player/tile012.png"),
                                                   (config['player_size'], config['player_size'])))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/player/tile013.png"),
                                                   (config['player_size'], config['player_size'])))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/player/tile014.png"),
                                                   (config['player_size'], config['player_size'])))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/player/tile015.png"),
                                                   (config['player_size'], config['player_size'])))

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

    # ------------ Movement ------------ #

    def movement(self):
        """
        movement

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

        if key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
            if self.shoot_delay == 0:
                self.shoot_delay = 0
                self.game.shoot(self.x, self.y, 'left')
            direction = "left"
        elif key[pygame.K_RIGHT] and not key[pygame.K_LEFT]:
            if self.shoot_delay == 0:
                self.shoot_delay = 0
                self.game.shoot(self.x, self.y, 'right')
            direction = "right"
        elif key[pygame.K_UP] and not key[pygame.K_DOWN]:
            if self.shoot_delay == 0:
                self.shoot_delay = 0
                self.game.shoot(self.x, self.y, 'up')
            direction = "up"
        elif key[pygame.K_DOWN] and not key[pygame.K_UP]:
            if self.shoot_delay == 0:
                self.shoot_delay = 0
                self.game.shoot(self.x, self.y, 'down')
            direction = "down"

        if self.mx != 0 and self.my != 0:
            self.mx *= 0.7071
            self.my *= 0.7071

        if self.shoot_delay > 0:
            self.shoot_delay -= 1

        self.sprite_update(direction)

    # ------------ Health ------------ #

    def get_damage(self, damage):
        """
        get_damage

            -

            param:
                damage(int):

            return:
                none

            test:
                * -
        """
        if self.health > 0:
            self.health -= damage
