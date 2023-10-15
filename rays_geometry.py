import pygame
from parametres import *
from play_map import world_map

def ray_casting(screen, player_position, angle_of_player):

    xo, yo = player_position
    current_angle = angle_of_player - (field_of_wiev / 2)
    for ray in range(count_of_rays):   #на каждый луч выстраиваем его косинус и синус,необходимо для грамотной видимости
        sin_a = math.sin(current_angle)
        cos_a = math.cos(current_angle)
        for depth in range(max_depth): #глубина видимости игрока
            x = xo + depth * cos_a
            y = yo + depth * sin_a
            if (x // tile * tile, y // tile * tile) in world_map: #при нахождении луча в видимости карты, выстроить
                depth *= math.cos(angle_of_player - current_angle)          #глубину видимости и высоту стен
                proj_height = min(project_coeff / (depth + 0.0001), height)
                c = 255 / (1 + depth * depth * 0.0001)          #реализация затемнения
                color = (c // 2, c, c // 3)
                pygame.draw.rect(screen, color, (ray * scale, (height // 2) - proj_height // 2, scale, proj_height))
                break
        current_angle += delta_angle #поворот головы