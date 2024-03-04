import pygame
import os
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load(r".\Elementals_fire_knight_FREE_v1.1\png\fire_knight\right_idle\right_idle_1.png").convert_alpha()
        self.image = pygame.transform.scale_by(self.image, (PLAYER_SPRITE_SCALE, PLAYER_SPRITE_SCALE))
        self.rect = self.image.get_rect(topleft = pos)
        self.direction = pygame.math.Vector2()
        self.speed = 10

        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        self.hitbox = self.rect.inflate(0, -20)
        self.obstacle_sprites = obstacle_sprites

        # animation attributes
        self.animations = {'right_idle': [], 'left_idle': [], 'right': [], 'left': [], 'right_jump': [], 'left_jump': [],
        'right_jump_down': [], 'left_jump_down': [], 'right_jump_up': [], 'left_jump_up': [], 'right_roll': [],
        'left_roll': [], 'right_attack_1': [], 'left_attack_1': [], 'right_attack_2': [], 'left_attack_2': [],
        'right_attack_3': [], 'left_attack_3': [], 'right_special': [], 'left_special': [], 'right_defend': [],
        'left_defend': [], 'right_take_hit': [], 'left_take_hit': [], 'right_death': [], 'left_death': [],
        'right_air_attack': [], 'left_air_attack': []}
        self.import_player_assets()
        self.status = "right_idle"    # the status of the player (the animation that is presented)
        self.frame_index = 0
        self.animation_speed = 0.3

    def import_player_assets(self):
        assets_path = r".\Elementals_fire_knight_FREE_v1.1\png\fire_knight"

        for animation in self.animations.keys():
            folder_name = os.path.join(assets_path, animation)
            for filename in os.listdir(folder_name):
                self.animations[animation].append(
                    pygame.transform.scale_by(pygame.image.load(os.path.join(folder_name, filename)).convert_alpha(),
                                              (PLAYER_SPRITE_SCALE, PLAYER_SPRITE_SCALE)))
    # def get_status(self):
    #
    #     if self.direction.x == 1 or self.direction.y == 1:  # moving right or
    #         self.status = "run"
    #     elif self.direction.x == -1 or self.direction.y == -1:
    #     if self.direction.x == 0 and self.direction.y == 0:
    #         self.status = "idle"
    #
    #     if self.attacking:
    #         self.direction.x = 0
    #         self.direction.y = 0
    #
    #     print(self.status)

    def get_input(self):

        keys = pygame.key.get_pressed()
        if not self.attacking:
            # movement input
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.direction.y = -1
                self.status = self.status.split("_")[0]
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.direction.y = 1
                self.status = self.status.split("_")[0]
            else:
                self.direction.y = 0
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.direction.x = 1
                self.status = "right"
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.direction.x = -1
                self.status = "left"
            else:
                self.direction.x = 0

        if keys[pygame.K_k] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            if "_attack_1" not in self.status:
                if "idle" in self.status:
                    self.status = self.status.replace("idle", "attack_1")
                else:
                    self.status += "_attack_1"

        if keys[pygame.K_j] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            if "_attack_2" not in self.status:
                if "idle" in self.status:
                    self.status = self.status.replace("idle", "attack_2")
                else:
                    self.status += "_attack_2"

        if keys[pygame.K_i] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            if "_attack_3" not in self.status:
                if "idle" in self.status:
                    self.status = self.status.replace("idle", "attack_3")
                else:
                    self.status += "_attack_3"

        if keys[pygame.K_p] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            if "_special" not in self.status:
                if "idle" in self.status:
                    self.status = self.status.replace("idle", "special")
                else:
                    self.status += "_special"

        if not self.attacking and self.direction.x == 0 and self.direction.y == 0:
            if "_attack_1" not in self.status and "_special" not in self.status and "_idle" not in self.status:
                self.status += "_idle"


    def cooldown(self):  # checks the cooldowns in the game and applies them if necessary
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                if "_idle" not in self.status:
                    self.status += "_idle"

    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x*self.speed
        self.collision("horizontal")
        self.hitbox.y += self.direction.y*self.speed
        self.collision("vertical")
        #self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right
        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index = self.frame_index + self.animation_speed
        if self.frame_index > len(animation):
            self.frame_index = 0
            if self.attacking:
                self.attacking = False
                self.status = self.status.split("_")[0] + "_idle"
        print(f"status: {self.status}, frame: {self.frame_index}")

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(bottomleft = self.hitbox.bottomleft)
        print(f"center: {self.rect.center}")

    def update(self):
        self.get_input()
        self.animate()
        self.move()
