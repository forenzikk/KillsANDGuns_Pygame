import pygame
from parametres import *
from rays_geometry import *
from play_map import *


class element_of_textures:
    def __init__(self, screen, screen_map):
        self.screen = screen
        self.screen_map = screen_map
        self.font = pygame.font.SysFont('Arial', 36, bold=True)

    def background(self):#фон
        pygame.draw.rect(self.screen, (40, 40, 40), (0, 0, width, (height // 2)))
        pygame.draw.rect(self.screen, (15, 15, 15), (0, (height // 2), width, (height // 2)))

    def world(self, player_pos, angle_of_player):#реализация геометрии 1-го лица
        ray_casting(self.screen, player_pos, angle_of_player)

    def mini_map(self, player):#мини-карта в окне
        self.screen_map.fill((0, 0, 0))
        map_x, map_y = player.x // map_scale, player.y // map_scale
        pygame.draw.line(self.screen_map, (220, 0, 0), (map_x, map_y), (map_x + 10 * math.cos(player.angle),
                                                               map_y + 10 * math.sin(player.angle)), 2)#направление
        pygame.draw.circle(self.screen_map, (220, 0, 0), (int(map_x), int(map_y)), 5)#позиция
        for y, x in minimap:
            pygame.draw.rect(self.screen_map, (0, 220, 0), (x, y, map_tile, map_tile))
        self.screen.blit(self.screen_map, map_position)