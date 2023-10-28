import sys

import pygame
from level import Level
from overworld import Overworld
from settings import *
from ui import UI


class Game:
    def __init__(self):
        # Game attributes
        self.max_level = 0
        self.max_health = 100
        self.current_health = 100
        self.coins = 0

        # Handle UI
        self.ui = UI(screen)

        # Create overworld
        self.overworld = Overworld(0, self.max_level, screen, self.create_level)
        self.status = "overworld"

    def create_level(self, current_level):
        self.level = Level(current_level, screen, self.create_overworld)
        self.status = "level"

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level)
        self.status = "overworld"

    def run(self):
        if self.status == "overworld":
            self.overworld.run()
        else:
            self.level.run()
            self.ui.show_health_bar(self.current_health, self.max_health)
            self.ui.show_coin(self.coins)


# PyGame setup
pygame.init()
FPS = 60
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill("white")
    game.run()

    pygame.display.update()
    clock.tick(FPS)
