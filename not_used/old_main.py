import pygame
import sys

import classes.Grid as grid
import classes.Score as scores
import not_used.Health as Health

grid = grid.Grid(11, 11)

grid.fill_grid(10)

pygame.init()
screen = pygame.display.set_mode([550, 600])
clock = pygame.time.Clock()
health = Health.Health(5)
pygame.key.set_repeat(1, 20)
full_heart = pygame.image.load('../images/player/health/full_heart.png').convert_alpha()
empty_heart = pygame.image.load('../images/player/health/empty_heart.png').convert_alpha()
font = pygame.font.SysFont('calibri', 30)
score = scores.Score()
level = 0

WHITE = (0, 0, 0)

while True:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    gedrueckt = pygame.key.get_pressed()
    if gedrueckt[pygame.K_ESCAPE]:
        sys.exit()
    if gedrueckt[pygame.K_r]:
        grid.fill_grid(10)
    if gedrueckt[pygame.K_DOWN]:
        health.get_damage(1)
    elif gedrueckt[pygame.K_UP]:
        health.get_health(1)
    if gedrueckt[pygame.K_o]:
        score.add_score(100)

    for x in range(grid.size_x):
        for y in range(grid.size_y):
            rect = pygame.rect.Rect(x * 50, y * 50 + 50, 50, 50)

            room = grid.grid[y][x].previous_door

            if room == 'e':
                pygame.draw.rect(screen, WHITE, rect)
            elif room == 's':
                pygame.draw.rect(screen, (229, 147, 22), rect)
            elif room == 'u':
                pygame.draw.rect(screen, (0, 255, 0), rect)
            elif room == 'd':
                pygame.draw.rect(screen, (0, 0, 255), rect)
            elif room == 'l':
                pygame.draw.rect(screen, (255, 0, 0), rect)
            elif room == 'r':
                pygame.draw.rect(screen, (255, 255, 0), rect)

    for heart in range(health.max_health):
        if heart < health.health:
            screen.blit(full_heart, ((heart * 40 + 10), 5))
        else:
            screen.blit(empty_heart, ((heart * 40 + 10), 5))

    rendered_score = font.render("Score: " + str(score.score), True, (255, 255, 255))
    rendered_level = font.render("Level " + str(level), True, (255, 255, 255))
    screen.blit(rendered_score, (400, 5))
    screen.blit(rendered_level, (250, 5))

    pygame.display.flip()
    clock.tick(60)
