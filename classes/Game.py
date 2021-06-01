""" Python Top Down Shooter - ZombieDungeon
    *
    *

    param:
        Author: Stefan Nemanja Banov & Phillip Tran
        Date: 06.06.2021
        Version: 1.0.0
        License: free

    Sources:
        Transparent Rectangle:
            Link: https://stackoverflow.com/questions/6339057/draw-a-transparent-rectangle-in-pygame

"""

import sys

from classes.Grid import *
from classes.Player import *
from classes.Score import *


class Game:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("ZombieDungeon")
        pygame.display.set_icon(pygame.image.load('images/zombie.png'))
        pygame.key.set_repeat(500, 100)
        clock = pygame.time.Clock()
        self.dt = clock.tick(config["fps"]) / 1000
        self.font = pygame.font.Font("fonts/dogicapixel.otf", 30)
        self.screen = pygame.display.set_mode((config['resolution_width'], config['resolution_height']))
        # dim_screen = pygame.Surface(screen.get_size()).convert_alpha()

        self.gamestate = 0 # 0 - Running (not started), 1 - Started, 2 - Paused
        self.character_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.background_sprites = pygame.sprite.Group()
        self.score = Score()
        # self.score.add_score(9999999) # Temporär
        self.level = 1
        # self.level = 9999 # Temporär
        self.grid = Grid(11, 11)
        self.grid.fill_grid(self.level)
        self.player = None

    def start_screen(self):

        start_screen_image = pygame.transform.scale(pygame.image.load("images/start_screen.png"),
                                                    (config["resolution_width"], config["resolution_height"]))
        self.screen.blit(start_screen_image, (0, 0))
        start_label = self.font.render("Welcome to Zombie Dungeon", True, (255, 0, 0))
        start_label2 = self.font.render("Press Enter to Start the Game!", True, (255, 0, 0))
        self.screen.blit(start_label, (self.screen.get_width() / 2 - start_label.get_width() / 2, self.screen.get_height() / 2.5))
        self.screen.blit(start_label2, (self.screen.get_width() / 2 - start_label2.get_width() / 2, (self.screen.get_height() / 2.5) + 100))
        pygame.display.flip()

        key = pygame.key.get_pressed()
        if key[pygame.K_KP_ENTER] or key[pygame.K_RETURN]:
            self.gamestate = 1

    def pause(self):
        dim_screen = pygame.Surface((config['resolution_width'], config['resolution_height']))
        dim_screen.set_alpha(200)
        dim_screen.fill((0, 0, 0))
        self.screen.blit(dim_screen, (0, 0))

        pause_label = self.font.render("The game has been paused.", True, (255, 0, 0))
        pause_label2 = self.font.render('Press "ESCAPE" to resume!', True, (255, 0, 0))
        self.screen.blit(pause_label, (self.screen.get_width() / 2 - pause_label.get_width() / 2, self.screen.get_height() / 2.5))
        self.screen.blit(pause_label2, (self.screen.get_width() / 2 - pause_label2.get_width() / 2, (self.screen.get_height() / 2.5) + 100))

    def grid(self):
        for x in range(0, config['resolution_width'], config['tile_size']):
            pygame.draw.line(self.screen, (0, 0, 0), (x, 0), (x, config['resolution_height']))
        for y in range(0, config['resolution_height'], config['tile_size']):
            pygame.draw.line(self.screen, (0, 0, 0), (0, y), (config['resolution_width'], y))

    def showHealth(self):
        full_heart = pygame.image.load('images/full_heart.png').convert_alpha()
        empty_heart = pygame.image.load('images/empty_heart.png').convert_alpha()

        for heart in range(self.player.max_health):
            if heart < self.player.health:
                self.screen.blit(full_heart, ((heart * 45 + 30), 15))
            else:
                self.screen.blit(empty_heart, ((heart * 45 + 30), 15))

    def showScore(self):
        font = pygame.font.Font("fonts/dogicapixel.otf", 20)
        rendered_score = font.render("Score: " + str(self.score.score), True, (255, 255, 255))
        self.screen.blit(rendered_score, (config["resolution_width"] - 250, 20))

    def showLevel(self):
        font = pygame.font.Font("fonts/dogicapixel.otf", 20)
        rendered_level = font.render("Level: " + str(self.level), True, (255, 255, 255))
        self.screen.blit(rendered_level, (config["resolution_width"] - 190, config["resolution_height"] - 30))

    def showMap(self):

        pass

    def draw(self):
        self.screen.fill((93, 227, 106))
        self.background_sprites.draw(self.screen)
        self.collision_sprites.draw(self.screen)
        self.character_sprites.draw(self.screen)
        self.showHealth()
        self.showScore()
        self.showLevel()
        self.showMap()

        if self.gamestate == 2:
            self.pause()

        pygame.display.flip()

    def update(self):
        self.character_sprites.update()

    def general_key_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if self.gamestate > 0:
                    if event.key == pygame.K_ESCAPE:
                        self.gamestate = 1 if self.gamestate == 2 else 2

    def room_generation(self, room_map):
        y = 0
        for column in room_map:
            x = 0
            for tile in column:
                if tile == "w":
                    Wall(self, x, y)
                if tile == "g":
                    Ground(self, x, y)
                if tile == "p":
                    self.player = Player(self, x, y)
                    Ground(self, x, y)
                x += 1
            y += 1