""" Python Top Down Shooter - ZombieDungeon
    *
    * This class contains the whole logic of the game

    param:
        Author: Stefan Nemanja Banov & Phillip Tran
        Date: 06.06.2021
        Version: 1.0.0
        License: free

    Sources:
        Transparent Rectangle:
            Link: https://stackoverflow.com/questions/6339057/draw-a-transparent-rectangle-in-pygame
        Transition:
            Link: https://www.youtube.com/watch?v=H2r2N7D56Uw
"""
import copy
import sys

from classes.Grid import *
from classes.Player import *
from classes.Score import *
from classes.Objects import *
from classes.Zombie import *


class Game:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("ZombieDungeon")
        pygame.display.set_icon(pygame.image.load('images/game/zombie.png'))
        pygame.key.set_repeat(500, 100)
        clock = pygame.time.Clock()
        self.dt = clock.tick(config["fps"]) / 1000
        self.font = pygame.font.Font("fonts/dogicapixel.otf", 30)
        self.screen = pygame.display.set_mode((config['resolution_width'], config['resolution_height']))

        self.gamestate = 0  # 0 - Running (not started), 1 - Started, 2 - Paused
        self.character_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.background_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.door_sprites = pygame.sprite.Group()
        self.weapon_sprites = pygame.sprite.Group()
        self.score = Score()
        self.level = 1
        self.level_grid = Grid(11, 11)
        self.level_grid.fill_grid(self.level)
        self.current_x = self.level_grid.start_x
        self.current_y = self.level_grid.start_y
        self.player = None
        self.next_room_direction = ''
        self.zombie_count = 0
        self.copied_room = copy.deepcopy(rooms[self.level_grid.grid[self.current_y][self.current_x].room_number])
        self.room_decoding(rooms[0])

    def room_cleared(self):
        fade = pygame.Surface((config['resolution_width'], config['resolution_height']))
        fade.fill((0, 0, 0))

        self.copied_room = copy.deepcopy(rooms[self.level_grid.grid[self.current_y][self.current_x].room_number])
        self.level_grid.grid[self.current_y][self.current_x].status = 2
        self.add_doors(self.level_grid.grid[self.current_y][self.current_x])
        self.room_decoding(rooms[self.level_grid.grid[self.current_y][self.current_x].room_number])
        self.level_grid.room_count -= 1

        if self.level_grid.room_count == 0:
            self.screen.fill((0, 0, 0))
            start_label = self.font.render("Level " + str(self.level) + " cleared!", True, (255, 255, 255))
            self.screen.blit(start_label, (self.screen.get_width() / 2 - start_label.get_width() / 2, self.screen.get_height() / 2.5))
            pygame.display.update()
            pygame.time.wait(2000)

            self.score.add_score(1000)  # 1000 Score per Level - 100 per Zombie
            self.level += 1
            self.level_grid = Grid(11, 11)
            self.level_grid.fill_grid(self.level)
            self.current_x = self.level_grid.start_x
            self.current_y = self.level_grid.start_y
            self.player.x = round(((len(rooms[0][0]) - 1) / 2)) * config['tile_size']
            self.player.y = round(((len(rooms[0]) - 1) / 2)) * config['tile_size']
            self.player.health = self.player.max_health
            self.copied_room = copy.deepcopy(rooms[self.level_grid.grid[self.current_y][self.current_x].room_number])
            self.room_decoding(rooms[0])

        for alpha in range(0, 50):
            fade.set_alpha(alpha)
            self.screen.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(3)

    def room_decoding(self, room_map):
        """
        room_decoding

            -

            param:
                room_map(2-dimensional array): -

            return:
                none

            test:
                * -
        """
        if self.current_y == self.level_grid.start_y and self.current_x == self.level_grid.start_x or self.level_grid.grid[self.current_y][self.current_x].status == 2:
            self.add_doors(self.level_grid.grid[self.current_y][self.current_x])

        self.collision_sprites = pygame.sprite.Group()
        self.background_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.door_sprites = pygame.sprite.Group()
        self.weapon_sprites = pygame.sprite.Group()

        if self.next_room_direction == 'left':
            self.player.x = (len(rooms[0][0]) - 2) * config['tile_size']
            self.player.y = (round((len(rooms[0]) - 1) / 2)) * config['tile_size']
        elif self.next_room_direction == 'right':
            self.player.x = 1 * config['tile_size']
            self.player.y = (round((len(rooms[0]) - 1) / 2)) * config['tile_size']
        elif self.next_room_direction == 'up':
            self.player.x = (round((len(rooms[0][0]) - 1) / 2)) * config['tile_size']
            self.player.y = (len(rooms[0]) - 2) * config['tile_size']
        elif self.next_room_direction == 'down':
            self.player.x = (round((len(rooms[0][0]) - 1) / 2)) * config['tile_size']
            self.player.y = 1 * config['tile_size']

        if self.current_x != round((self.level_grid.size_x - 1) / 2) or self.current_y != round(
                (self.level_grid.size_y - 1) / 2):
            if self.level_grid.grid[self.current_y][self.current_x].status == 1:
                self.zombie_count = random.randint(2, config['max_zombie_count'])

                for count in range(self.zombie_count):
                    x = 0
                    y = 0

                    while room_map[y][x] != 'g' or abs(self.player.x / config['tile_size'] - x) < 3 or abs(self.player.y / config['tile_size'] - y) < 3:
                        x = random.randint(0, len(room_map[0]) - 1)
                        y = random.randint(0, len(room_map) - 1)

                    room_map[y][x] = 'z'

        y = 0
        for column in room_map:
            x = 0
            for tile in column:
                if tile == "w":
                    Wall(self, x, y)
                if tile == "g":
                    Ground(self, x, y)
                if tile == "d":
                    Door(self, x, y)
                if tile == "p":
                    if self.player is None:
                        self.player = Player(self, x, y)
                    Ground(self, x, y)
                if tile == "z":
                    Zombie(self, x, y)
                    Ground(self, x, y)
                x += 1
            y += 1

        self.next_room_direction = ''
        rooms[self.level_grid.grid[self.current_y][self.current_x].room_number] = self.copied_room

    def add_doors(self, room):
        if 'left' in room.doors:
            rooms[room.room_number][round((len(rooms[0]) - 1) / 2)][0] = 'd'
        if 'right' in room.doors:
            rooms[room.room_number][round((len(rooms[0]) - 1) / 2)][len(rooms[0][0]) - 1] = 'd'
        if 'up' in room.doors:
            rooms[room.room_number][0][round((len(rooms[0][0]) - 1) / 2)] = 'd'
        if 'down' in room.doors:
            rooms[room.room_number][len(rooms[0]) - 1][round((len(rooms[0][0]) - 1) / 2)] = 'd'

    def next_room(self, sprite):
        fade = pygame.Surface((config['resolution_width'], config['resolution_height']))
        fade.fill((0, 0, 0))

        x = sprite.rect.x / config['tile_size']
        y = sprite.rect.y / config['tile_size']

        self.level_grid.grid[self.current_y][self.current_x].status = 3

        if x == 0 and y == round((len(rooms[0]) - 1) / 2):
            self.current_x -= 1
            self.next_room_direction = 'left'
        elif x == len(rooms[0][0]) - 1 and y == round((len(rooms[0]) - 1) / 2):
            self.current_x += 1
            self.next_room_direction = 'right'
        elif x == round((len(rooms[0][0]) - 1) / 2) and y == 0:
            self.current_y -= 1
            self.next_room_direction = 'up'
        elif x == round((len(rooms[0][0]) - 1) / 2) and y == len(rooms[0]) - 1:
            self.current_y += 1
            self.next_room_direction = 'down'

        next_room = self.level_grid.grid[self.current_y][self.current_x]

        self.copied_room = copy.deepcopy(rooms[next_room.room_number])

        if next_room.status != 3:
            next_room.status = 1
        else:
            next_room.status = 2

        self.room_decoding(rooms[next_room.room_number])

        rooms[next_room.room_number] = self.copied_room

        for alpha in range(0, 200):
            fade.set_alpha(alpha)
            self.screen.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(3)

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
        if self.player.health == 0:
            self.gamestate = 3

        self.character_sprites.update()
        self.enemy_sprites.update()
        self.weapon_sprites.update()

    # ------------ Gamestates ------------ #

    def start_screen(self):
        """
        start_screen

            -

            param:
                none

            return:
                none

            test:
                * -
        """

        self.screen.fill((0, 0, 0))

        start_screen_image = pygame.transform.scale(pygame.image.load("images/game/start_screen.png"),
                                                    (config["resolution_width"], config["resolution_height"]))
        start_screen_image.set_alpha(150)
        self.screen.blit(start_screen_image, (0, 0))
        start_label = self.font.render("Welcome to Zombie Dungeon", True, (48, 131, 255))
        start_label2 = self.font.render("Press Enter to Start the Game!", True, (48, 131, 255))
        self.screen.blit(start_label, (self.screen.get_width() / 2 - start_label.get_width() / 2, self.screen.get_height() / 2.5))
        self.screen.blit(start_label2, (self.screen.get_width() / 2 - start_label2.get_width() / 2, (self.screen.get_height() / 2.5) + 100))
        pygame.display.flip()

        key = pygame.key.get_pressed()
        if key[pygame.K_KP_ENTER] or key[pygame.K_RETURN]:
            self.gamestate = 1

    def pause(self):
        """
        pause

            -

            param:
                none

            return:
                none

            test:
                * -
        """

        dim_screen = pygame.Surface((config['resolution_width'], config['resolution_height']))
        dim_screen.set_alpha(200)
        dim_screen.fill((0, 0, 0))
        self.screen.blit(dim_screen, (0, 0))

        pause_label = self.font.render("The game has been paused.", True, (255, 255, 255))
        pause_label2 = self.font.render('Press "ESCAPE" to resume!', True, (255, 255, 255))
        self.screen.blit(pause_label, (self.screen.get_width() / 2 - pause_label.get_width() / 2, self.screen.get_height() / 2.5))
        self.screen.blit(pause_label2, (self.screen.get_width() / 2 - pause_label2.get_width() / 2, (self.screen.get_height() / 2.5) + 100))

    def game_over_screen(self):
        """
        start_screen

            -

            param:
                none

            return:
                none

            test:
                * -
        """

        self.screen.fill((0, 0, 0))

        game_over_screen = pygame.transform.scale(pygame.image.load("images/game/game_over_screen.jpg"),
                                                  (config["resolution_width"], config["resolution_height"]))
        game_over_screen.set_alpha(75)
        self.screen.blit(game_over_screen, (0, 0))
        game_over_label = self.font.render("Game Over!", True, (255, 255, 255))
        game_over_label2 = self.font.render("Your Score: " + str(self.score.score), True, (255, 255, 255))
        self.screen.blit(game_over_label, (self.screen.get_width() / 2 - game_over_label.get_width() / 2, self.screen.get_height() / 2.5))
        self.screen.blit(game_over_label2, (self.screen.get_width() / 2 - game_over_label2.get_width() / 2, (self.screen.get_height() / 2.5) + 100))
        pygame.display.flip()

    # ------------ Draw Objects on Screen ------------ #

    def show_health(self):
        """
        show_health

            -

            param:
                none

            return:
                none

            test:
                * -
        """
        full_heart = pygame.image.load('images/player/health/full_heart.png').convert_alpha()
        empty_heart = pygame.image.load('images/player/health/empty_heart.png').convert_alpha()

        for heart in range(self.player.max_health):
            if heart < self.player.health:
                self.screen.blit(full_heart, ((heart * 45 + 30), 15))
            else:
                self.screen.blit(empty_heart, ((heart * 45 + 30), 15))

    def show_score(self):
        """
        show_score

            -

            param:
                none

            return:
                none

            test:
                * -
        """
        font = pygame.font.Font("fonts/dogicapixel.otf", 20)
        rendered_score = font.render("Score: " + str(self.score.score), True, (255, 255, 255))
        self.screen.blit(rendered_score, (config["resolution_width"] - 250, 20))

    def show_level(self):
        """
        show_level

            -

            param:
                none

            return:
                none

            test:
                * -
        """
        font = pygame.font.Font("fonts/dogicapixel.otf", 20)
        rendered_level = font.render("Level: " + str(self.level), True, (255, 255, 255))
        self.screen.blit(rendered_level, (config["resolution_width"] - 190, config["resolution_height"] - 30))

    def show_map(self):
        """
        show_map

            -

            param:
                none

            return:
                none

            test:
                * -
        """
        map_surface = pygame.Surface((165, 165), pygame.SRCALPHA)
        map_surface.fill((0, 0, 0, 175))
        map_surface.fill((220, 220, 220, 64), map_surface.get_rect().inflate(-5, -5))
        self.screen.blit(map_surface, (20, config['resolution_height'] - 185))

        for x in range(self.level_grid.size_x):
            for y in range(self.level_grid.size_y):
                map_grid = pygame.Surface((15, 15), pygame.SRCALPHA)

                room = self.level_grid.grid[y][x]

                if room.room_number > -1:
                    if room.status == 0:
                        map_grid.fill((0, 0, 0, 200))
                        map_grid.fill((37, 36, 31, 175), map_grid.get_rect().inflate(-3, -3))
                    elif room.status == 1 or room.status == 2:
                        map_grid.fill((0, 0, 0, 200))
                        map_grid.fill((64, 145, 255, 255), map_grid.get_rect().inflate(-3, -3))
                    elif room.status == 3:
                        map_grid.fill((0, 0, 0, 200))
                        map_grid.fill((171, 170, 171, 175), map_grid.get_rect().inflate(-3, -3))

                self.screen.blit(map_grid, (x * 15 + 20, y * 15 + config['resolution_height'] - 185))

    def draw(self):
        """
        draw

            -

            param:
                none

            return:
                none

            test:
                * -
        """
        self.screen.fill((93, 227, 106))
        self.background_sprites.draw(self.screen)
        self.collision_sprites.draw(self.screen)
        self.door_sprites.draw(self.screen)
        self.character_sprites.draw(self.screen)
        self.enemy_sprites.draw(self.screen)
        self.weapon_sprites.draw(self.screen)
        self.show_health()
        self.show_score()
        self.show_level()
        self.show_map()

        if self.gamestate == 2:
            self.pause()

        pygame.display.flip()

    # ------------ Events ------------ #

    def shoot(self, x, y, dir):
        Fireball(self, x, y, dir)

    def general_key_events(self):
        """
        general_key_events

            -

            param:
                none

            return:
                none

            test:
                * -
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if self.gamestate > 0:
                    if event.key == pygame.K_ESCAPE:
                        self.gamestate = 1 if self.gamestate == 2 else 2

    # ------------ Not used ------------ #

    # def grid(self):
    #    """
    #    grid
    #
    #        -
    #
    #        param:
    #            none
    #
    #        return:
    #            none
    #
    #        test:
    #            * -
    #    """
    #    for x in range(0, config['resolution_width'], config['tile_size']):
    #        pygame.draw.line(self.screen, (0, 0, 0), (x, 0), (x, config['resolution_height']))
    #    for y in range(0, config['resolution_height'], config['tile_size']):
    #        pygame.draw.line(self.screen, (0, 0, 0), (0, y), (config['resolution_width'], y))
