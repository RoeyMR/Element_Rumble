import pygame


class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups, image_path):
        super().__init__(groups)

        self.damage = 10

        self.player = player
        direction = self.player.status.split("_")[0]
        self.image = pygame.image.load(image_path)
        self.base_image = pygame.image.load(image_path)
        self.previous_direction = direction

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
        direction = self.player.status.split("_")[0]
        # sets the location of the weapon according to the direction of the player
        if direction == "right":
            if self.previous_direction != direction:
                self.image = self.base_image.copy()
            self.rect = self.image.get_rect(midleft = self.player.rect.midright)
            self.rect.x -= 5
        elif direction == "left":
            if self.previous_direction != direction:
                self.image = pygame.transform.flip(self.base_image, True, False)
            self.rect = self.image.get_rect(midright = self.player.rect.midleft)
            self.rect.x += 5
        elif direction == "front":
            if self.previous_direction != direction:
                self.image = pygame.transform.flip(self.base_image, False, True)
            self.rect = self.image.get_rect(midtop = self.player.rect.midbottom)
            self.rect.y -= 15
            self.rect.x += 5
        else:
            if self.previous_direction != direction:
                self.image = pygame.transform.flip(self.base_image, True, False)
            self.rect = self.image.get_rect(midbottom = self.player.rect.midtop)
            self.rect.y += 25
            self.rect.x -= 5
        self.previous_direction = direction