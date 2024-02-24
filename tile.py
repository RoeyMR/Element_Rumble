import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(r"C:\Users\roeym\PycharmProjects\Element_Rumble\tile assets\rock.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
