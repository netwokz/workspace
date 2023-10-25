import pygame
from tiles import *
from player import Player
from enemy import Enemy
from settings import tile_size, screen_width, screen_height
from particles import ParticleEffect
from decoration import *
from util import import_csv_layout, import_cut_graphic


class Level:
    EDGE_SCROLL_DELTA = 0.45

    def __init__(self, level_data, surface):
        # Level setup
        self.display_surface = surface
        self.world_shift = -4

        # self.setup_level(level_data)
        # Terrain setup
        terrain_layout = import_csv_layout(level_data["terrain"])
        self.terrain_sprites = self.create_tile_group(terrain_layout, "terrain")

        # Grass setup
        grass_layout = import_csv_layout(level_data["grass"])
        self.grass_sprites = self.create_tile_group(grass_layout, "grass")

        self.current_x = 0

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
                        terrain_tile_list = import_cut_graphic("C:/Users/deanejst/Documents/CODE/workspace/python/pygame/graphics/terrain/terrain_tiles.png")
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(x, y, tile_size, tile_surface)

                    if type == "grass":
                        grass_tile_list = import_cut_graphic("C:/Users/deanejst/Documents/CODE/workspace/python/pygame/graphics/decoration/grass/grass.png")
                        grass_tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(x, y, tile_size, grass_tile_surface)

                    if type == "crates":
                        sprite = Crate(tile_size, x, y)

                    if type == "coins":
                        if val == "0":
                            sprite = Coin(tile_size, x, y, "graphics/coins/gold", 5)
                        if val == "1":
                            sprite = Coin(tile_size, x, y, "graphics/coins/silver", 1)
                    if type == "fg_palms":
                        if val == "5":
                            sprite = Palm(tile_size, x, y, "graphics/terrain/palm_small", 38)
                        if val == "4":
                            sprite = Palm(tile_size, x, y, "graphics/terrain/palm_large", 64)
                        if val == "0":
                            sprite = Palm(tile_size, x, y, "graphics/terrain/palm_bg", 64)
                    if type == "bg_palms":
                        sprite = Palm(tile_size, x, y, "graphics/terrain/palm_bg", 64)
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

        for sprite in self.tiles.sprites():
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

        for sprite in self.tiles.sprites():
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

    def run(self):
        # Dust
        # self.dust_sprite.update(self.world_shift)
        # self.dust_sprite.draw(self.display_surface)

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

        # self.enemy_collision_reverse()
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

        # foreground palms
        self.fg_palm_sprites.update(self.world_shift)
        self.fg_palm_sprites.draw(self.display_surface)

        # self.scroll_x()

        # Level Player
        # self.player.update()
        # self.horizontal_movement_collision()
        # self.get_player_on_ground()
        # self.vertical_movement_collision()
        # self.create_landing_partical()
        # self.player.draw(self.display_surface)
