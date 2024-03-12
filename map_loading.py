import pygame
from settings import TILE_SIZE
from csv import reader


def import_tiles(path):  # divides the image of the tiles and and returns a list of them as separate tiles (as pygame surface)
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / TILE_SIZE)
    tile_num_y = int(surface.get_size()[1] / TILE_SIZE)

    tile_surfaces = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            new_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
            new_surf.blit(surface, (0, 0), pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            tile_surfaces.append(new_surf)
    return tile_surfaces


def import_csv_layout(path):    # returns a list of the csv file of the map layout
    terrain = []
    with open(path) as map:
        level = reader(map, delimiter = ",")
        for row in level:
            terrain.append(list(row))

    return terrain
