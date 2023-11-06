import pygame
from decoration import *
from enemy import Enemy
from game_data import levels
from particles import ParticleEffect
from player import Player
from settings import screen_height, screen_width, tile_size
from tiles import *
from util import import_csv_layout, import_cut_graphic
import os

BASE_DIR_PATH = os.path.expanduser("~" + "/Documents")


class Level:
    EDGE_SCROLL_DELTA = 0.45

    def __init__(self, current_level, surface, create_overworld):
        # Level setup
        self.display_surface = surface
        self.world_shift = 0
        self.current_x = 0

        # Overworld setup
        self.current_level = current_level
        self.create_overworld = create_overworld
        level_data = levels[self.current_level]
        self.new_max_level = level_data["unlock"]

        # Player setup
        player_layout = import_csv_layout(level_data["player"])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        # Terrain setup
        terrain_layout = import_csv_layout(level_data["terrain"])
        self.terrain_sprites = self.create_tile_group(terrain_layout, "terrain")

        # Grass setup
        grass_layout = import_csv_layout(level_data["grass"])
        self.grass_sprites = self.create_tile_group(grass_layout, "grass")

        # Dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

        # crates
        crate_layout = import_csv_layout(level_data["crates"])
        self.crate_sprites = self.create_tile_group(crate_layout, "crates")

        # coins
        coin_layout = import_csv_layout(level_data["coins"])
        self.coin_sprites = self.create_tile_group(coin_layout, "coins")

        # foreground palms
        fg_palm_layout = import_csv_layout(level_data["fg_palms"])
        self.fg_palm_sprites = self.create_tile_group(fg_palm_layout, "fg_palms")

        # background palms
        bg_palm_layout = import_csv_layout(level_data["bg_palms"])
        self.bg_palm_sprites = self.create_tile_group(bg_palm_layout, "bg_palms")

        # enemy
        enemy_layout = import_csv_layout(level_data["enemies"])
        self.enemy_sprites = self.create_tile_group(enemy_layout, "enemies")

        # constraint
        constraint_layout = import_csv_layout(level_data["constraints"])
        self.constraint_sprites = self.create_tile_group(constraint_layout, "constraint")

        # decoration
        self.sky = Sky(8)
        level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(screen_height - 20, level_width)
        self.clouds = Clouds(400, level_width, 30)

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != "-1":
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == "terrain":
                        terrain_tile_list = import_cut_graphic(BASE_DIR_PATH + "/CODE/workspace/python/pygame/graphics/terrain/terrain_tiles.png")
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(x, y, tile_size, tile_surface)

                    if type == "grass":
                        grass_tile_list = import_cut_graphic(BASE_DIR_PATH + "/CODE/workspace/python/pygame/graphics/decoration/grass/grass.png")
                        grass_tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(x, y, tile_size, grass_tile_surface)

                    if type == "crates":
                        sprite = Crate(tile_size, x, y)

                    if type == "coins":
                        if val == "0":
                            sprite = Coin(tile_size, x, y, BASE_DIR_PATH + "/CODE/workspace/python/pygame/graphics/coins/gold", 5)
                        if val == "1":
                            sprite = Coin(tile_size, x, y, BASE_DIR_PATH + "/CODE/workspace/python/pygame/graphics/coins/silver", 1)
                    if type == "fg_palms":
                        if val == "5" or val == "1":
                            sprite = Palm(tile_size, x, y, BASE_DIR_PATH + "/CODE/workspace/python/pygame/graphics/terrain/palm_small", 38)
                        if val == "4":
                            sprite = Palm(tile_size, x, y, BASE_DIR_PATH + "/CODE/workspace/python/pygame/graphics/terrain/palm_large", 64)
                        if val == "0":
                            sprite = Palm(tile_size, x, y, BASE_DIR_PATH + "/CODE/workspace/python/pygame/graphics/terrain/palm_bg", 64)
                    if type == "bg_palms":
                        sprite = Palm(tile_size, x, y, BASE_DIR_PATH + "/CODE/workspace/python/pygame/graphics/terrain/palm_bg", 64)
                    if type == "enemies":
                        sprite = Enemy(tile_size, x, y)
                    if type == "constraint":
                        sprite = Tile(tile_size, x, y)

                    sprite_group.add(sprite)

        return sprite_group

    def create_jump_partical(self, position):
        if self.player.sprite.facing_right:
            position -= pygame.math.Vector2(10, 5)
        else:
            position += pygame.math.Vector2(10, -5)
        jump_particle_sprite = ParticleEffect(position, "jump")
        self.dust_sprite.add(jump_particle_sprite)

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def create_landing_partical(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10, 15)
            else:
                offset = pygame.math.Vector2(-10, 15)
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, "land")
            self.dust_sprite.add(fall_dust_particle)

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if cell == "X":
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                if cell == "P":
                    player_sprite = Player((x, y), self.display_surface, self.create_jump_partical)
                    self.player.add(player_sprite)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        colilidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.fg_palm_sprites.sprites()

        for sprite in colilidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False

        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        colilidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.fg_palm_sprites.sprites()

        for sprite in colilidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.on_ground = True
                    player.direction.y = 0
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.on_ceiling = True
                    player.direction.y = 0

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == "0":
                    sprite = Player((x, y), self.display_surface, self.create_jump_partical)
                    self.player.add(sprite)
                if val == "1":
                    hat_surface = pygame.image.load(BASE_DIR_PATH + "/CODE/workspace/python/pygame/graphics/character/hat.png").convert_alpha()
                    sprite = StaticTile(x, y, tile_size, hat_surface)
                    self.goal.add(sprite)

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()

    def check_death(self):
        if self.player.sprite.rect.top > screen_height:
            self.create_overworld(self.current_level, 0)

    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            self.create_overworld(self.current_level, self.new_max_level)

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_p]:
            self.create_overworld(self.current_level, self.new_max_level)

    def run(self):
        self.get_input()
        # sky
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface, self.world_shift)

        # background palms
        self.bg_palm_sprites.update(self.world_shift)
        self.bg_palm_sprites.draw(self.display_surface)

        # dust particles
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        # terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        # enemy
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)

        # self.explosion_sprites.update(self.world_shift)
        # self.explosion_sprites.draw(self.display_surface)

        # crate
        self.crate_sprites.update(self.world_shift)
        self.crate_sprites.draw(self.display_surface)

        # grass
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        # coins
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)

        # player sprites
        self.scroll_x()
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)
        self.player.update()
        self.horizontal_movement_collision()
        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.create_landing_partical()
        self.player.draw(self.display_surface)

        self.check_death()
        self.check_win()

        # Water
        self.water.draw(self.display_surface, self.world_shift)

        # foreground palms
        self.fg_palm_sprites.update(self.world_shift)
        self.fg_palm_sprites.draw(self.display_surface)
