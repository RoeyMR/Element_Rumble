import pygame
import os
from settings import *
from entity import Entity


class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, assets_path):
        super().__init__(pos, groups, obstacle_sprites, assets_path)
        self.image = pygame.image.load(r".\character\front\front_1.png").convert_alpha()
        self.image = pygame.transform.scale_by(self.image, (PLAYER_SPRITE_SCALE, PLAYER_SPRITE_SCALE))
        self.rect = self.image.get_rect(topleft = pos)
        self.speed = NORMAL_SPEED

        self.attacking = False
        self.attack_cooldown = ATTACK_COOLDOWN
        self.attack_time = None
        self.attack_duration = ATTACK_DURATION
        self.last_attack_frame = 0  # enables to display only part of the attack animation (so the attack is quick)

        self.hitbox = self.rect.inflate(0, -20)
        self.obstacle_sprites = obstacle_sprites

        # dash attributes
        self.dash_time = None
        self.dash_cooldown = DASH_COOLDOWN
        self.dash_duration = DASH_DURATION

        # animation attributes
        # self.animations = {'right_idle': [], 'left_idle': [], 'right': [], 'left': [], 'right_jump': [], 'left_jump': [],
        # 'right_jump_down': [], 'left_jump_down': [], 'right_jump_up': [], 'left_jump_up': [], 'right_roll': [],
        # 'left_roll': [], 'right_attack_1': [], 'left_attack_1': [], 'right_attack_2': [], 'left_attack_2': [],
        # 'right_attack_3': [], 'left_attack_3': [], 'right_special': [], 'left_special': [], 'right_defend': [],
        # 'left_defend': [], 'right_take_hit': [], 'left_take_hit': [], 'right_death': [], 'left_death': [],
        # 'right_air_attack': [], 'left_air_attack': []}


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
        current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        if not self.attacking and "dash" not in self.status:
            # movement input
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.last_direction_x = self.direction.x = 1
                self.status = "right"
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.last_direction_x = self.direction.x = -1
                self.status = "left"
            elif "dash" not in self.status:
                self.direction.x = 0
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.last_direction_y = self.direction.y = -1
                #self.status = self.status.split("_")[0]
                self.status = "back"
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.last_direction_y = self.direction.y = 1
                #self.status = self.status.split("_")[0]
                self.status = "front"
            elif "dash" not in self.status:
                self.direction.y = 0

        if keys[pygame.K_k] and not self.attacking and \
                (not self.attack_time or current_time - self.attack_time >= self.attack_cooldown):
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.direction.x, self.direction.y = (0, 0)
            if "_attack" not in self.status:
                self.frame_index = self.last_attack_frame
                if "idle" in self.status:
                    self.status = self.status.replace("idle", "attack")
                else:
                    self.status += "_attack"

        if keys[pygame.K_l] and not self.attacking and (not self.dash_time or current_time - self.dash_time >= self.dash_cooldown):
            self.dash_time = pygame.time.get_ticks()
            if "_dash" not in self.status:
                if "idle" in self.status:
                    self.status = self.status.replace("idle", "dash")
                else:
                    self.status += "_dash"
                self.speed = DASH_SPEED
                if self.direction.x == 0 and self.direction.y == 0:
                    self.direction.x, self.direction.y = DIRECTIONS[self.status.split("_")[0]]

        # if keys[pygame.K_j] and not self.attacking:
        #     self.attacking = True
        #     self.attack_time = pygame.time.get_ticks()
        #     if "_attack_2" not in self.status:
        #         if "idle" in self.status:
        #             self.status = self.status.replace("idle", "attack_2")
        #         else:
        #             self.status += "_attack_2"
        #
        # if keys[pygame.K_i] and not self.attacking:
        #     self.attacking = True
        #     self.attack_time = pygame.time.get_ticks()
        #     if "_attack_3" not in self.status:
        #         if "idle" in self.status:
        #             self.status = self.status.replace("idle", "attack_3")
        #         else:
        #             self.status += "_attack_3"
        #
        # if keys[pygame.K_p] and not self.attacking:
        #     self.attacking = True
        #     self.attack_time = pygame.time.get_ticks()
        #     if "_special" not in self.status:
        #         if "idle" in self.status:
        #             self.status = self.status.replace("idle", "special")
        #         else:
        #             self.status += "_special"

        if not self.attacking and self.direction.x == 0 and self.direction.y == 0:
            if "_attack" not in self.status and "_dash" not in self.status and "_idle" not in self.status:
                self.status += "_idle"

    def check_durations(self):  # checks the durations of actions in the game and disables them if necessary
        current_time = pygame.time.get_ticks()

        # attack cooldown
        if "attack" in self.status:
            self.last_attack_frame = self.frame_index
            if current_time - self.attack_time >= self.attack_duration:
                self.attacking = False
                if "_idle" not in self.status:
                    self.status = self.status.replace("attack", "idle")

        # dash cooldown
        if "dash" in self.status:
            if current_time - self.dash_time >= self.dash_duration:
                #self.status = self.status.replace("dash", "idle")
                self.speed = NORMAL_SPEED
                self.status = self.status.replace("dash", "idle")


    def update(self):
        self.get_input()
        self.animate()
        self.check_durations()
        self.move()
