""" Python Top Down Shooter - ZombieDungeon
    *
    * This class portrays all static objects

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


class Ground(pygame.sprite.Sprite):
    """ Ground
        *
        * This class portrays all static objects

        type:
            pygame.sprite.Sprite
    """
    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self, game.background_sprites)
        self.image = pygame.transform.scale(pygame.image.load("images/objects/ground.png"),     # [1]
                                            (config['tile_size'], config['tile_size']))
        self.rect = self.image.get_rect()
        self.rect.x = x * config['tile_size']
        self.rect.y = y * config['tile_size']


class Wall(pygame.sprite.Sprite):
    """ Python Top Down Shooter - ZombieDungeon
        *
        * This class portrays all static objects

        param:
            Author: Stefan Nemanja Banov & Phillip Tran
            Date: 06.06.2021
            Version: 1.0.0
            License: free

        Sources:
            [1] Sprites:
                    Designer: Nina Vukovic (Friend of developer)
    """
    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self, game.collision_sprites)
        self.image = pygame.transform.scale(pygame.image.load("images/objects/wall.png"),       # [1]
                                            (config['tile_size'], config['tile_size']))
        self.rect = self.image.get_rect()
        self.rect.x = x * config['tile_size']
        self.rect.y = y * config['tile_size']


class Door(pygame.sprite.Sprite):
    """ Python Top Down Shooter - ZombieDungeon
        *
        * This class portrays all static objects

        param:
            Author: Stefan Nemanja Banov & Phillip Tran
            Date: 06.06.2021
            Version: 1.0.0
            License: free

        Sources:
            [1] Sprites:
                    Designer: Nina Vukovic (Friend of developer)
    """
    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self, game.door_sprites)
        self.image = pygame.transform.scale(pygame.image.load("images/objects/ground.png"),     # [1]
                                            (config['tile_size'], config['tile_size']))
        self.rect = self.image.get_rect()
        self.rect.x = x * config['tile_size']
        self.rect.y = y * config['tile_size']
