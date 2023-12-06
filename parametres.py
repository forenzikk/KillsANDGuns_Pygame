import math
import pygame

#width = 1200
#height = 800
tile = 100  # размер квадрата карты

minimap_scale = 5  # масштабирующий коэффициент
minimap_res = (1200 // minimap_scale - 70, 800 //
               minimap_scale)  # размер мини-карты
map_scale = 2 * minimap_scale  # числовой коэффициент
map_tile = tile // map_scale  # масштаб для стороны квадрата
map_position = (0, 800 - 800 // minimap_scale - 640)

count_of_rays = 300
max_depth = 800
delta_angle = (math.pi / 3) / count_of_rays
# расстояние от игрока до стены
distantion = count_of_rays / (2 * math.tan(((math.pi / 3) / 2)))
# проекция высоты (основание треугольника по подобию)
proj_coeff = 3 * distantion * tile
# масштабирующий коэффициаент (чтобы без тормозов работало)
scale = 1200 // count_of_rays

center_of_ray = count_of_rays // 2 - 1
fake_rays = 100
fake_rays_range = count_of_rays - 1 + 2 * fake_rays

width_of_textures = 1200
height_of_textures = 1200
scale_texture = width_of_textures // tile

player_position = (600 // 4, 350)
player_angle = 0  # направление взгляда игрока
player_speed = 2
