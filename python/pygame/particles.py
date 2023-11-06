import pygame
from util import import_folder
import os

BASE_DIR_PATH = os.path.expanduser("~" + "/Documents")


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, position, type_of_particle):
        super().__init__()
        self.frame_index = 0
        self.animation_speed = 0.5

        if type_of_particle == "jump":
            self.frames = import_folder(BASE_DIR_PATH + "/CODE/workspace/python/pygame/graphics/character/dust_particles/jump")

        if type_of_particle == "land":
            self.frames = import_folder(BASE_DIR_PATH + "/CODE/workspace/python/pygame/graphics/character/dust_particles/land")

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=position)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self, x_shift):
        self.animate()
        self.rect.x += x_shift
