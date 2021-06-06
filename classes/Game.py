""" Python Top Down Shooter - ZombieDungeon
    *
    *

    param:
        Author: Stefan Nemanja Banov & Phillip Tran
        Date: 06.06.2021
        Version: 1.0.0
        License: free

    Sources:
        [1] Transparent Rectangle:
            Link: https://stackoverflow.com/questions/6339057/draw-a-transparent-rectangle-in-pygame
        [2] Transition:
            Link: https://www.youtube.com/watch?v=H2r2N7D56Uw
        [3] Health Container:
            Tutorial-Link: https://www.youtube.com/watch?v=WLYEsgYkEvY
        [4] Tile Game Idea:
            Tutorial-Link: https://www.youtube.com/watch?v=3UxnelT9aCo
"""

import copy
import sys
import logging

try:
    from classes.Logs import *
    from classes.Grid import *
    from classes.Player import *
    from classes.Objects import *
    from classes.Zombie import *
except ImportError as e:
    logging.critical("Not all of the required classes could be loaded!")


try:
    config["resolution_width"]
    config["resolution_height"]
    config['tile_size']
    config['player_health']
    config['min_zombie_count']
    config['max_zombie_count']
    config["fps"]
except KeyError:
    logging.critical("Config is incomplete!")
    sys.exit()

class Game:
    """ Game

        this class is the heart of the game, everything will be processed here

        attributes:
            dt(int): delta time
            font(font): font for texts
            screen(surface): game window
            gamestate(int): the state the game is in (Started Program, started game, paused game, lost game)
            score(int): points of player
            level(int): level of current game
            character_sprites(group of sprites): a group of sprites of the player
            collision_sprites(group of sprites): a group of sprites of 'wall'
            background_sprites(group of sprites): a group of sprites of 'ground'
            enemy_sprites(group of sprites): a group of sprites of 'zombie'
            door_sprites(group of sprites): a group of sprites of 'door'
            weapon_sprites(group of sprites): a group of sprites of 'fireball'
            player(player): player
            zombie_count(int): number of zombies in current room
            level_grid(grid): current map of level
            current_x(int): x-coordinate of current room on grid
            current_y(int): y-coordinate of current room on grid
            copied_room(2d-list of str): deep-copied room map
            start_button_rect(rect): rectangle of start button
            exit_button_rect(rect): rectangle of exit button
            restart_button_rect(rect): rectangle of restart button

        test:
            * Game processes everything right - no errors while playing
            * pygame initialization is correct
    """

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Zombie Dungeon")
        try:
            pygame.display.set_icon(pygame.image.load('images/game/zombie.png'))
        except FileNotFoundError:
            logging.critical("Zombie Dungeon logo not found")
        pygame.key.set_repeat(500, 100)
        self.dt = pygame.time.Clock().tick(config["fps"]) / 1000
        try:
            self.font = pygame.font.Font("fonts/dogicapixel.otf", 35)
        except FileNotFoundError:
            logging.critical("Custom fonts not found")
        self.screen = pygame.display.set_mode((config['resolution_width'], config['resolution_height']))

        self.game_state = 0
        self.score = 0
        self.level = 1

        self.character_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.background_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.door_sprites = pygame.sprite.Group()
        self.weapon_sprites = pygame.sprite.Group()

        self.player = None
        self.zombie_count = 0

        self.level_grid = Grid(11, 11)
        self.level_grid.fill_grid(self.level)
        self.current_x = self.level_grid.start_x
        self.current_y = self.level_grid.start_y
        self.copied_room = copy.deepcopy(rooms[self.level_grid.grid[self.current_y][self.current_x].room_number])
        self.room_decoding(rooms[0], 'start')

        self.start_button_rect = None
        self.exit_button_rect = None
        self.restart_button_rect = None

        # Logging
        logging.info("New Game Instace has been intialized")
        # [SOUND] Game music can be added here

    def update(self):
        """ update

            updates the display of the whole screen and gets input from user

            param:
                none

            return:
                none

            test:
                * all objects are displayed
                * input is captured
        """

        self.character_sprites.update()
        self.enemy_sprites.update()
        self.weapon_sprites.update()
        self.player.movement()
        self.draw()

    # ------------ Events ------------ #

    def general_key_events(self):
        """ general_key_events

            check if user quits the game or tries to pause the game

            param:
                none

            return:
                none

            test:
                * game is paused
                * game can be exited
        """

        for event in pygame.event.get():
            # user quits program
            if event.type == pygame.QUIT:
                logging.info("Game has been successfully closed")
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # user pauses program
                if self.game_state > 0:
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = 1 if self.game_state == 2 else 2
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.game_state == 0 and self.start_button_rect.collidepoint(event.pos):
                        self.game_state = 1
                    elif self.game_state == 0 and self.exit_button_rect.collidepoint(event.pos):
                        logging.info("Game has been successfully closed")
                        sys.exit()
                    elif self.game_state == 3 and self.restart_button_rect.collidepoint(event.pos):
                        self.game_state = 4

    def room_cleared(self):
        """ room_cleared

            adds doors to the room, after the player has killed all zombies.
                - if it's the last room on this level the grid will generate a new map

            param:
                none

            return:
                none

            test:
                * doors are on the correct positions
                * on level up, information is updated - new map is generated, score is added, level is increased
                * player position is updated
        """

        # Transition fading for each level
        fade = pygame.Surface((config['resolution_width'], config['resolution_height']))    # [2]
        fade.fill((0, 0, 0))

        self.level_grid.grid[self.current_y][self.current_x].status = 2
        self.level_grid.room_count -= 1

        # add doors to the room and decode the room again
        self.copied_room = copy.deepcopy(rooms[self.level_grid.grid[self.current_y][self.current_x].room_number])
        self.add_doors(self.level_grid.grid[self.current_y][self.current_x])
        self.room_decoding(rooms[self.level_grid.grid[self.current_y][self.current_x].room_number], 'none')

        # if all rooms has been cleared go to the next level (new map)
        if self.level_grid.room_count == 0:
            # display that the level has been cleared
            self.screen.fill((0, 0, 0))
            start_label = self.font.render("Level " + str(self.level) + " cleared!", True, (255, 255, 255))
            self.screen.blit(start_label, (self.screen.get_width() / 2 - start_label.get_width() / 2, self.screen.get_height() / 2 - start_label.get_height() / 2))
            pygame.display.update()
            pygame.time.wait(2000)

            # add points and increase level
            self.score += 1000  # +1000 Score per Level
            self.level += 1

            # create a new grid
            self.level_grid = Grid(11, 11)
            self.level_grid.fill_grid(self.level)
            self.current_x = self.level_grid.start_x
            self.current_y = self.level_grid.start_y

            # deep-copy room and decode it
            self.copied_room = copy.deepcopy(rooms[self.level_grid.grid[self.current_y][self.current_x].room_number])
            self.room_decoding(rooms[0], 'start')

            # Change position and give player full health
            self.player.x = round(((len(rooms[0][0]) - 1) / 2)) * config['tile_size']
            self.player.y = round(((len(rooms[0]) - 1) / 2)) * config['tile_size']
            self.player.health = config['player_health']

        for alpha in range(0, 75):  # [2]
            fade.set_alpha(alpha)
            self.screen.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(3)

    def next_room(self, sprite):
        """ next_room

            transition to the next room on grid (going through a door)

            param:
                sprite(sprite): sprite colliding with door

            return:
                none

            test:
                * going into the right direction on the grid
                * room status updated properly
        """
        fade = pygame.Surface((config['resolution_width'], config['resolution_height']))    # [2]
        fade.fill((0, 0, 0))

        x = sprite.rect.x / config['tile_size']
        y = sprite.rect.y / config['tile_size']
        next_room_direction = ''

        # update status of current room
        self.level_grid.grid[self.current_y][self.current_x].status = 3

        # get position of next room
        if x == 0 and y == round((len(rooms[0]) - 1) / 2):
            self.current_x -= 1
            next_room_direction = 'left'
        elif x == len(rooms[0][0]) - 1 and y == round((len(rooms[0]) - 1) / 2):
            self.current_x += 1
            next_room_direction = 'right'
        elif x == round((len(rooms[0][0]) - 1) / 2) and y == 0:
            self.current_y -= 1
            next_room_direction = 'up'
        elif x == round((len(rooms[0][0]) - 1) / 2) and y == len(rooms[0]) - 1:
            self.current_y += 1
            next_room_direction = 'down'

        next_room = self.level_grid.grid[self.current_y][self.current_x]

        # check if room has been cleared already, if yes there shouldn't spawn any zombies anymore
        next_room.status = 1 if next_room.status != 3 else 2

        # deepcopy room_map and decode room
        self.copied_room = copy.deepcopy(rooms[next_room.room_number])
        self.room_decoding(rooms[next_room.room_number], next_room_direction)

        # reset room_map of 'rooms-list'
        rooms[next_room.room_number] = self.copied_room

        for alpha in range(0, 200):     # [2]
            fade.set_alpha(alpha)
            self.screen.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(3)

    # ------------ Roomupdate ------------ #

    def room_decoding(self, room_map, next_room_direction):
        """ room_decoding

            decode room map from strings to real objects

            param:
                room_map(2d-list of str): list of all objects with their coordinates
                next_room_direction(str): direction of the next room

            return:
                none

            test:
                * all zombies are assigned on the room map
                * rooms are decoded right
        """

        # Reset all sprites
        self.collision_sprites = pygame.sprite.Group()
        self.background_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.door_sprites = pygame.sprite.Group()
        self.weapon_sprites = pygame.sprite.Group()

        # add doors to the start room
        if next_room_direction == 'start' or self.level_grid.grid[self.current_y][self.current_x].status == 2:
            self.add_doors(self.level_grid.grid[self.current_y][self.current_x])

        # move player to the right position (if he left the previous room on the left, he should spawn on the right)
        if next_room_direction == 'left':
            self.player.x = (len(rooms[0][0]) - 2) * config['tile_size']
            self.player.y = (round((len(rooms[0]) - 1) / 2)) * config['tile_size']
        elif next_room_direction == 'right':
            self.player.x = 1 * config['tile_size']
            self.player.y = (round((len(rooms[0]) - 1) / 2)) * config['tile_size']
        elif next_room_direction == 'up':
            self.player.x = (round((len(rooms[0][0]) - 1) / 2)) * config['tile_size']
            self.player.y = (len(rooms[0]) - 2) * config['tile_size']
        elif next_room_direction == 'down':
            self.player.x = (round((len(rooms[0][0]) - 1) / 2)) * config['tile_size']
            self.player.y = 1 * config['tile_size']

        # spawn zombies
        if next_room_direction != 'start' and self.level_grid.grid[self.current_y][self.current_x].status == 1:

            # determine zombie count random
            self.zombie_count = random.randint(config['min_zombie_count'], config['max_zombie_count'])

            for count in range(self.zombie_count):
                x = 0
                y = 0

                # if there is an obstacle or the player within a radius of 3 try to find another spawn point
                while room_map[y][x] != 'g' \
                        or abs(self.player.x / config['tile_size'] - x) < 3 \
                        or abs(self.player.y / config['tile_size'] - y) < 3:
                    x = random.randint(1, len(room_map[0]) - 2)
                    y = random.randint(1, len(room_map) - 2)

                room_map[y][x] = 'z'

        # Decode all strings and create real objects
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

        # reset room map in rooms list
        rooms[self.level_grid.grid[self.current_y][self.current_x].room_number] = self.copied_room

    def add_doors(self, room):
        """ add_doors

            add doors to the room map

            param:
                room(room): current room

            return:
                none

            test:
                * coordinates are on the right position
                * doors are beeing added to the room map
        """
        if 'left' in room.doors:
            rooms[room.room_number][round((len(rooms[0]) - 1) / 2)][0] = 'd'

        if 'right' in room.doors:
            rooms[room.room_number][round((len(rooms[0]) - 1) / 2)][len(rooms[0][0]) - 1] = 'd'

        if 'up' in room.doors:
            rooms[room.room_number][0][round((len(rooms[0][0]) - 1) / 2)] = 'd'

        if 'down' in room.doors:
            rooms[room.room_number][len(rooms[0]) - 1][round((len(rooms[0][0]) - 1) / 2)] = 'd'

    # ------------ Gamestates ------------ #

    def start_screen(self):
        """ start_screen

            display the start screen

            param:
                none

            return:
                none

            test:
                * start screen is displayed
                * text is displayed
        """

        self.screen.fill((0, 0, 0))

        start_screen_image = pygame.transform.scale(pygame.image.load("images/game/start_screen.png"),  # [1]
                                                    (config["resolution_width"], config["resolution_height"]))
        # make image a little bit transparent
        start_screen_image.set_alpha(150)
        self.screen.blit(start_screen_image, (0, 0))

        # define textlabels
        start_label = self.font.render("Welcome to Zombie Dungeon", True, (48, 131, 255))
        self.screen.blit(start_label, (self.screen.get_width() / 2 - start_label.get_width() / 2,
                                       self.screen.get_height() / 4))

        # start button
        start_button_text = self.font.render(">>Start<<", True, (48, 131, 255))
        self.start_button_rect = start_button_text.get_rect()
        self.start_button_rect.topleft = (self.screen.get_width() / 2 - start_button_text.get_width() / 2, self.screen.get_height() / 4 + 150)
        self.screen.blit(start_button_text, (self.screen.get_width() / 2 - start_button_text.get_width() / 2, self.screen.get_height() / 4 + 150))

        # exit button
        exit_button_text = self.font.render(">>Exit<<", True, (48, 131, 255))
        self.exit_button_rect = exit_button_text.get_rect()
        self.exit_button_rect.topleft = (self.screen.get_width() / 2 - exit_button_text.get_width() / 2, self.screen.get_height() / 4 + 250)
        self.screen.blit(exit_button_text, (self.screen.get_width() / 2 - exit_button_text.get_width() / 2, self.screen.get_height() / 4 + 250))

        pygame.display.flip()

    def pause(self):
        """ pause

            pause game

            param:
                none

            return:
                none

            test:
                * pause screen is displayed
                * text is displayed
                * game is paused (no updates)
        """

        # screen is dimmed to see the text better
        dim_screen = pygame.Surface((config['resolution_width'], config['resolution_height']))  # [1]
        dim_screen.set_alpha(200)
        dim_screen.fill((0, 0, 0))
        self.screen.blit(dim_screen, (0, 0))

        # define textlabels
        pause_label = self.font.render("The game has been paused.", True, (255, 255, 255))
        pause_label2 = self.font.render('Press "ESCAPE" to resume!', True, (255, 255, 255))
        self.screen.blit(pause_label, (self.screen.get_width() / 2 - pause_label.get_width() / 2,
                                       self.screen.get_height() / 2.5))
        self.screen.blit(pause_label2, (self.screen.get_width() / 2 - pause_label2.get_width() / 2,
                                        (self.screen.get_height() / 2.5) + 100))

    def game_over_screen(self):
        """ game_over_screen

            display game over screen

            param:
                none

            return:
                none

            test:
                * show score + text
                * image is displayed correct
        """

        self.screen.fill((0, 0, 0))

        game_over_screen = pygame.transform.scale(pygame.image.load("images/game/game_over_screen.jpg"),    # [1]
                                                  (config["resolution_width"], config["resolution_height"]))
        # make image a little transparent
        game_over_screen.set_alpha(75)
        self.screen.blit(game_over_screen, (0, 0))

        # define textlabels
        game_over_label = self.font.render("Game Over!", True, (255, 255, 255))
        game_over_label2 = self.font.render("Your Score: " + str(self.score), True, (255, 255, 255))
        self.screen.blit(game_over_label, (self.screen.get_width() / 2 - game_over_label.get_width() / 2, self.screen.get_height() / 3.5))
        self.screen.blit(game_over_label2, (self.screen.get_width() / 2 - game_over_label2.get_width() / 2, (self.screen.get_height() / 3.5) + 100))

        # restart button
        restart_text = self.font.render('>>Restart<<', True, (255, 255, 255))
        self.restart_button_rect = restart_text.get_rect()
        self.restart_button_rect.topleft = (self.screen.get_width() / 2 - restart_text.get_width() / 2, self.screen.get_height() / 2 + 100)
        self.screen.blit(restart_text, (self.screen.get_width() / 2 - restart_text.get_width() / 2, self.screen.get_height() / 2 + 100))

        pygame.display.flip()

    # ------------ Draw Objects on Screen ------------ #

    def show_health(self):  # [3]
        """ show_health

            display the health containers of the player

            param:
                none

            return:
                none

            test:
                * health is updated on damage of player
                * container show the correct amount of hearts of player
        """

        # load images of hearts
        full_heart = pygame.image.load('images/player/health/full_heart.png').convert_alpha()
        empty_heart = pygame.image.load('images/player/health/empty_heart.png').convert_alpha()

        for heart in range(config['player_health']):
            if heart < self.player.health:
                # if heart exists draw a full heart
                self.screen.blit(full_heart, ((heart * 45 + 30), 15))
            else:
                # if heart doesn't exists draw an empty heart
                self.screen.blit(empty_heart, ((heart * 45 + 30), 15))

    def show_score(self):
        """ show_score

            display the score of the player

            param:
                none

            return:
                none

            test:
                * score is displayed on the top-right
                * score is updated frequently
        """

        font = pygame.font.Font("fonts/dogicapixel.otf", 20)
        rendered_score = font.render("Score: " + str(self.score), True, (255, 255, 255))
        self.screen.blit(rendered_score, (config["resolution_width"] - 250, 20))

    def show_level(self):
        """ show_level

            display the current level of the game

            param:
                none

            return:
                none

            test:
                * level is correct
                * text is displayed on the bottom-right corner
        """

        font = pygame.font.Font("fonts/dogicapixel.otf", 20)
        rendered_level = font.render("Level: " + str(self.level), True, (255, 255, 255))
        self.screen.blit(rendered_level, (config["resolution_width"] - 190, config["resolution_height"] - 30))

    def show_map(self):
        """ show_map

            display the map with all rooms in it

            param:
                none

            return:
                none

            test:
                * rooms have the right color based on their status (current room is highlighted in blue)
                * grid is pictured correctly
        """



        # Rectangle of Map (background)
        map_surface = pygame.Surface((165, 165), pygame.SRCALPHA)   # [1]
        map_surface.fill((0, 0, 0, 175))
        map_surface.fill((220, 220, 220, 64), map_surface.get_rect().inflate(-5, -5))
        self.screen.blit(map_surface, (20, config['resolution_height'] - 185))


        # fill map surface with all rooms
        for x in range(self.level_grid.size_x):
            for y in range(self.level_grid.size_y):
                map_grid = pygame.Surface((15, 15), pygame.SRCALPHA)    # [1]

                room = self.level_grid.grid[y][x]

                # Don't draw 'empty' rooms
                if room.room_number > -1:
                    # rooms not visited yet (darkgray)
                    if room.status == 0:
                        map_grid.fill((0, 0, 0, 200))
                        map_grid.fill((37, 36, 31, 175), map_grid.get_rect().inflate(-3, -3))
                    # current room (blue)
                    elif room.status == 1 or room.status == 2:
                        map_grid.fill((0, 0, 0, 200))
                        map_grid.fill((64, 145, 255, 255), map_grid.get_rect().inflate(-3, -3))
                    # rooms cleared (light gray)
                    elif room.status == 3:
                        map_grid.fill((0, 0, 0, 200))
                        map_grid.fill((171, 170, 171, 175), map_grid.get_rect().inflate(-3, -3))
                self.screen.blit(map_grid, (x * 15 + 20, y * 15 + config['resolution_height'] - 185))

    def draw(self):
        """ draw

            draw is calling all display-functions and updating them to the latest 'version'

            param:
                none

            return:
                none

            test:
                * all information are displayed on the screen (sprites, text, map...)
                * game is paused, when switching to gamestate 2
                * display is updated properly
        """
        self.screen.fill((93, 227, 106))

        # draw all sprites
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

        # check if game is paused
        if self.game_state == 2:
            self.pause()

        pygame.display.flip()

    # ------------ Not used ------------ #

    # def grid(self):
    #
    #    for x in range(0, config['resolution_width'], config['tile_size']):
    #        pygame.draw.line(self.screen, (0, 0, 0), (x, 0), (x, config['resolution_height']))
    #    for y in range(0, config['resolution_height'], config['tile_size']):
    #        pygame.draw.line(self.screen, (0, 0, 0), (0, y), (config['resolution_width'], y))
