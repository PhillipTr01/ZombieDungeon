""" Python Top Down Shooter - ZombieDungeon
    *
    *

    param:
        Author: Stefan Nemanja Banov & Phillip Tran
        Date: 06.06.2021
        Version: 1.0.0
        License: free

    Sources:
        [1] Player (Sprites):
                Designer: Nina Vukovic (Friend of developer) and Stefan Nemanja Banov
"""

from classes.Weapons import *


class Player(pygame.sprite.Sprite):
    """ Player

        this class portrays the player, the playable character of the user

        attributes:
            sprites(list of surface): contains all images / sprites of player
            current_sprite(int): declares which sprite should be displayed
            image(surface): current sprite
            rect(rect): rectangle of player
            x(int): x-coordinate of position
            y(int): y-coordinate of position
            game(game): current game running
            mx(float): movement indicator on x-axis
            my(float): movement indicator on y-axis
            animation_time(int): interval a new sprite is chosen
            health(int): health of player
            invincible_count(int): interval the player can get damage
            shoot_delay(int): interval the player can shoot

        test:
            * Player spawns on correct position (doesn't collide on spawn)
            * [OPEN]
    """

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

        self.health = config['player_health']
        self.invincible_count = 0
        self.shoot_delay = 0

    def update(self):
        """ update

            this method updates the position of the player and handles collisions

            param:
                none

            return:
                none

            test:
                * is moving in the right direction
                * collision is detected and further action is taken
        """

        # Game Over
        if self.health == 0:
            # [SOUND]: Game over sound can be added here
            self.game.gamestate = 3

        # [SOUND]: Player base sound can be added here

        # Change position
        self.x += self.mx * self.game.dt
        self.y += self.my * self.game.dt
        self.rect.topleft = (self.x, self.y)

        # Collide with wall
        if pygame.sprite.spritecollideany(self, self.game.collision_sprites):
            # Reset position so that player doesn't pass or goes through the wall
            self.x -= self.mx * self.game.dt
            self.y -= self.my * self.game.dt
            self.rect.topleft = (self.x, self.y)

        # Collide with enemy
        if pygame.sprite.spritecollideany(self, self.game.enemy_sprites):
            # if player is not "invincible" he gets damage
            if self.invincible_count == 0:
                # [SOUND]: Player hurt sound can be added here
                self.health -= config['zombie_damage']
                self.invincible_count = 50

            # Reset position so that player doesn't pass or goes through zombie
            self.x -= self.mx * self.game.dt
            self.y -= self.my * self.game.dt
            self.rect.topleft = (self.x, self.y)

        # Collide with door
        if pygame.sprite.spritecollideany(self, self.game.door_sprites):
            # Move on to the next room
            # [SOUND]: Room transition sound can be added here
            self.game.next_room(pygame.sprite.spritecollideany(self, self.game.door_sprites))

        if self.invincible_count > 0:
            self.invincible_count -= 1

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
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/player/tile000.png"),  # [1]
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
        """ sprite_update

            updates the index of current sprite to create an animation

            param:
                direction(str): direction in which the player is moving

            return:
                none

            test:
                * sprite animation fits to the player movement
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
        """ movement

            algorithm to check in which direction the zombie shall move

            param:
                none

            return:
                none

            test:
                * player can shoot
                * pressed keys captured correct
        """
        self.mx = 0
        self.my = 0
        direction = "idle"
        key = pygame.key.get_pressed()

        # moving left
        if key[pygame.K_a] and not key[pygame.K_d]:
            self.mx = -config['player_speed']
            direction = "left"

        # moving right
        if key[pygame.K_d] and not key[pygame.K_a]:
            self.mx = config['player_speed']
            direction = "right"

        # moving up
        if key[pygame.K_w] and not key[pygame.K_s]:
            self.my = -config['player_speed']
            direction = "up"

        # moving down
        if key[pygame.K_s] and not key[pygame.K_w]:
            self.my = config['player_speed']
            direction = "down"

        # moving diagonally
        if self.mx != 0 and self.my != 0:
            self.mx *= 0.7071
            self.my *= 0.7071

        # shooting left
        if key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
            if self.shoot_delay == 0:
                self.shoot_delay = config['weapon_shoot_delay']
                Fireball(self.game, self.x, self.y, 'left')

            direction = "left"

        # shooting right
        elif key[pygame.K_RIGHT] and not key[pygame.K_LEFT]:
            if self.shoot_delay == 0:
                self.shoot_delay = config['weapon_shoot_delay']
                Fireball(self.game, self.x, self.y, 'right')

            direction = "right"

        # shooting up
        elif key[pygame.K_UP] and not key[pygame.K_DOWN]:
            if self.shoot_delay == 0:
                self.shoot_delay = config['weapon_shoot_delay']
                Fireball(self.game, self.x, self.y, 'up')

            direction = "up"

        # shooting down
        elif key[pygame.K_DOWN] and not key[pygame.K_UP]:
            if self.shoot_delay == 0:
                self.shoot_delay = config['weapon_shoot_delay']
                Fireball(self.game, self.x, self.y, 'down')

            direction = "down"

        if self.shoot_delay > 0:
            self.shoot_delay -= 1

        self.sprite_update(direction)
