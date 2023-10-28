from os import walk
import os
import pygame
from csv import reader
from settings import tile_size


def import_folder(path):
    surface_list = []

    for _, __, img_files in walk(path):
        for image in img_files:
            fullpath = path + "/" + image
            image_surf = pygame.image.load(fullpath).convert_alpha()
            surface_list.append(image_surf)

    return surface_list


def import_csv_layout(path):
    full_path = os.path.join("C:/Users/deanejst/Documents/CODE/workspace/python/pygame/", path)
    terrian_map = []
    with open(full_path, "r") as map:
        level = reader(map, delimiter=",")
        for row in level:
            terrian_map.append(list(row))
        return terrian_map


def import_cut_graphic(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / tile_size)
    tile_num_y = int(surface.get_size()[1] / tile_size)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size
            y = row * tile_size

            new_surface = pygame.Surface((tile_size, tile_size), flags=pygame.SRCALPHA)
            new_surface.blit(surface, (0, 0), pygame.Rect(x, y, tile_size, tile_size))
            cut_tiles.append(new_surface)
    return cut_tiles
