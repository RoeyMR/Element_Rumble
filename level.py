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
        self.camera_borders = {"left": 400, "right": 400, "top": 200, "bottom": 200}
        width = self.display_surface.get_size()[0] - (self.camera_borders["left"] + self.camera_borders["right"])
        height = self.display_surface.get_size()[1] - (self.camera_borders["top"] + self.camera_borders["bottom"])
        self.camera_rect = pygame.Rect(self.camera_borders["left"], self.camera_borders["top"],
                                       width, height)

        # self.floor_surface = pygame.image.load(r".\tile assets\floor_tile.png").convert()
        # self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))
        #
    def update_camera_rect(self, target):  # moves the rect of the camera if the player goes out of it
        if target.rect.left < self.camera_rect.left:
            self.camera_rect.left = target.rect.left

        if target.rect.right > self.camera_rect.right:
            self.camera_rect.right = target.rect.right

        if target.rect.top < self.camera_rect.top:
            self.camera_rect.top = target.rect.top

        if target.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = target.rect.bottom

        self.offset.x = self.camera_rect.left - self.camera_borders["left"]
        self.offset.y = self.camera_rect.top - self.camera_borders["top"]


    def draw_from_camera_angle(self, player, terrain_sprites):
        """ draws the scene from the angle of the camera, draws the upper objects first
        
        """
        self.update_camera_rect(player)

        for sprite in sorted(terrain_sprites, key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

        for sprite in sorted(list(set(self.sprites()) - set(terrain_sprites)), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
