import pygame
from parametres import *
from rays_geometry import ray_casting
from play_map import mini_map

class Drawing:
    def __init__(self, screen, screen_map):
        self.screen = screen
        self.screen_map = screen_map
        self.font = pygame.font.SysFont('Arial', 36, bold=True)
        self.textures = {1: pygame.image.load('images/wall1.png').convert(),
                         2: pygame.image.load('images/wall2.png').convert(),
                         'S': pygame.image.load('images/luna.jpg').convert()
                         }

    def background(self, angle):
        sky_offset = -10 * math.degrees(angle) % width
        self.screen.blit(self.textures['S'], (sky_offset, 0))
        self.screen.blit(self.textures['S'], (sky_offset - width, 0))
        self.screen.blit(self.textures['S'], (sky_offset + width, 0))
        pygame.draw.rect(self.screen, (20, 20, 20), (0, (height // 2), width, (height // 2)))

    def world(self, world_objects):
        for obj in sorted(world_objects, key=lambda n: n[0], reverse=True):
            if obj[0]:
                _, object, object_pos = obj
                self.screen.blit(object, object_pos)

    def mini_map(self, player):
        self.screen_map.fill((0, 0, 0))
        map_x, map_y = player.x // map_scale, player.y // map_scale
        pygame.draw.line(self.screen_map, (220, 220, 0), (map_x, map_y), (map_x + 10 * math.cos(player.angle),
                                                                          map_y + 10 * math.sin(player.angle)), 2)
        pygame.draw.circle(self.screen_map, (250, 0, 0), (int(map_x), int(map_y)), 5)
        for x, y in mini_map:
            pygame.draw.rect(self.screen_map, (169, 200, 150), (x, y, map_tile, map_tile))
        self.screen.blit(self.screen_map, map_pos)