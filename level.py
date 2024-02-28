import pygame
from settings import *
from tile import Tile
from player import Player
from map_loading import *


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = CameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()
        #self.create_map()

        self.player = Player((64*5, 64*5), [self.visible_sprites], self.obstacles_sprites)
        ground_layout = import_csv_layout(r".\map\layers\map._ground.csv")
        self.terrain_sprites = self.create_tile_group(ground_layout, "ground")
        props_layout = import_csv_layout(r".\map\layers\map._props.csv")
        self.create_tile_group(props_layout, "prop")
        trees_layout = import_csv_layout(r".\map\layers\map._entities.csv")
        self.create_tile_group(trees_layout, "tree")

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        ground_surfaces_list = import_tiles(r".\tile assets\Texture\TX Tileset Grass.png")

        for row_index, row in enumerate(layout):
            for col_index, tile_id in enumerate(row):
                if tile_id != "-1":
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE

                    if type == "ground":    # the ground layer
                        sprite_group.add(Tile((x, y), [self.visible_sprites], surface=ground_surfaces_list[int(tile_id)]))
                    elif type == "prop":
                        sprite_group.add(Tile((x, y), [self.visible_sprites, self.obstacles_sprites], surface=pygame.image.load(PROPS_IMAGES[tile_id])))
                    elif type == "tree":
                        sprite_group.add(Tile((x, y), [self.visible_sprites], surface=pygame.image.load(TREES_IMAGES[tile_id])))

        return sprite_group

    def create_map(self):   # creates the game objects according to the map
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if col == "X":
                    Tile((x, y), [self.visible_sprites, self.obstacles_sprites])
                elif col == "P":
                    self.player = Player((x, y), [self.visible_sprites], self.obstacles_sprites)

    def run(self):
        self.visible_sprites.draw_from_camera_angle(self.player, self.terrain_sprites)
        self.visible_sprites.update()


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # self.floor_surface = pygame.image.load(r".\tile assets\floor_tile.png").convert()
        # self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))
        #


    def draw_from_camera_angle(self, player, terrain_sprites):
        """ draws the scene from the angle of the camera, draws the upper objects first
        
        """
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        for sprite in sorted(terrain_sprites, key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

        for sprite in sorted(list(set(self.sprites()) - set(terrain_sprites)), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
