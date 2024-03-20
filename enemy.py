import pygame
from entity import Entity
from settings import *
from weapon import Projectile


class Enemy(Entity):
    def __init__(self, enemy_name, pos, groups, obstacle_sprites, player, image_scale=1):
        enemy_data = ENEMIES_DATA[enemy_name]
        super().__init__(pos, groups, obstacle_sprites, enemy_data["assets path"], image_scale=image_scale)
        self.health = enemy_data["health"]
        self.damage = enemy_data["damage"]
        self.notice_radius = enemy_data["notice radius"]
        self.attack_radius = enemy_data["attack radius"]
        self.speed = enemy_data["speed"]
        self.attack_cooldown = enemy_data["attack cooldown"]
        self.player = player
        self.health = enemy_data["health"]

    def get_player_distance(self):
        player_vector = pygame.math.Vector2(self.player.rect.center)
        enemy_vector = pygame.math.Vector2(self.rect.center)
        distance = (player_vector - enemy_vector).magnitude()

        return distance

    def get_player_direction(self):
        player_vector = pygame.math.Vector2(self.player.rect.center)
        enemy_vector = pygame.math.Vector2(self.rect.center)
        if self.get_player_distance() > 0:
            return (player_vector - enemy_vector).normalize()
        else:
            return pygame.math.Vector2()

    def get_status(self):
        distance = self.get_player_distance()
        status = ""
        if self.direction.x > 0:
            status = "right"
        elif self.direction.x < 0:
            status = "left"
        else:
            status = self.status.split("_")[0]
        if self.health <= 0:
            self.status = status + "_death"
            return
        if distance <= self.attack_radius:
            status += "_attack"
            if "attack" not in self.status:
                self.attack_time = pygame.time.get_ticks()
        elif distance <= self.notice_radius:
            status += "_move"
        else:
            status += "_idle"
        self.status = status

    def act(self):
        if self.status.endswith("move"):
            self.direction = self.get_player_direction()
        else:
            self.direction = pygame.math.Vector2()

    def update(self):
        self.get_status()
        self.act()
        self.check_durations()
        self.move()
        self.animate()
        if "death" in self.status and  self.frame_index + self.animation_speed >= len(self.animations[self.status]):
            self.kill()


class Shooting_Enemy(Enemy):
    def __init__(self, enemy_name, pos, groups, obstacle_sprites, player, projectile_path, attack_sprite_group,
                 projectile_explosion_path = "", image_scale=1):
        super().__init__(enemy_name, pos, groups, obstacle_sprites, player, image_scale=image_scale)

        self.projectile_path = projectile_path
        self.projectile_explosion_path = projectile_explosion_path
        self.attack_sprite_group = attack_sprite_group

    def act(self):
        super().act()

        if "attack" in self.status and self.frame_index == 0:
            self.resistant_against.append(Projectile(self.player, self.groups() + [self.attack_sprite_group], r".\enemy assets\Fire Worm\Sprites\Fire Ball\move\move_1.png",
                   self.groups()[0], 15, 7, self.obstacle_sprites, self.get_player_direction(), effect_path=r".\enemy assets\Fire Worm\Sprites\Fire Ball\move",
                       pos = self.rect.center, explosion_path=r".\enemy assets\Fire Worm\Sprites\Fire Ball\explosion",
                                          image_scale=self.image_scale))
