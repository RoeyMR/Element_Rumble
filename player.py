import pygame
import os


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load(r".\Elementals_fire_knight_FREE_v1.1\png\fire_knight\idle\idle_1.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.direction = pygame.math.Vector2()
        self.speed = 5

        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        self.hitbox = self.rect.inflate(0, -20)
        self.obstacle_sprites = obstacle_sprites

        # animation attributes
        self.animations = {"idle": [], "run": [], "jump": [], "jump_down": [], "jump_up": [], "roll": [], "attack_1": [],
                      "attack_2": [], "attack_3": [], "special": [], "defend": [], "take_hit": [], "death": [],
                      "air_attack": []}
        self.import_player_assets()
        self.status = "idle"    # the status of the player (the animation that is presented)
        self.frame_index = 0
        self.animation_speed = 0.15

    def import_player_assets(self):
        assets_path = r".\Elementals_fire_knight_FREE_v1.1\png\fire_knight"

        for animation in self.animations.keys():
            folder_name = os.path.join(assets_path, animation)
            for filename in os.listdir(folder_name):
                self.animations[animation].append(pygame.image.load(os.path.join(folder_name, filename)).convert_alpha())

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

        # movement input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
            self.status = "run"
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.status = "run"
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pygame.K_k] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.status = "attack_1"

        if keys[pygame.K_p] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.status = "special"

        if not self.attacking and self.direction.x == 0 and self.direction.y == 0:
            self.status = "idle"

    def cooldown(self):  # checks the cooldowns in the game and applies them if necessary
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.status = "idle"

    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x*self.speed
        self.collision("horizontal")
        self.hitbox.y += self.direction.y*self.speed
        self.collision("vertical")
        self.rect.center = self.hitbox.center

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
            if self.status == "attack_1" or self.status == "special":
                self.attacking = False
                self.status = "idle"
        print(f"status: {self.status}, frame: {self.frame_index}")

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(topright = self.hitbox.topright)
        print(f"bottomleft: {self.image.get_rect().bottomleft}")

    def update(self):
        self.get_input()
        self.animate()
        self.move()