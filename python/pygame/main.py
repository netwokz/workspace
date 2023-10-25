import pygame
import sys
from settings import *
from level import Level
from game_data import level_0

# PyGame setup
pygame.init()
FPS = 60
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level(level_0, screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill("white")
    level.run()

    pygame.display.update()
    clock.tick(FPS)
