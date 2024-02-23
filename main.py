import pygame
from settings import *
from level import Level


class Game:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Element Rumble")
        self.clock = pygame.time.Clock()
        self.level = Level()
        self.RUN = True


    def run(self):
        while self.RUN:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            self.win.fill("black")
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()