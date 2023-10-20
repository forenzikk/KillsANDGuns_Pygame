import pygame
from parametres import *
from play_map import world_map


def mapping(a, b):
    return (a // tile) * tile, (b // tile) * tile

def ray_casting(screen, player_position, angle_of_player):

    xo, yo = player_position
    xn, yn = mapping(xo, yo)

    current_angle = angle_of_player - (field_of_wiev / 2)
    for ray in range(count_of_rays):   #на каждый луч выстраиваем его косинус и синус,необходимо для грамотной видимости
        sin_a = math.sin(current_angle)
        cos_a = math.cos(current_angle)

        if sin_a:
            sin_a = sin_a
        else:
            sin_a = 0.000001

        if cos_a:
            cos_a = cos_a
        else:
            cos_a = 0.000001

        #vertical
        if cos_a >= 0:
            x, dx = xn + tile, 1
        else:
            x, dx = xn, -1

        for i in range(0, width, tile):
            depth_vertical = (x - xo) / cos_a
            y = yo + depth_vertical * sin_a
            if mapping(x + dx, y) in world_map:
                break
            x += dx * tile

        #horizontal
        if sin_a >= 0:
            y, dy = yn + tile, 1
        else:
            y, dy = yn, -1

        for i in range(0, height, tile):
            depth_horizontal = (y - yo) / sin_a
            x = xo + depth_horizontal * cos_a
            if mapping(x, y + dy) in world_map:
                break
            y += dy * tile

        #projection
        if depth_vertical < depth_horizontal:
            depth = depth_vertical
        else:
            depth = depth_horizontal

        depth *= math.cos(angle_of_player - current_angle)
        proj_height = project_coeff / depth
        c = 255 / (1 + depth * depth * 0.00002)#реализация затемнения стен
        color = (c, c // 2, c // 3)

        pygame.draw.rect(screen, color, (ray * scale, (height // 2) - proj_height // 2, scale, proj_height))
        current_angle += delta_angle
