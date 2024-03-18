import pygame
from settings import *
from tile import Tile
from player import Player
from map_loading import *
from enemy import Enemy
from weapon import Weapon
from entity import Entity


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = CameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()

        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        self.player = Player((64*5, 64*5), [self.visible_sprites], self.obstacles_sprites, r".\character", self.create_attack)
        Weapon(self.player, [self.visible_sprites, self.attack_sprites], r"C:\Users\roeym\PycharmProjects\Element_Rumble\weapons\sword.png")

        Enemy("fire worm",(64*10, 64*10), [self.visible_sprites, self.attackable_sprites], self.obstacles_sprites, self.player)



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

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collided_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collided_sprites:
                    for target_sprite in collided_sprites:
                        if isinstance(target_sprite, Entity):
                            target_sprite.get_damage(attack_sprite)
                            print(f"target sprite health: {target_sprite.health}")

    def create_attack(self):
        pass

    def run(self):
        self.visible_sprites.draw_from_camera_angle(self.player, self.terrain_sprites)
        self.visible_sprites.update()
        self.player_attack_logic()


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
        if not target.attacking:
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
