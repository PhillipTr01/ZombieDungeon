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

from config import *


class Zombie(pygame.sprite.Sprite):
    """ Zombie

        this class portrays the zombie, the enemy of the player

        attributes:
            sprites(list of surface): contains all images / sprites of zombie
            current_sprite(int): declares which sprite should be displayed
            image(surface): current sprite
            rect(rect): rectangle of zombie
            x(int): x-coordinate of position
            y(int): y-coordinate of position
            game(game): current game running
            mx(float): movement indicator on x-axis
            my(float): movement indicator on y-axis
            animation_time(int): interval a new sprite is chosen
            health(int): health of zombie
            invincible_count(int): interval the zombie can get damage

        test:
            * Zombie spawns on correct position (doesn't collide on spawn)
            * Movement is automated and zombie is moving towards player
    """

    def __init__(self, game, x, y):
        self.sprites = []
        self.initialize_sprites()
        self.current_sprite = 0
        pygame.sprite.Sprite.__init__(self, game.enemy_sprites)
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.x = x * config["tile_size"]
        self.y = y * config["tile_size"]
        self.game = game
        self.mx = 0
        self.my = 0
        self.animation_time = 0

        self.health = config['zombie_health']
        self.invincible_count = 0

    def update(self):
        """ update
            this method updates the position of the zombie and handles collisions
            param:
                none
            return:
                none
            test:
                * is moving in the right direction
                * collision is detected and further action is taken
        """
        self.ai_movement()

        # [SOUND]: Zombie base sound can be added here

        # Change position
        self.x += self.mx * self.game.dt
        self.y += self.my * self.game.dt
        self.rect.x = self.x
        self.collide_check("x", self.game.collision_sprites)
        self.rect.y = self.y
        self.collide_check("y", self.game.collision_sprites)


        # Collide with weapon / fireball
        if pygame.sprite.spritecollideany(self, self.game.weapon_sprites):
            sprite = pygame.sprite.spritecollideany(self, self.game.weapon_sprites)
            sprite.kill()

            # if zombie is not "invincible" he gets damage
            if self.invincible_count == 0:
                # Zombie gets damage
                # [SOUND]: Zombie hurt sound can be added here
                self.health -= config['weapon_damage']
                self.invincible_count = config['zombie_invincible_time']

                # zombie gets killed, player gains 100 points
                if self.health == 0:
                    # [SOUND]: Zombie death sound can be added here
                    self.game.zombie_count -= 1
                    self.game.score += 100
                    self.kill()

                # Detect if all zombies have been killed
                if self.game.zombie_count == 0:
                    self.game.room_cleared()

        # Collide with Player
        if pygame.sprite.spritecollideany(self, self.game.character_sprites):
            # Reset position so that zombie doesn't pass or goes through player
            self.x -= self.mx * self.game.dt
            self.y -= self.my * self.game.dt
            self.rect.topleft = (self.x, self.y)

            # if player is not "invincible" he gets damage
            if self.game.player.invincible_count == 0:
                # [SOUND]: Player hurt sound can be added here
                self.game.player.health -= config['zombie_damage']
                self.game.player.invincible_count = 50

        # TODO: Zombies should no longer be able to move inside themself

        # print(len(self.game.enemy_sprites))
        # for sprite in self.game.enemy_sprites:
        #     print(pygame.sprite.collide_rect(self, sprite), end=",")
        # print()

        if self.invincible_count > 0:
            self.invincible_count -= 1

        # [OPEN] to add:
        #   - Collision with other Enemies
        #   - Collision with Walls
        #   - "Knockback" on Weapon- / Fireballcollision
        #   - Better collision with player

    # ------------ Sprites ------------ #

    def initialize_sprites(self):
        """ initialize_sprites

            loads all the sprites into the sprite array

            param:
                none

            return:
                none

            test:
                * sprites are appended correct (size & image is right)
                * all sprites are appended
        """
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/tile000.png"),  # [1]
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
        """ sprite_update

            updates the index of current sprite to create an animation

            param:
                direction(str): direction in which the zombie is moving

            return:
                none

            test:
                * sprite animation fits to the zombie movement
                * animation is displayed correct
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
        """ ai_movement

            algorithm to check in which direction the zombie shall move

            param:
                none

            return:
                none

            test:
                * zombie moves towards player
                * zombie sprite is correct
        """
        self.mx = 0
        self.my = 0

        # Checking Difference to Players-Y Position
        suby = self.y - self.game.player.y
        if suby < 0:
            self.my = config['zombie_speed']
        else:
            self.my = -config['zombie_speed']

        # Checking Difference to Players-X Position
        subx = self.x - self.game.player.x
        if subx < 0:
            self.mx = config['zombie_speed']
        else:
            self.mx = -config['zombie_speed']

        # moving diagonally
        if self.mx != 0 and self.my != 0:
            self.mx *= 0.7071
            self.my *= 0.7071

        # Check which variable is bigger, to decide in which direction the zombie is looking
        if abs(suby) > abs(subx):
            if suby < 0:
                self.sprite_update("down")
            else:
                self.sprite_update("up")
        else:
            if subx < 0:
                self.sprite_update("right")
            else:
                self.sprite_update("left")

    def collide_check(self, direction, target):
        hits = pygame.sprite.spritecollide(self, target, False)
        if direction == "x" and hits:
            if self.mx > 0:
                self.x = hits[0].rect.left - self.rect.width
            if self.mx < 0:
                self.x = hits[0].rect.right
            self.mx = 0
            self.rect.x = self.x
        if direction == "y" and hits:
            if self.my > 0:
                self.y = hits[0].rect.top - self.rect.height
            if self.my < 0:
                self.y = hits[0].rect.bottom
            self.my = 0
            self.rect.y = self.y