import pygame
import os


class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups, image_path, visible_sprites, damage, effect_path = "", image_scale=1, pos=(0, 0)):
        super().__init__(groups)

        self.image_scale = image_scale
        self.damage = damage

        self.player = player
        self.visible_sprites = visible_sprites

        # weapon effect animation attributes
        self.effect = pygame.sprite.Sprite()
        self.frame_index = 0
        self.animation_speed = 0.3
        self.effect_animation = []
        if effect_path != "":
            self.effect_animation = self.import_assets(effect_path)
        self.effect.image = self.effect_animation[0] if len(self.effect_animation) > 0 else None

        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(center = pos)


    def animate_effect(self):
        self.frame_index = self.frame_index + self.animation_speed
        if self.frame_index >= len(self.effect_animation):
            self.frame_index = 0

        self.effect.image = self.effect_animation[int(self.frame_index)]
        self.effect.rect = self.effect.image.get_rect(bottomleft = self.rect.bottomleft)

    def update(self):
        if len(self.effect_animation) > 0:
            effect_visible = self.visible_sprites in self.effect.groups()
            if self.player.attacking:
                if not effect_visible:
                    self.effect.add([self.visible_sprites])
                self.animate_effect()
            elif effect_visible:
                self.effect.remove(self.visible_sprites)

    def import_assets(self, animation_folder):
        assets = []
        for filename in os.listdir(animation_folder):
            assets.append(
                pygame.transform.scale_by(
                    pygame.image.load(os.path.join(animation_folder, filename)).convert_alpha(),
                    (self.image_scale, self.image_scale)))
        return assets


class Held_Weapon(Weapon):
    def __init__(self, player, groups, image_path, visible_sprites, attack_sprites, damage, effect_path = "", image_scale=1):
        super().__init__(player, groups, image_path, visible_sprites, damage, effect_path, image_scale=image_scale)
        direction = self.player.status.split("_")[0]
        self.previous_direction = direction
        self.base_image = pygame.image.load(image_path)

        self.attack_sprites = attack_sprites

        # sets the location of the weapon according to the direction of the player
        if direction == "right":
            self.rect = self.image.get_rect(midleft = self.player.rect.midright)
        elif direction == "left":
            self.image = pygame.transform.flip(self.image, True, False)
            self.rect = self.image.get_rect(midright = self.player.rect.midleft)
        elif direction == "front":
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect(midtop = self.player.rect.midbottom)
        else:
            self.rect = self.image.get_rect(midbottom = self.player.rect.midtop)

    def update(self):
        super().update()

        if self.player.attacking:
            if self.attack_sprites not in self.groups():
                self.add(self.attack_sprites)

        elif self.attack_sprites in self.groups():
            self.remove(self.attack_sprites)

        effect_base_image = self.effect.image
        direction = self.player.status.split("_")[0]
        # sets the location of the weapon according to the direction of the player
        if direction == "right":
            if self.previous_direction != direction:
                self.image = self.base_image.copy()
            self.rect = self.image.get_rect(midleft = self.player.rect.midright)
            self.rect.x -= 5

            if self.player.attacking:
                self.effect.rect.x += 5
        elif direction == "left":
            if self.previous_direction != direction:
                self.image = pygame.transform.flip(self.base_image, True, False)

            self.rect = self.image.get_rect(midright = self.player.rect.midleft)
            self.rect.x += 5

            if self.player.attacking:
                self.effect.image = pygame.transform.flip(effect_base_image, True, False)
                self.effect.rect.x -= 5
        elif direction == "front":
            if self.previous_direction != direction:
                self.image = pygame.transform.flip(self.base_image, False, True)
            self.rect = self.image.get_rect(midtop = self.player.rect.midbottom)
            self.rect.y -= 15
            self.rect.x += 5

            if self.player.attacking:
                self.effect.rect.y += 5
                self.effect.rect.x -= 20
                self.effect.image = pygame.transform.rotate(self.effect.image, -70)

               #self.effect.image = pygame.transform.flip(effect_base_image, True, False)
        else:
            if self.previous_direction != direction:
                self.image = pygame.transform.flip(self.base_image, True, False)
            self.rect = self.image.get_rect(midbottom = self.player.rect.midtop)
            self.rect.y += 25
            self.rect.x -= 5

            if self.player.attacking:
                self.effect.image = pygame.transform.rotate(pygame.transform.flip(effect_base_image, True, True), -50)
                self.effect.rect.y -= 10

        self.previous_direction = direction


class Projectile(Weapon):
    def __init__(self, player, groups, image_path, visible_sprites, damage, speed, obstacle_sprites, direction,
                 effect_path = "", pos = (0, 0), explosion_path="", image_scale=1):
        super().__init__(player, groups, image_path, visible_sprites, damage, effect_path, pos=pos,
                         image_scale=image_scale)

        self.speed = speed
        self.direction = direction
        self.obstacle_sprites = obstacle_sprites
        self.explosion_path = explosion_path

    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.rect.x += self.direction.x*self.speed
        self.collision("horizontal")
        self.rect.y += self.direction.y*self.speed
        self.collision("vertical")

    def collision(self, direction):
        for sprite in self.obstacle_sprites:
            if sprite.rect.colliderect(self.rect):
                self.destroy()

    def destroy(self):
        if self.direction.x != 0 and self.direction.y != 0:
            if self.explosion_path != "":
                # explode
                self.effect_animation = self.import_assets(self.explosion_path)
                self.frame_index = 0
                self.direction = pygame.math.Vector2(0, 0)
            else:
                self.kill()

    def update(self):
        super().update()
        self.animate_effect()
        if self.direction.x == 0 and self.direction.y == 0 and \
                self.frame_index + self.animation_speed >= len(self.effect_animation):
            # destroys the projectile after explosion (if it explodes)
            self.kill()
        self.image = pygame.transform.rotate(self.effect.image, -self.direction.as_polar()[1])
        self.move()