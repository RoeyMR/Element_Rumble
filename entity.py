import pygame
from settings import *
import os


class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, assets_path):
        super().__init__(groups)
        self.image = pygame.image.load(
            r".\character\front\front_1.png").convert_alpha()
        self.image = pygame.transform.scale_by(self.image, (PLAYER_SPRITE_SCALE, PLAYER_SPRITE_SCALE))
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.math.Vector2()
        self.speed = 10
        self.health = 100

        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.attack_duration = 400

        self.hitbox = self.rect.inflate(0, -20)
        self.obstacle_sprites = obstacle_sprites

        # animation attributes
        self.animations = {}
        self.import_assets(assets_path)
        self.status = "right_idle"  # the status of the player (the animation that is presented)
        self.frame_index = 0
        self.animation_speed = 0.3
        self.status = "right_idle"    # the status of the entity (the animation that is presented)

        # makes sure the damage of the attack is reduced only once for each attack
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 400

    def import_assets(self, assets_path):
        for animation_folder in os.listdir(assets_path):
            folder_name = os.path.join(assets_path, animation_folder)
            if os.path.isdir(folder_name):
                self.animations[animation_folder] = []
                for filename in os.listdir(folder_name):
                    self.animations[animation_folder].append(
                        pygame.transform.scale_by(pygame.image.load(os.path.join(folder_name, filename)).convert_alpha(),
                                                  (PLAYER_SPRITE_SCALE, PLAYER_SPRITE_SCALE)))

    def get_damage(self, weapon):
        if self.vulnerable and weapon.player.attacking:
            self.health -= weapon.damage
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

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

    def check_durations(self):  # checks the durations of actions in the game and disables them if necessary
        current_time = pygame.time.get_ticks()

        # attack duration
        if "attack" in self.status:
            self.last_attack_frame = self.frame_index
            if current_time - self.attack_time >= self.attack_duration:
                self.attacking = False
                if "_idle" not in self.status:
                    self.status = self.status.replace("attack", "idle")

        # vulnerability duration
        if not self.vulnerable and current_time - self.hit_time >= self.invincibility_duration:
            self.vulnerable = True

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index = self.frame_index + self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
            # if self.attacking:
            #     self.attacking = False
            #     self.status = self.status.split("_")[0] + "_idle"

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(bottomleft = self.hitbox.bottomleft)

