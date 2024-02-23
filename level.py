import pygame


class Level:
    def __init__(self):
        self.sprites = pygame.sprite.Group()
        self.obstacles_sprites = pygame.sprite.Group()
        self.display_surface = pygame.display.get_surface()


    def run(self):
        pass